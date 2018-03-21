"""
=============
Core
=============

底层配置
"""

from flask import current_app
from werkzeug.local import LocalProxy

_fantasy = LocalProxy(lambda: current_app.extensions['fantasy'])


class Fantasy(object):
    def __init__(self, app=None, prefix='hive_', **kwargs):
        self.app = app
        self._kwargs = kwargs

        if app is not None:
            self._state = self.init_app(app, prefix, **kwargs)
        pass

    def init_app(self, app, prefix='hive_', **kwargs):
        self.app = app

        for key, value in self._kwargs.items():
            kwargs.setdefault(key, value)

        # for key, value in _default_config.items():
        #     app.config.setdefault(prefix.upper() + key, value)

        self._state = state = _get_state(app, datastore, **kwargs)  # noqa: F821,F841,E501

        pass


pass
