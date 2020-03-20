"""
=====================
improve builtin-dict
=====================
"""

import json


class objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class objectview(object):
    def __init__(self, d):
        self.__dict__ = d


class jsonview(object):
    """Halt in pypy3"""
    def __init__(self, d):
        self.__dict__ = json.loads(d)
