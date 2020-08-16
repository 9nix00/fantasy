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

version = "0.4.2"
version_info = version.split('.')

# active database

requirement_env_dict = {
    # active
    'FANTASY_ACTIVE_DB': 'no',
    'FANTASY_ACTIVE_CELERY': 'no',
    'FANTASY_ACTIVE_CACHE': 'yes',
    'FANTASY_ACTIVE_DOC_DB': 'no',
    'FANTASY_ACTIVE_EXPORTER': 'yes',
    'FANTASY_ACTIVE_SENTRY': 'yes',
    'FANTASY_ACTIVE_ACCOUNT': 'yes',
    'FANTASY_ACTIVE_ADMIN': 'no',
    'FANTASY_ACTIVE_CLI': 'yes',
    'FANTASY_ACTIVE_I18N': 'yes',
    'FANTASY_ACTIVE_CORS': 'no',
    'FANTASY_APPLICATION_ROOT': '/',
    # account settings
    'FANTASY_ACCOUNT_SECURITY_MODE': 'no',
    'FANTASY_ACCOUNT_MODEL': 'account.models.Account',
    'FANTASY_ROLE_MODEL': 'account.models.Role',
    'FANTASY_AUTO_MIGRATE': 'no',
    'FANTASY_TRACK_MODE': 'no',
    'FANTASY_WORKSPACE': os.getcwd(),
    'CELERY_APP_NAME': 'fantasy',
    'SQLALCHEMY_TRACK_MODIFICATIONS': 'no',
    'FANTASY_TASKS_PATH': '',
    'FANTASY_STORAGE_MODULE': ''
}

for k, v in requirement_env_dict.items():
    os.environ.setdefault(k, v)
    pass

optional_env_list = [
    'FANTASY_ADMIN_NAME',  # admin
    'FANTASY_ADMIN_TEMPLATE_MODE',  # bootstrap3
    'FANTASY_ACCOUNT_MANAGER',
    'FANTASY_ADMIN_NAME'
]

global_env_list = [
    'FANTASY_ACTIVE_DB',
    'FANTASY_ACTIVE_DOC_DB',
    'FANTASY_SETTINGS_MODULE',
    'FANTASY_APPLICATION_ROOT',
    'FANTASY_APP',
    # support load from app.config
    # 'FANTASY_ACTIVE_CELERY',
    # 'CELERY_APP_NAME',
    # 'CELERY_RESULT_BACKEND',
    # 'CELERY_BROKER_URL',
]

all_env_list = list(requirement_env_dict.keys()) + optional_env_list

config_env_list = [k for k in all_env_list if k not in global_env_list]


def show_env(p=print):
    """show optional environment"""
    p('requirements:')
    p(requirement_env_dict)
    p('global[set in os.environ]:')
    p(global_env_list)
    p('optional:')
    p(optional_env_list)

    p('active db:')
    p(['SQLALCHEMY_DATABASE_URI', 'FANTASY_MIGRATION_PATH'])

    p('active session:')
    p(['SESSION_TYPE', 'SESSION_KEY'])

    p('active cache:')
    p(['CACHE_TYPE', 'CACHE_REDIS_URL'])

    p('user feature:')
    p(['ACCOUNT_TOKEN_SALT',
       'ACCOUNT_USERNAME_DISABLE_REGISTER',
       'ACCOUNT_TOKEN_TTL',
       'SECRET_KEY'])

    p('cors feature:')
    p(['CORS_KWARGS', ])

    p('flask built-in:')
    p(['FLASK_ENV', ])

    pass
