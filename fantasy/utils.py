"""
=============
全局通用库函数
=============
"""

from flask import current_app
from werkzeug.local import LocalProxy

_fantasy = LocalProxy(lambda: current_app.extensions['security'])
localize_callback = LocalProxy(lambda: _fantasy.i18n_domain.gettext)


def get_config(app, prefix='hive_'):
    """Conveniently get the security configuration for the specified
    application without the annoying 'SECURITY_' prefix.

    :param app: The application to inspect
    """
    items = app.config.items()
    prefix = prefix.upper()

    def strip_prefix(tup):
        return (tup[0].replace(prefix, ''), tup[1])

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def config_value(key, app=None, default=None, prefix='hive_'):
    """Get a Flask-Security configuration value.

    :param key: The configuration key without the prefix `SECURITY_`
    :param app: An optional specific application to inspect. Defaults to
                Flask's `current_app`
    :param default: An optional default value if the value is not set
    """
    app = app or current_app
    return get_config(app, prefix=prefix).get(key.upper(), default)
