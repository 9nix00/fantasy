"""
======================
Bootstrap for  Flask
======================
"""

import importlib
import os

from flask import Flask

from . import config_env_list, version

_db = None
if os.environ.get('FANTASY_ACTIVE_DB', 'no') == 'yes':
    from flask_sqlalchemy import SQLAlchemy

    _db = SQLAlchemy()
    pass

_celery = None
if os.environ.get('FANTASY_ACTIVE_CELERY', 'no') == 'yes':
    from celery import Celery

    _celery = Celery(os.environ.get('CELERY_APP_NAME', 'fantasy'),
                     backend=os.environ.get('CELERY_RESULT_BACKEND',
                                            'redis://localhost:6379/2'),
                     broker=os.environ.get('CELERY_BROKER_URL',
                                           'redis://localhost:6379/1'))
    pass


def router(app, sub_apps={}):
    from werkzeug.wsgi import DispatcherMiddleware
    embed_apps = {}

    if app.config['FANTASY_ACTIVE_EXPORTER'] == 'yes':
        from prometheus_client import make_wsgi_app
        embed_apps['/metrics'] = make_wsgi_app()

    if embed_apps:
        sub_apps.update(embed_apps)

    return DispatcherMiddleware(app, sub_apps)


class FantasyFlask(Flask):
    """replacement for default Flask

    ..note::

        make sure you use same SQLAlchemy instance.
        otherwise you may cause a permanent lock error.

    """
    cache = None
    celery = _celery
    db = _db
    pass


def smart_database(app):
    """Initial Database"""

    from sqlalchemy.engine.url import make_url
    from sqlalchemy_utils import database_exists, create_database

    # if database not exist,try add it.
    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        raise ValueError('Database Mode is active,'
                         'but config.SQLALCHEMY_DATABASE_URI is not set.')

    dsn = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(dsn):
        create_database(dsn)
        pass
    pass


def smart_migrate(app):
    """Migrate database if migrations exists and AUTO_MIGRATE set to 'yes'"""

    db = app.db

    migrations_root = os.path.join(
        app.config.get('FANTASY_MIGRATION_PATH', os.getcwd()), 'migrations')

    if os.path.exists(migrations_root) and \
            app.config['FANTASY_AUTO_MIGRATE'] == 'yes':
        from flask_migrate import (Migrate,
                                   upgrade as migrate_upgrade)

        migrate = Migrate(app, db, directory=migrations_root)
        migrate.init_app(app, db)
        migrate_upgrade(migrations_root)
        pass
    pass


def smart_account(app):
    """Active account, depends on flask_security"""
    if app.config['FANTASY_ACTIVE_ACCOUNT'] == 'no':
        return

    from flask_security import SQLAlchemyUserDatastore, Security

    account_module_name, account_class_name = app.config[
        'FANTASY_ACCOUNT_MODEL'].rsplit('.', 1)

    account_module = importlib.import_module(account_module_name)
    account_class = getattr(account_module, account_class_name)

    role_module_name, role_class_name = app.config[
        'FANTASY_ROLE_MODEL'].rsplit('.', 1)
    role_module = importlib.import_module(role_module_name)
    role_class = getattr(role_module, role_class_name)

    r = True if app.config[
                    'FANTASY_ACCOUNT_SECURITY_MODE'] != 'no' else False

    Security(app,
             SQLAlchemyUserDatastore(
                 app.db, account_class, role_class),
             register_blueprint=r)
    pass


def smart_logging():
    """
    ..deprecated::

        弃用，应该通过类似run_app注入的方式来完成

    :return:
    """
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


def track_info(msg):
    track_mode = os.environ['FANTASY_TRACK_MODE'] == 'yes'
    if track_mode:
        print(msg)
    pass


def create_app(app_name, config={}):
    """
    App Factory Tools

    Workflow: follow the track_infos,current has 15 steps.

    primary workflow:

    1. call a dirty way to hack depends package,e.g: webargs
    1. merge config from env.FANTASY_SETTINGS_MODULE if user defined
    1. call error_handle if user defined
    1. call run_admin if user defined
    1. call run_cli if user defined
    :return:
    """

    track_info('(00/14)fantasy track mode active...')
    from webargs.flaskparser import parser
    from . import error_handler, cli

    track_info('(01/14)i18n webargs...')
    if os.environ.get('LANG') == 'zh_CN.UTF-8':
        from .i18n import zh_cn
        zh_cn()
        pass

    track_info('(02/14)initial app...')
    mod = importlib.import_module(app_name)
    app = FantasyFlask(app_name, root_path=os.path.dirname(mod.__file__))

    track_info('(03/14)update app.config...')
    if config:
        app.config.update(config)

    # 由外部做显式声明，否则不做调用
    config_module = os.environ.get('FANTASY_SETTINGS_MODULE', None)
    if config_module:
        track_info(
            "       found config module %s,try load it..." % config_module)
        app.config.from_object(config_module)

    track_info("       merge config from os.environment.")
    for k in config_env_list:
        if not app.config.get(k):
            track_info("              key: %s merged" % k)
            app.config.update({
                k: os.environ.get(k, None)
            })
            pass
        pass

    track_info('(04/14)confirm cors...')
    if app.config['FANTASY_ACTIVE_CORS'] == 'yes':
        from flask_cors import CORS
        CORS(app, **app.config.get('CORS_KWARGS', {}))
        pass

    track_info('(05/14)bind app context...')
    with app.app_context():
        track_info('(06/14)confirm db handle... skip for now...')

        track_info('(07/14)confirm sentry...')
        if app.config['FANTASY_ACTIVE_SENTRY'] == 'yes':
            from raven.contrib.flask import Sentry
            Sentry(app)
            pass

        if app.config['FANTASY_ACTIVE_EXPORTER'] == 'yes':
            from prometheus_client import make_wsgi_app
            from flask_prometheus_metrics import register_metrics
            register_metrics(app, app_version='v' + version,
                             app_config=app.config['ENV'])

            pass

        track_info('(08/14)confirm cache...')
        if app.config['FANTASY_ACTIVE_CACHE'] == 'yes':
            from flask_caching import Cache
            app.cache = Cache(app, config=app.config)
            pass

        track_info('(09/14)active app...')
        if hasattr(mod, 'run_app'):
            run_app = getattr(mod, 'run_app')

            try:
                run_app(app)
            except Exception as e:
                if hasattr(app, 'sentry'):
                    app.sentry.handle_exception(e)
                    pass

                import sys
                import traceback
                traceback.print_exc()
                sys.exit(-1)

            pass

        if app.db:
            track_info('(10/14)trigger auto migrate...')

            smart_database(app)
            smart_migrate(app)
            smart_account(app)
            app.db.init_app(app)

            # disable, may cause another problem
            # @app.teardown_request
            # def session_clear(exception=None):
            #     if exception and app.db.session.is_active:
            #         app.db.session.rollback()
            #         app.db.session.remove()
            pass

        track_info('(11/14)bind error handle...')

        @parser.error_handler
        def handle_error(error, req, schema, status_code, headers, *args,
                         **kwargs):
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

        track_info('(12/14)bind admin handle...')
        if hasattr(mod, 'run_admin'):
            import flask_admin

            try:
                admin_name = app.config.get('FANTASY_ADMIN_NAME')
            except KeyError:
                admin_name = 'Admin'

            try:
                admin_tpl_name = app.config.get(
                    'FANTASY_ADMIN_TEMPLATE_MODE')
            except KeyError:
                admin_tpl_name = 'bootstrap3'

            admin = flask_admin.Admin(name=admin_name,
                                      template_mode=admin_tpl_name)

            run_admin = getattr(mod, 'run_admin')
            run_admin(admin)
            admin.init_app(app)
            pass

        pass

    track_info('(13/14)bind ff command...')
    app.cli.add_command(cli.ff)

    track_info('(14/14)bind cli command...')
    if hasattr(mod, 'run_cli'):
        run_cli = getattr(mod, 'run_cli')
        run_cli(app)
        pass

    return app
