"""
=================
Context Helper
=================
"""

from contextlib import contextmanager

from flask import current_app as app


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


def pagination(q, keys):
    return {
        'has_next': q.has_next,
        'has_prev': q.has_prev,
        'page': q.page,
        'pages': q.pages,
        'prev_num': q.prev_num,
        'total': q.total,
        'items': [{k: getattr(row, k) for k in keys} for row in q.items]
    }
