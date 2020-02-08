"""
=============

=============
"""

import importlib
import os
import sys

import click

from . import ff, with_appcontext, app


def get_migrations_root(migrations_root):
    migrations_root = migrations_root or os.path.join(
        os.environ.get('FANTASY_MIGRATION_PATH',
                       os.environ['FANTASY_WORKSPACE']), 'migrations')

    return os.path.expanduser(migrations_root)


@ff.command()
@click.option('--migrations-root', type=click.Path(exists=False))
@with_appcontext
def makemigrations(migrations_root):
    """a command same as django makemigrations

    migrations path search order:

    1. migrations_root set by user
    1. environment: FANTASY_MIGRATION_PATH
    1. environment: FANTASY_WORKSPACE + /migrations

    """
    from flask_migrate import (Migrate, init as migrate_init,
                               migrate as migrate_exec)

    migrations_root = get_migrations_root(migrations_root)
    mig = Migrate(app, app.db, directory=migrations_root)

    if not os.path.exists(migrations_root):
        migrate_init(migrations_root)
        pass

    models_file = os.path.join(migrations_root, 'models.txt')

    if not os.path.exists(models_file):
        with open(models_file, 'w') as fw:
            fw.write('# add module name in this file.')
            pass
        pass

    with open(models_file, 'r') as fp:
        modules = fp.readlines()
        pass

    modules = filter(lambda x: x.strip("\n"), modules)
    modules = map(lambda x: x.strip("\n").split("#")[0].strip(), modules)
    modules = list(filter(lambda x: x, modules))

    if not modules:
        click.echo(
            click.style('No Model found,'
                        'skip create migrations...'
                        'You need edit %s file set your module' % models_file,
                        fg='yellow'))
        sys.exit(0)

    for m in modules:
        importlib.import_module(m + '.models')
        pass

    migrate_exec(migrations_root)
    mig.init_app(app, app.db)
    pass


@ff.command()
@click.option('--migrations-root', type=click.Path(exists=False))
@with_appcontext
def migrate(migrations_root):
    """a command same as django migrate

    ..note::
        if database not exist, will create it.
        the default charset use

    """

    from flask_migrate import Migrate, upgrade as migrate_upgrade
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy.engine.url import make_url
    from sqlalchemy_utils import database_exists, create_database

    if not app.config['SQLALCHEMY_DATABASE_URI']:
        click.echo(
            click.style(
                'no SQLALCHEMY_DATABASE_URI config found,skip migrate...',
                fg='red'))
        sys.exit(-1)

    dsn = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(dsn):
        create_database(dsn,
                        encoding=app.config.get('SQLALCHEMY_DATABASE_CHARSET',
                                                'utf8mb4'))
        pass

    migrations_root = get_migrations_root(migrations_root)

    if not os.path.exists(migrations_root):
        click.echo(
            click.style('migration files not exist,skip migrate...', fg='red'))
        sys.exit(-1)

    db = SQLAlchemy()
    mig = Migrate(app, db, directory=migrations_root)
    mig.init_app(app, db)
    migrate_upgrade(migrations_root)
    pass
