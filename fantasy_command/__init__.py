"""
=============

=============
"""

import click
from flask import current_app as app
from flask.cli import with_appcontext

@click.group()
def ff():
    """
    Fantasy toolbox.
    """
    pass

