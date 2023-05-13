#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('./utils')

import jwt, random
from .fernet_crypto import *
from .log_util import Log
from .time_util import timeNow
from bson.objectid import ObjectId

from .jwt_util import JWT_ENCODE, JWT_DECODE


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
                    handler.write()
                    handler.finish()

                #Authnotneeded = handler.request.headers.get('Authnotneeded')
                #if bool(Authnotneeded):
                #    return True
                    
                bearerToken = handler.request.headers.get('Authorization')
                
                if bearerToken:
                    bearerToken = str(bearerToken).split('Bearer ')
                    if len(bearerToken):
                        bearerToken = bearerToken[1]
                        print("bearerToken Orig=",bearerToken)
                        
                        #bearerToken= "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJnQUFBQUFCaTBzR1docnJHNjB1dEpEZ2JXR0FGMVRwYVgtQWZBVnBuMFhDM3I5WC0yd19jVmhVYjQ0MzVfNnFwcXpGQ0RhY3Q4dHlZUDJ5Q3B5S29JTzBYYU1UUzNubDJKM2s1dUtwSnE2Ni1VRUtnaG8xSG14RT0iLCJleHAiOjE2ODk1MTUyODZ9.-PjXKLQAp_WNcffNCBkAM67LjS8EokuHx4F1L4ceDtM"
                        #print('bearerToken After=',bearerToken)
                        accountId = JWT_DECODE(bearerToken)
                        print("accountId",accountId)
                        if not accountId:
                            Log.i('accountId not found ',bearerToken)
                            raise Exception('Authorization')
                        else:
                            handler.accountId = ObjectId(accountId.decode("utf-8"))
                            Log.i('Authorization', handler.accountId)
                    else:
                        Log.i('Bearer Token')
                        raise Exception('Bearer Token')
                       
                else:
                    handler._transforms = []
                    handler.set_status(501)
                    code = 4010
                    message = 'Missing - [ Authorization ]'
                    Log.i(message)
                    raise Exception(message)

                xOriginKey = handler.request.headers.get('x-Origin-Key')
                if xOriginKey:
                    print('xOriginKey',xOriginKey)
                    entityId = FN_DECRYPT(xOriginKey)
                    if not entityId:
                        Log.i('x-Origin-Key is not dicrypted')
                        raise Exception('x-Origin-Key')
                    else:
                        handler.entityId = ObjectId(entityId.decode("utf-8"))
                        Log.i('x-Origin-Key', handler.entityId)
                else:
                    handler._transforms = []
                    handler.set_status(501)
                    code = 4020
                    message = 'Missing - [ x-Origin-Key ].'
                    Log.i(message)
                    raise Exception(message)

                xApiKey = handler.request.headers.get('x-Api-Key')
                if xApiKey:
                    applicationId = FN_DECRYPT(xApiKey)
                    if not applicationId:
                        Log.i('x-Api-Key')
                        raise Exception('x-Api-Key')
                    else:
                        handler.applicationId = ObjectId(applicationId.decode("utf-8"))
                        Log.i('x-Api-Key', handler.applicationId)
                else:
                    handler._transforms = []
                    handler.set_status(501)
                    code = 4030
                    message = 'Missing - [ x-Api-Key ].'
                    Log.i(' Missing - [ x-Api-Key ].')
                    raise Exception
                #Newly added from class code
                

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

                response = {
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
                        handler.entityId = ObjectId(entityId.decode('utf-8'))
                        Log.i('x-Origin-Key', handler.entityId)
                else:
                    handler._transforms = []
                    handler.set_status(501)
                    code = 4020,
                    message = 'Missing - [ x-Origin-Key ].'
                    raise Exception

                return True
            except Exception as e:

                if code == 4000:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = exc_tb.tb_frame.f_code.co_filename
                    Log.d('No-Xen',
                          'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                    handler._transforms = []
                    handler.set_status(401)
                    code = 4001
                    message = 'Invalid headers.'

                response = {
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
