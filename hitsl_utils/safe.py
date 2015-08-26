# -*- coding: utf-8 -*-
import json
import uuid
import datetime
import pytz

__author__ = 'viruzzz-kun'


def string_to_datetime(date_string, formats=None):
    # TODO: Надо разобраться с магией часовых поясов.
    if formats is None:
        formats = ('%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S+00:00', '%Y-%m-%dT%H:%M:%S.%f+00:00')
    elif not isinstance(formats, (tuple, list)):
        formats = (formats, )

    if date_string:
        for fmt in formats:
            try:
                dt = datetime.datetime.strptime(date_string, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError
        return pytz.timezone('UTC').localize(dt).astimezone(tz=pytz.timezone(app.config.get('TIME_ZONE', 'Europe/Moscow'))).replace(tzinfo=None)
    else:
        return date_string


def safe_unicode(obj):
    if obj is None:
        return None
    return unicode(obj)


def safe_int(obj):
    if obj is None:
        return None
    return int(obj)


def safe_dict(obj):
    if obj is None:
        return None
    elif isinstance(obj, dict):
        for k, v in obj.iteritems():
            obj[k] = safe_dict(v)
        return obj
    elif hasattr(obj, '__json__'):
        return safe_dict(obj.__json__())
    return obj


def safe_datetime(val):
    if not val:
        return None
    if isinstance(val, basestring):
        try:
            val = string_to_datetime(val)
        except ValueError:
            try:
                val = string_to_datetime(val, '%Y-%m-%d')
            except ValueError:
                return None
        return val
    elif isinstance(val, datetime.datetime):
        return val
    elif isinstance(val, datetime.date):
        return datetime.datetime(val.year, val.month, val.day)
    else:
        return None


def safe_date(val):
    if not val:
        return None
    if isinstance(val, basestring):
        try:
            val = string_to_datetime(val)
        except ValueError:
            try:
                val = string_to_datetime(val, '%Y-%m-%d')
            except ValueError:
                return None
        return val.date()
    elif isinstance(val, datetime.datetime):
        return val.date()
    elif isinstance(val, datetime.date):
        return val
    else:
        return None


def safe_time_as_dt(val):
    if not val:
        return None
    if isinstance(val, basestring):
        for fmt in ('%H:%M:%S', '%H:%M'):
            try:
                val = datetime.datetime.strptime(val, fmt)
                break
            except ValueError:
                continue
        return val
    elif isinstance(val, datetime.datetime):
        return val
    else:
        return None


def safe_time(val):
    if not val:
        return None
    val = safe_time_as_dt(val)
    if isinstance(val, datetime.datetime):
        return val.time()
    else:
        return None


def safe_traverse(obj, *args, **kwargs):
    """Безопасное копание вглубь dict'а
    @param obj: точка входя для копания
    @param *args: ключи, по которым надо проходить
    @param default=None: возвращаемое значение, если раскопки не удались
    @rtype: any
    """
    default = kwargs.get('default', None)
    if obj is None:
        return default
    if len(args) == 0:
        raise ValueError(u'len(args) must be > 0')
    elif len(args) == 1:
        return obj.get(args[0], default)
    else:
        return safe_traverse(obj.get(args[0]), *args[1:], **kwargs)


def safe_traverse_attrs(obj, *args, **kwargs):
    default = kwargs.get('default', None)
    if obj is None:
        return default
    if len(args) == 0:
        raise ValueError(u'len(args) must be > 0')
    elif len(args) == 1:
        return getattr(obj, args[0], default)
    else:
        return safe_traverse_attrs(getattr(obj, args[0]), *args[1:], **kwargs)


def safe_bool(val):
    if isinstance(val, (str, unicode)):
        return val.lower() not in ('0', 'false', '\x00', '')
    return bool(val)


def safe_uuid(val):
    if not isinstance(val, basestring):
        return None
    u_obj = uuid.UUID(val)
    return u_obj


def safe_hex_color(val):
    if not isinstance(val, basestring):
        return None
    if val.startswith('#') and len(val) == 7:
        return val[1:]


def parse_json(json_string):
    try:
        result = json.loads(json_string)
    except ValueError:
        result = None
    return result


