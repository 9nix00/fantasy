"""
================
Fantasy Tools
================

参数

-f app.yaml file

指令：
init    初始化项目
sync    根据配置初始化项目
    --private-key, -i
info    查看当前环境变量
flask   flask wrapper
serve   运行debug app
    --port: 5000
    --bind: 127.0.0.1
"""

import os
import sys

import click


class Captain(object):
    def __init__(self, debug=False, dry_run=False, verbose=0):
        self.debug = debug
        self.dry_run = dry_run
        self.verbose_count = verbose
        self.logger = logger
        self.logger_level = logging.CRITICAL

        if verbose == 1:
            self.logger_level = logging.ERROR
        elif verbose == 2:
            self.logger_level = logging.WARNING
        elif verbose == 3:
            self.logger_level = logging.INFO
        else:
            self.logger_level = logging.DEBUG
            pass

        if self.debug:
            self.logger_level = logging.DEBUG

        self.logger.setLevel(self.logger_level)
        pass


@click.group()
@click.option('--debug', default=False,
              envvar='FANTASY_DEBUG')
@click.option('-v', '--verbose', count=True)
@click.option('-V', '--version', count=True)
@click.pass_context
def cli(ctx, debug, verbose):
    """Fantasy

    A modern SRE tool.
    """
    ctx.obj = captain.Captain(debug, dry_run, verbose)
    pass


cli.add_command(report)
cli.add_command(fetch_log)
cli.add_command(init)

from fantasy.bootstrap import create_app

app = create_app(os.environ['FANTASY_APP'])

if __name__ == '__main__':
    import os
    import sys
    from werkzeug.serving import run_simple

    if len(sys.argv) == 1 or sys.argv[1] == 'serve':
        bind_ip = os.environ.get('FLASK_SIMPLE_BIND', '127.0.0.1')

        run_simple(bind_ip, 5000, app,
                   use_reloader=True, use_debugger=True, use_evalex=True)
    elif sys.argv[1] == 'queue':
        from fantasy.celery import create_celery, load_tasks

        load_tasks(app, __file__)
    else:
        import click
        from flask.cli import FlaskGroup


        def cli_app(info):
            return app


        @click.group(cls=FlaskGroup, create_app=cli_app)
        def cli():
            pass


        cli()
    pass
