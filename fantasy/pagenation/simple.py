"""
=============
简单分页
=============

一种通用分页工具
"""

from math import ceil

from flask import request


class Pagination(object):

    def __init__(self, page, per_page, total_count, page_key='page',
                 limit_key='limit'):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.page_key = page_key
        self.limit_key = limit_key
        pass

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def query_params(self):
        query_params = {}
        query_string = request.query_string.decode()
        for v in query_string.split('&'):
            pairs = v.split('=')
            key = pairs[0]
            value = pairs[1] if len(pairs) > 1 else ''
            query_params[key] = value
            pass
        return query_params

    @property
    def prev_page(self):
        return request.base_url + '?' + self.build_query_string(
            self.page - 1) if self.has_prev else None

    @property
    def next_page(self):
        return request.base_url + '?' + self.build_query_string(
            self.page + 1) if self.has_next else None

    @property
    def start(self):
        return max(0, (self.page - 1) * self.per_page)

    @property
    def end(self):
        return max(0, self.start + self.per_page)

    @property
    def count(self):
        return self.total_count

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):

            is_outside = (num > self.page - left_current - 1) and \
                         (num < self.page + right_current)

            if num <= left_edge or is_outside or \
                    num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

    def build_query_string(self, page):
        query_string = ''
        for k, v in self.query_params.items():
            use_value = page if k == 'page' else v
            query_string += '&%s=%s' % (k, use_value)
            pass
        return query_string.strip('&')
