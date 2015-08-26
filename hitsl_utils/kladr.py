# -*- coding: utf-8 -*-

__author__ = 'viruzzz-kun'


class KladrLocality(object):
    # I - IV KLADR levels
    code_len = 11
    level_digits = {
        1: 2,
        2: 5,
        3: 8,
        4: 11
    }

    def __init__(self, **kwargs):
        if 'invalid' in kwargs:
            self.invalid = kwargs['invalid']
            self.name = None
            self.code = kwargs['code'] if 'code' in kwargs else None
            self.level = None
        else:
            self.code = kwargs['code'] if 'code' in kwargs else None
            self.name = kwargs['name'] if 'name' in kwargs else None
            self.level = int(kwargs['level']) if 'level' in kwargs else None
            self.parent_code = kwargs['parent_code'] if 'parent_code' in kwargs else None
        self._set_parents(kwargs.get('parents', []))

    def _set_parents(self, parent_list):
        self.parents = dict((p.level, p) for p in parent_list)
        fullname = ', '.join(
            filter(None, [
                (self.parents[level].name if level in self.parents else (self.name if self.level == level else None))
                for level in range(1, 5)
                ])
        )
        self.fullname = fullname

    def get_region_code(self):
        if self.code:
            return self.code[:2].ljust(self.code_len, '0')

    def get_district_code(self):
        if self.code:
            return self.code[:5].ljust(self.code_len, '0')

    def __json__(self):
        if hasattr(self, 'invalid'):
            return {
                'code': self.code,
                'name': self.invalid,
                'fullname': self.invalid,
                'parent_code': self.invalid
            }
        else:
            return {
                'code': self.code,
                'name': self.name,
                'fullname': self.fullname,
                'parent_code': self.parent_code
            }

    def __unicode__(self):
        return self.invalid if hasattr(self, 'invalid') else self.fullname


class KladrStreet(object):
    # V KLADR level
    code_len = 13

    def __init__(self, **kwargs):
        if 'invalid' in kwargs:
            self.invalid = kwargs['invalid']
            self.code = kwargs['code'] if 'code' in kwargs else None
            self.name = kwargs['invalid']
        else:
            self.code = kwargs['code'] if 'code' in kwargs else None
            self.name = kwargs['name'] if 'name' in kwargs else None

    def __json__(self):
        if hasattr(self, 'invalid'):
            return {
                'code': self.code,
                'name': self.invalid,
            }
        else:
            return {
                'code': self.code,
                'name': self.name,
            }

    def __unicode__(self):
        return self.invalid if hasattr(self, 'invalid') else self.name