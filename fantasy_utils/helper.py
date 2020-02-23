"""
=================
Context Helper
=================
"""

from flask import current_app as app
from contextlib import contextmanager


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = app.db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    # finally:
    #     don't close session
    #     session.close()
    pass