"""
================
app boot file
================
"""
import os
import sys

for k in [
    'FANTASY_ACTIVE_DB',
    'FANTASY_ACTIVE_CACHE',
    'FANTASY_ACTIVE_SENTRY',
]:
    os.environ[k] = 'no'

os.environ.setdefault('FANTASY_APP', 'welcome')

from fantasy.bootstrap import create_app, router

sys.path.insert(0, __file__.rsplit('/', 2)[0])
home = create_app(os.environ['FANTASY_APP'])
app = router(home)

if __name__ == '__main__':
    import os
    import sys
    from werkzeug.serving import run_simple

    if len(sys.argv) == 1 or sys.argv[1] == 'serve':
        bind_ip = os.environ.get('FLASK_SIMPLE_BIND', '127.0.0.1')

        run_simple(bind_ip, 5001, app,
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
