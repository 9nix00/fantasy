"""
=============
Fantasy
=============

Fantasy Bootstrap Loader

QuickStart
-------------

python -m fantasy_kickstart init project-1


"""

import os

version = "0.2.16"
version_info = version.split('.')

# active database

requirement_env_dict = {
    # active
    'FANTASY_ACTIVE_DB': 'yes',
    'FANTASY_ACTIVE_CACHE': 'yes',
    'FANTASY_ACTIVE_EXPORTER': 'yes',
    'FANTASY_ACTIVE_SENTRY': 'yes',
    'FANTASY_ACTIVE_ACCOUNT': 'yes',
    # account settings
    'FANTASY_ACCOUNT_SECURITY_MODE': 'no',
    'FANTASY_ACCOUNT_MODEL': 'account.models.Account',
    'FANTASY_ROLE_MODEL': 'account.models.Role',
    'FANTASY_AUTO_MIGRATE': 'no',
    'FANTASY_TRACK_MODE': 'no',
    'FANTASY_WORKSPACE': os.getcwd(),
    'CELERY_APP_NAME': 'fantasy',
}

for k, v in requirement_env_dict.items():
    os.environ.setdefault(k, v)
    pass

optional_env_list = [
    'FANTASY_ADMIN_NAME',  # admin
    'FANTASY_ADMIN_TEMPLATE_MODE',  # bootstrap3
    'FANTASY_SETTINGS_MODULE',  # web.conf
    'FLASK_SECRET_KEY',  # flask-security require
]

global_env_list = [
    'FANTASY_ACTIVE_DB',
    'FANTASY_SETTINGS_MODULE',
]

all_env_list = list(requirement_env_dict.keys()) + optional_env_list

config_env_list = [k for k in all_env_list if k not in global_env_list]


def show_env(p=print):
    """show optional environment"""
    p('requirements:')
    p(requirement_env_dict)
    p('optional:')
    p(optional_env_list)

    p('active db:')
    p(['SQLALCHEMY_DATABASE_URI', ])

    p('active cache:')
    p(['CACHE_TYPE', ])
    pass
