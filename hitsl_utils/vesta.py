# -*- coding: utf-8 -*-
import requests
import logging
from hitsl_utils.kladr import KladrLocality, KladrStreet

__author__ = 'viruzzz-kun'


# TODO Conform to Vesta v2 api (nVesta)


logger = logging.getLogger('VestaClient')
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())


class VestaException(Exception):
    message = 'Cannot connect to Vesta'


class Vesta(object):
    vesta_url = None

    def get(self, rb, code=None):
        if code:
            url = u'%s/api/v1/%s/%s' % (self.vesta_url, rb, code)
        else:
            url = u'%s/api/v1/%s' % (self.vesta_url, rb)
        return self._get(url)

    def _get(self, url):
        try:
            response = requests.get(url)
        except (requests.ConnectionError, requests.exceptions.MissingSchema, ValueError):
            raise VestaException(u'Невозможно связаться с подсистемой справочников')
        if response.status_code != 200:
            raise VestaException(u'Не удалось обработать запрос в подсистему справочников')
        return response.json().get('data')

    def _post(self, url, json):
        try:
            response = requests.post(url, json=json)
        except (requests.ConnectionError, requests.exceptions.MissingSchema, ValueError):
            raise VestaException(u'Невозможно связаться с подсистемой справочников')
        if response.status_code != 200:
            raise VestaException(u'Не удалось обработать запрос в подсистему справочников')
        return response.json().get('data')

    def get_kladr_locality(self, code):
        if len(code) == 13:  # убрать после конвертации уже записанных кодов кладр
            code = code[:-2]
        url = u'{0}/api/kladr/city/{1}/'.format(self.vesta_url, code)
        data = self._get(url)
        if not data:
            return KladrLocality(invalid=u'Не найден адрес в кладр по коду {0}'.format(code))
        return _make_kladr_locality(data[0])

    def get_kladr_locality_list(self, level, parent_code):
        if len(parent_code) == 13:  # убрать после конвертации уже записанных кодов кладр
            parent_code = parent_code[:-2]
        url = u'{0}/api/find/KLD172/'.format(self.vesta_url)
        data = self._post(url, {
            "level": level,
            "identparent": parent_code,
            "is_actual": "1"
        })

        if not data:
            return []
        return [
            KladrLocality(
                code=loc_info['identcode'],
                name=u'{0}. {1}'.format(loc_info['shorttype'], loc_info['name']),
                parent_code=loc_info['identparent']
            ) for loc_info in data
        ]

    def get_kladr_street(self, code):
        if len(code) == 17:  # убрать после конвертации уже записанных кодов кладр
            code = code[:-2]
        url = u'{0}/api/kladr/street/{1}/'.format(self.vesta_url, code)
        data = self._get(url)
        if not data:
            return KladrStreet(invalid=u'Не найдена улица в кладр по коду {0}'.format(code))
        return _make_kladr_street(data[0])

    def search_kladr_locality(self, query, limit=300):
        url = u'{0}/api/kladr/psg/search/{1}/{2}/'.format(self.vesta_url, query, limit)
        data = self._get(url)
        if not data:
            return []
        return map(_make_kladr_locality, data)

    def search_kladr_street(self, locality_code, query, limit=100):
        url = u'{0}/kladr/street/search/{1}/{2}/{3}/'.format(self.vesta_url, locality_code, query, limit)
        data = self._get(url)
        if not data:
            return []
        return map(_make_kladr_street, data)


class VestaExtension(Vesta):
    def __init__(self, app=None):
        super(VestaExtension, self).__init__()
        if app is None:
            self.app = None
            self.vesta_url = None
        else:
            self.init_app(app)

    def init_app(self, app):
        """
        :type app: flask.app.Flask
        :param app:
        :return:
        """
        self.app = app
        self.vesta_url = app.config.get('VESTA_URL', 'http://127.0.0.1:5002').rstrip('/')
        app.errorhandler(VestaException)(self._handle_vesta_exception)

    def _handle_vesta_exception(self, e):
        return u'Невозможно связаться с подсистемой справочников'


def _make_kladr_locality(loc_info):
    code = loc_info['identcode']
    name = u'{0}. {1}'.format(loc_info['shorttype'], loc_info['name'])
    level = loc_info['level']
    parents = map(_make_kladr_locality, loc_info.get('parents', []))
    return KladrLocality(code=code, name=name, level=level, parents=parents)


def _make_kladr_street(street_info):
    code = street_info['identcode']
    name = u'{0} {1}'.format(street_info['fulltype'], street_info['name'])
    return KladrStreet(code=code, name=name)
