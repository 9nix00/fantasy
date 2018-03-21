"""
======================
MongoDB ORM utils

..todo::
    i18n support

======================
"""

from mongoengine.errors import ValidationError, DoesNotExist, NotUniqueError
from webargs.flaskparser import abort


def get_document(document_class, pk):
    try:
        data = document_class.objects.get(pk=pk)
    except (AttributeError, ValidationError, DoesNotExist):
        abort(404, errors={
            'detail': 'pk not exists'
        })
        pass
    return data


def save_document(doc, conflict_msg=None):
    try:
        doc.save()
    except NotUniqueError:
        abort(422, errors={
            'detail': conflict_msg or '写入失败，存在不唯一文档'
        })
        pass
    pass
