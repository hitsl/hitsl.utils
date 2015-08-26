# -*- coding: utf-8 -*-

__author__ = 'viruzzz-kun'


def transfer_fields(src, dst, names):
    for name in names:
        setattr(dst, name, getattr(src, name))


def functools_compose(*funcs):
    if len(funcs) < 2:
        raise Exception(u'Must me at least 2 functions to compose')
    head = funcs[0]
    tail = funcs[1:]

    def wrapper(*args, **kwargs):
        result = head(*args, **kwargs)
        for func in tail:
            result = func(result)
        return result

    return wrapper


def translate_dict(source, attr):
    return dict(
        (item[attr], item)
        for item in source
    )


def first(sequence):
    if len(sequence) > 0:
        return sequence[0]
