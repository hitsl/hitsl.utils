# -*- coding: utf-8 -*-
import blinker
import requests
from flask import request, redirect, json, session

__author__ = 'viruzzz-kun'


class CasError(Exception):
    pass


class CasNotAvailable(CasError):
    message = u'Castiel not available'


class CasExtension(object):
    """
    Extension for working with CAS Castiel
    """
    user_id_changed = blinker.Signal()

    def __init__(self, app=None):
        if app is None:
            self.cookie_name = 'CastielAuthToken'
            self.cas_external_address = 'http://127.0.0.1:5001/'
            self.cas_internal_address = self.cas_external_address
        else:
            self.init_app(app)
        self.app = app

    def init_app(self, app):
        """
        Install Extension at app
        :type app: flask.app.Flask
        :param app: Application
        :return:
        """
        self.cookie_name = app.config.get('CASTIEL_AUTH_COOKIE', 'CastielAuthToken')
        self.cas_external_address = app.config.get('CASTIEL_ADDRESS', 'http://127.0.0.1:5001/').rstrip('/')
        self.cas_internal_address = app.config.get('CASTIEL_ADDRESS_INTERNAL', self.cas_external_address)
        app.before_request(self._before_request)
        app.errorhandler(CasNotAvailable)(self._cas_not_available)

    def _before_request(self):
        if not (request.endpoint and 'static' not in request.endpoint and
                not getattr(self.app.view_functions[request.endpoint], 'is_public', False)):
            return
        token = request.cookies.get(self.cookie_name)
        if not token:
            return redirect(self.cas_external_address + '/cas/login')
        try:
            result = requests.post(
                self.cas_internal_address + '/cas/api/check',
                data=json.dumps({'token': token, 'prolong': True}),
                headers={'Referer': request.url.encode('utf-8')}
            )
        except requests.ConnectionError:
            raise CasNotAvailable

        answer = result.json()
        if not answer['success']:
            return redirect(self.cas_external_address + '/cas/login')

        user_id = answer['user_id']

        if user_id != session.get('user_id'):
            self.user_id_changed.send(self.app, old=session.get('cas_user_id'), new=user_id)
            session['cas_user_id'] = user_id

    def _cas_not_available(self, e):
        return u'Невозможно связаться с подсистемой централизованной аутентификации'
