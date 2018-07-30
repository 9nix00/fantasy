"""
=============
Fantasy
=============

Fantasy在我所做的基于Flask项目中一直发挥着作用。
虽然还有很大的优化空间，但从目前看，效果也算是稳定，符合预期。

在我的项目中，Fantasy是为了解决在团队内部开发的Hive-App（本质上是Flask App）之间
构造一层。提供通用的工具链，模块之间的数据尽可能的复用。

目前因为入职的关系，考虑到版权相关的风险因素，所以将这部分代码开源。
后期也会持续提供迭代改进。

"""

import importlib
import os

from flask import Flask

version = "0.2.6"
version_info = version.split('.')

os.environ.setdefault('FANTASY_ACTIVE_DB', 'yes')
os.environ.setdefault('FANTASY_ACTIVE_CACHE', 'yes')
os.environ.setdefault('FANTASY_ACTIVE_SENTRY', 'no')
os.environ.setdefault('FANTASY_ACTIVE_ACCOUNT', 'yes')
os.environ.setdefault('FANTASY_ACCOUNT_SECURITY_MODE', 'no')
os.environ.setdefault('FANTASY_ACCOUNT_MODEL', 'account.models.Account')
os.environ.setdefault('FANTASY_ROLE_MODEL', 'account.models.Role')
os.environ.setdefault('FANTASY_PRIMARY_NODE', 'no')

_db = None
if os.environ.get('FANTASY_ACTIVE_DB', 'no') != 'no':
    from flask_sqlalchemy import SQLAlchemy

    _db = SQLAlchemy()
    pass


class FantasyFlask(Flask):
    db = None
    cache = None
    celery = None
    pass


def smart_database(app):
    """尝试对数据库做初始化操作"""

    from sqlalchemy.engine.url import make_url
    from sqlalchemy_utils import database_exists, create_database

    # 如果数据库不存在，则尝试创建数据
    dsn = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(dsn):
        create_database(dsn)
        pass
    pass


def smart_migrate(app, migrations_root):
    """如果存在migration且指定为primary_node则执行migrate操作"""

    db = app.db
    if os.path.exists(migrations_root) and \
            os.environ['FANTASY_PRIMARY_NODE'] != 'no':
        from flask_migrate import (Migrate,
                                   upgrade as migrate_upgrade)

        migrate = Migrate(app, db, directory=migrations_root)
        migrate.init_app(app, db)
        migrate_upgrade(migrations_root)
        pass
    pass


def smart_account(app):
    """尝试使用内置方式构建账户"""
    if os.environ['FANTASY_ACTIVE_ACCOUNT'] == 'no':
        return

    from flask_security import SQLAlchemyUserDatastore, Security

    account_module_name, account_class_name = os.environ[
        'FANTASY_ACCOUNT_MODEL'].rsplit('.', 1)

    account_module = importlib.import_module(account_module_name)
    account_class = getattr(account_module, account_class_name)

    role_module_name, role_class_name = os.environ[
        'FANTASY_ROLE_MODEL'].rsplit('.', 1)
    role_module = importlib.import_module(role_module_name)
    role_class = getattr(role_module, role_class_name)

    r = True if os.environ[
                    'FANTASY_ACCOUNT_SECURITY_MODE'] != 'no' else False

    Security(app,
             SQLAlchemyUserDatastore(
                 app.db, account_class, role_class),
             register_blueprint=r)
    pass


def smart_logging():
    import sys
    from logging.config import dictConfig

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'shopping': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    })
    pass


def load_tasks(app, entry_file=None):
    """装载任务，解决celery无法自动装载的问题"""
    from celery import Task
    tasks_txt = os.path.join(os.path.dirname(entry_file), 'migrations',
                             'tasks.txt')

    if not os.path.exists(tasks_txt):
        import sys
        print('Tasks file not found:%s' % tasks_txt)
        sys.exit(-1)

    class ContextTask(Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    app.celery.config_from_object(app.config, namespace='CELERY')
    app.celery.Task = ContextTask

    with app.app_context():
        with open(tasks_txt, 'r') as f:
            for line in f:
                mod = line.strip('\n')
                if mod:
                    importlib.import_module(mod + '.tasks')
                pass
            pass
        pass
    pass


def create_celery(name):
    from .celery import Celery

    celery = Celery(name,
                    backend=os.environ['CELERY_RESULT_BACKEND'],
                    broker=os.environ['CELERY_BROKER_URL'])
    return celery


def create_app(app_name, config={}, db=None, celery=None):
    """
    App Factory 工具

    策略是：
        - 初始化app
        - 根据app_name,装载指定的模块
        - 尝试装载app.run_app
        - 如果指定了`FANTASY_PRIMARY_NODE`，则尝试进行migrate操作
        - 装载error handler

    :return:
    """

    # smart_logging()

    from webargs.flaskparser import parser
    from . import error_handler, hacker, cli

    hacker.hack_webargs()

    migrations_root = os.path.join(
        os.environ.get('FANTASY_MIGRATION_PATH',
                       os.getcwd()),
        'migrations')

    mod = importlib.import_module(app_name)
    app = FantasyFlask(__name__, root_path=os.path.dirname(mod.__file__))

    if config:
        app.config.update(config)

    # 由外部做显式声明，否则不做调用
    config_module = os.environ.get('FANTASY_SETTINGS_MODULE', None)
    if config_module:
        app.config.from_object(config_module)

    if celery:
        app.celery = celery
        pass

    with app.app_context():
        # 通用组件装载区域
        # if os.environ['FANTASY_ACTIVE_DB'] != 'no':
        #     from flask_sqlalchemy import SQLAlchemy
        #     # from sqlalchemy import MetaData
        #     # app.db = SQLAlchemy(metadata=MetaData())
        #     app.db = SQLAlchemy()
        #     pass

        if db is None:
            global _db
            app.db = _db
        else:
            app.db = db

        if os.environ['FANTASY_ACTIVE_CACHE'] != 'no':
            from flask_caching import Cache
            app.cache = Cache(app, config=app.config)
            pass

        if os.environ.get('FANTASY_ACTIVE_SENTRY') != 'no':
            from raven.contrib.flask import Sentry
            Sentry(app)
            pass

        if hasattr(mod, 'run_app'):
            run_app = getattr(mod, 'run_app')
            run_app(app)
            pass

        if app.db:
            smart_database(app)
            smart_migrate(app, migrations_root)
            smart_account(app)
            app.db.init_app(app)

            @app.teardown_request
            def session_clear(exception=None):
                app.db.session.remove()
                if exception and app.db.session.is_active:
                    app.db.session.rollback()

            pass

        # 添加错误控制
        @parser.error_handler
        def h_webargs(error):
            return error_handler.webargs_error(error)

        @app.errorhandler(422)
        def h_422(error):
            return error_handler.http422(error)

        @app.errorhandler(500)
        def h_500(error):
            return error_handler.http500(error)

        if hasattr(mod, 'error_handler'):
            error_handle = getattr(mod, 'error_handle')
            error_handle(app)
            pass

        if hasattr(mod, 'run_admin'):
            import flask_admin
            admin = flask_admin.Admin(name=os.environ.get('FANTASY_ADMIN_NAME',
                                                          'Admin'),
                                      template_mode=os.environ.get(
                                          'FANTASY_ADMIN_TEMPLATE_MODE',
                                          'bootstrap3'))

            run_admin = getattr(mod, 'run_admin')
            run_admin(admin)
            admin.init_app(app)
            pass
        pass

    app.cli.add_command(cli.ff)

    if hasattr(mod, 'run_cli'):
        run_cli = getattr(mod, 'run_cli')
        run_cli(app)
        pass

    return app
