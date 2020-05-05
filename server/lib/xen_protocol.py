#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('./utils')

import jwt, random
from fernet_crypto import *
from log_util import Log
from time_util import timeNow
from bson.objectid import ObjectId
SECRETS = [
        'IS-*HGJHFKJL^%&*O(PTDJFKGHJKRE%^UR&IT*O^(&P&TRYJFK^%^*&(*^*%%*^(^&O^*(*P(UYUFHGJLKKJGFHRTO&^*&YUTYII',
        'IS-%*^&*YUTIFUKGLH:GCMGV<JHB>KJNLKML&^*&(POUIOUGH<GKJLJKJHJFHG<GBJKL:TOO:IY>UGBJNMJJKJuBKMLFGHJ**UJH',
        'IS-%*^&*P(*F<HGBJHNKJLKLJJRTUYIUOIP&^%&*&(*(*&^&(*IPOJHJGJBJNKMLK:IUTYYIUOUO&*&(**^&%$#@$%$^%&^*&(*)',
        'IS-&%^$*&*(&$^&%O*^*P&YUTYFGHJOKIYUYTRTYUIOIYTYUFGHJKY^&(*$#!@#$%$^%&^*&(*)_)GUHIJOKPFCVBNM$^%&^*^&(',
        'IS-$*%^&(&^*{(*})(_TYGHJKLGFJHJKL%$^%&^*&(*)(&^&%^ERTFGYHJK^%$&^*&(*)(YTFYGHJK^%&*()(FGHJK&^$%%&^*&(',
        'IS-^$%&^*%&(*&({)(})_UYTIFHVBJNKMLK!@#$%^&*()POIUYGFVBNJKLP*&^%$%^&*()UYTFGHJK*&^%$^&*()UYTFGHJKL&^&',
        'IS-$#^%^&*()_)(YTGHUIOP{(*&^%$%^&*(OIUGFGHJKY#$%^&*()_IUYTFGHJKL!@#$%^&*()DFGHJKL@#$%^&*IOJHG@#RTY^^',
        'IS-!@#$%^&*()_IUYTREDFGHJIOPUY$#$%^&*(#$^%&^&**(&^%RTGYHJ@#$%^&*(*UYTRFGHJKL#$%^&U*()(*&^%TYU((^&*()',
        'IS-!@#$%^&*()OIUYTREDFGHNM@#$%^&OFDGGHJKYTR$%$^&*()(RTDFGHJKOU%$^%&^*&(&*&^%$#%$^%&^*&(*(*%$^%&^*&(*',
        'IS-#$%^&*()UYTRYUIOPHRE!@#$%^&*()_(*&^%$#@#$%^&*())(*&^%$#@#$%^&*(*&^%$#@!@#$%^&*(UYTRERTYUIOGFVBJKJ'
        ]
OPTIONS = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
        }

def JWT_ENCODE(payload = str):
    try:
        kyE = FN_ENCRYPT(payload)
        index = random.randint(0, len(SECRETS) - 1)
        kyEn = jwt.encode(
                {
                    'key': kyE,
                    'exp': dtime.datetime.utcnow() + dtime.timedelta(seconds=31536000L)
                },
                SECRETS[index],
                algorithm='HS256'
            )
        return kyEn
    except:
        return False

    return False


def JWT_DECODE(token = str):
    try:
        if len(SECRETS):
            for s in SECRETS:
                try:
                    tokenObj = jwt.decode(token, s, options=OPTIONS)
                    kyDe = FN_DECRYPT(tokenObj['key'])
                    if kyDe:
                        return kyDe
                except:
                    continue

    except:
        return False

    return False


def xenSecureV1(handler_class):
    """ Handle Xen Protocol """

    def wrap_execute(handler_execute):

        def require_auth(handler, kwargs):

            code = 4000
            status = False
            message = ''
            result = []

            try:
                handler.time = timeNow()
                handler.set_header('Xen-Protocol-Version', '1.0')
                requestCros = handler.request.headers.get('Origin')
                if requestCros != None:
                    handler.set_header('Access-Control-Allow-Origin', requestCros)
                requestHeader = handler.request.headers.get('Access-Control-Request-Headers')
                if requestHeader != None:
                    handler.set_header('Access-Control-Allow-Headers', requestHeader)
                    handler.set_header('Access-Control-Allow-Methods', 'DELETE,OPTIONS,GET,HEAD,PATCH,POST,PUT')
                    handler._transforms = []
                    handler.set_status(204)
                    handler.write
                    handler.finish()

                bearerToken = handler.request.headers.get('Authorization')
                if bearerToken:
                    bearerToken = str(bearerToken).split('Bearer ')
                    if len(bearerToken):
                        bearerToken = bearerToken[1]
                        accountId = JWT_DECODE(bearerToken)
                        if not accountId:
                            raise Exception('Authorization')
                        else:
                            handler.accountId = ObjectId(accountId)
                            Log.i('Authorization', handler.accountId)
                    else:
                        raise Exception('Bearer Token')
                else:
                    handler._transforms = []
                    handler.set_status(501)
                    code = 4010
                    message = 'Missing - [ Authorization ]'
                    raise Exception

                xOriginKey = handler.request.headers.get('x-Origin-Key')
                if xOriginKey:
                    entityId = FN_DECRYPT(xOriginKey)
                    if not entityId:
                        raise Exception('x-Origin-Key')
                    else:
                        handler.entityId = ObjectId(entityId)
                        Log.i('x-Origin-Key', handler.entityId)
                else:
                    handler._transforms = []
                    handler.set_status(501)
                    code = 4020,
                    message = 'Missing - [ x-Origin-Key ].'
                    raise Exception

                xApiKey = handler.request.headers.get('x-Api-Key')
                if xApiKey:
                    applicationId = FN_DECRYPT(xApiKey)
                    if not applicationId:
                        raise Exception('x-Api-Key')
                    else:
                        handler.applicationId = ObjectId(applicationId)
                        Log.i('x-Api-Key', handler.applicationId)
                else:
                    handler._transforms = []
                    handler.set_status(501)
                    code = 4030,
                    message = 'Missing - [ x-Api-Key ].'
                    raise Exception

                return True
            except Exception as e:

                if code == 4000:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = exc_tb.tb_frame.f_code.co_filename
                    Log.d('Xen', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                    handler._transforms = []
                    handler.set_status(401)
                    code = 4001
                    message = 'Invalid headers.'

                response =  {
                                'code': code,
                                'status': status,
                                'result': [],
                                'message': message
                            }
                Log.d('Xen', response)
                handler.write(response)
                handler.finish()

            return False

        def _execute(self, transforms, *args, **kwargs):
            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class


def noXenSecureV1(handler_class):
    """ Handle No-Xen Protocol """

    def wrap_execute(handler_execute):

        def require_auth(handler, kwargs):

            code = 4000
            status = False
            result = []
            message = ''

            try:
                handler.time = timeNow()
                handler.set_header('No-Xen-Protocol-Version', '1.0')
                requestCros = handler.request.headers.get('Origin')
                if requestCros != None:
                    handler.set_header('Access-Control-Allow-Origin', requestCros)
                requestHeader = handler.request.headers.get('Access-Control-Request-Headers')
                if requestHeader != None:
                    handler.set_header('Access-Control-Allow-Headers', requestHeader)
                    handler.set_header('Access-Control-Allow-Methods', 'DELETE,GET,HEAD,PATCH,POST,PUT')
                    handler._transforms = []
                    handler.set_status(204)
                    handler.write
                    handler.finish()
                xOriginKey = handler.request.headers.get('x-Origin-Key')
                if xOriginKey:
                    entityId = FN_DECRYPT(xOriginKey)
                    if not entityId:
                        raise Exception('x-Origin-Key')
                    else:
                        handler.entityId = ObjectId(entityId)
                        Log.i('x-Origin-Key', handler.entityId)
                else:
                    handler._transforms = []
                    handler.set_status(501)
                    code  = 4020,
                    message = 'Missing - [ x-Origin-Key ].'
                    raise Exception

                return True
            except Exception as e:

                if code == 4000:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = exc_tb.tb_frame.f_code.co_filename
                    Log.d('No-Xen', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                    handler._transforms = []
                    handler.set_status(401)
                    code = 4001
                    message = 'Invalid headers.'


                response =  {
                                'code': code,
                                'status': status,
                                'result': [],
                                'message': message
                            }
                Log.d('No-Xen', response)
                handler.write(response)
                handler.finish()

            return False

        def _execute(self, transforms, *args, **kwargs):
            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class

