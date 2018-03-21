"""
=============

=============
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
