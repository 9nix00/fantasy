"""
=====================
Improve for celery
=====================
"""

import logging
import os

import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal

logger = logging.getLogger(__name__)


class Celery(celery.Celery):
    def on_configure(self):
        dsn = os.environ.get('SENTRY_DSN')
        if not dsn:
            logger.warning('no SENTRY_DSN found in os.environment')
            return

        client = raven.Client(dsn)

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)
        pass


def load_tasks(app, task_file=None):
    """装载任务，解决celery无法自动装载的问题"""
    import importlib

    tasks_root = os.path.join(
        app.config['FANTASY_TASKS_PATH'] if app.config[
            'FANTASY_TASKS_PATH'] else os.getcwd(), 'tasks')

    tasks_txt = task_file or os.path.join(tasks_root, 'main.txt')

    if not os.path.exists(tasks_txt):
        import sys
        print('Tasks file not found:%s' % tasks_txt)
        sys.exit(-1)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    app.celery.config_from_object(app.config, namespace='CELERY')
    app.celery.Task = ContextTask

    with app.app_context():
        with open(tasks_txt, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                mod = line.strip('\n')
                if mod:
                    importlib.import_module(mod + '.tasks')
                pass
            pass
        pass

    return app.celery
