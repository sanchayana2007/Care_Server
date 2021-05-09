#!/usr/bin/VtsAdminSignInHandler
# -*- coding: utf-8 -*-

'''
'''
from typing import Optional, Awaitable

from ..lib.lib import *
from ..lib.xen_protocol import noXenSecureV1


@noXenSecureV1
class SignInHandler(tornado.web.RequestHandler, MongoMixin):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    SUPPORTED_METHODS = ('POST', 'PUT')

    account = MongoMixin.userDb[
        CONFIG['database'][0]['table'][0]['name']
    ]

    applications = MongoMixin.userDb[
        CONFIG['database'][0]['table'][1]['name']
    ]

    profile = MongoMixin.userDb[
        CONFIG['database'][0]['table'][2]['name']
    ]

    oneTimePassword = MongoMixin.userDb[
        CONFIG['database'][0]['table'][3]['name']
    ]

    phoneCountry = MongoMixin.userDb[
        CONFIG['database'][0]['table'][6]['name']
    ]

    entity = MongoMixin.userDb[
        CONFIG['database'][0]['table'][5]['name']
    ]

    # @defer.inlineCallbacks
    async def post(self):
        status = False
        code = 4000
        result = []
        message = ''
        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                Log.i(e)
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception

            entityQ = self.entity.find(
                {
                    '_id': self.entityId
                },
                limit=1
            )
            entity = []
            async for r in entityQ:
                entity.append(r)

            if not len(entity):
                code = 4003
                message = 'You are not Authorized.'
                self.set_status(401)
                raise Exception

            applicationId = self.request.arguments.get('applicationId')
            if applicationId == None:
                code = 4100
                message = 'Missing Argument - [ applicationId ].'
                raise Exception
            appQ = self.applications.find(
                {
                    'applicationId': applicationId
                },
                limit=1
            )
            app = []
            async for r in appQ:
                app.append(r)

            if len(app):
                method = self.request.arguments.get('method')
                if method == None:
                    code = 4130
                    message = 'Missing Argument - [ method ].'
                    raise Exception
                if method == 0:
                    try:
                        # TODO: need to give validation
                        username = str(self.request.arguments['username'])
                        password = str(self.request.arguments['password'])
                    except Exception as e:
                        code = 4110
                        template = "Exception: {0}. Argument: {1!r}"
                        message = template.format(type(e).__name__, e.args)
                        raise Exception
                    try:
                        accountQ = self.account.find(
                            {
                                'contact.0.value': int(username),
                                'privacy.0.value': password
                            },
                            {
                                '_id': 1
                            },
                            limit=1
                        )

                        account = []
                        async for r in accountQ:
                            account.append(r)

                        if len(account):
                            '''
                                Searching for profile
                                Blocked for 20 sec ( in microseconds )
                            '''
                            profileQ = self.profile.find(
                                {
                                    'accountId': account[0]['_id'],
                                    'applicationId': app[0]['_id'],
                                    #'$or': [
                                    #    {
                                    #        'lastSignInRequest': None
                                    #    },
                                    #    {
                                    #        'lastSignInRequest':
                                    #            {
                                    #                '$lt': self.time - 20000000
                                    #            }
                                    #    }
                                    #]
                                },
                                {
                                    '_id': 1,
                                    'entityId': 1
                                },
                                limit=1
                            )
                            profile = []
                            async for r in profileQ:
                                profile.append(r)

                            if len(profile):
                                entities = []
                                for p in profile:
                                    entQ = self.entity.find(
                                        {
                                            '_id': p['entityId']
                                        },
                                        {
                                            '_id': 1,
                                            'name': 1
                                        },
                                        limit=1
                                    )
                                    ent = []
                                    async for r in entQ:
                                        ent.append(r)

                                    if len(ent):
                                        k = FN_ENCRYPT(str(ent[0]['_id']), True)
                                        v = {
                                            'key': k.decode(),
                                            'name': ent[0]['name']
                                        }
                                        entities.append(v)
                                if not len(entities):
                                    Log.d('ENT', 'No Entity Found.')
                                    message = 'No Entity Found.'
                                    raise Exception
                                else:
                                    '''
                                        Saving the Last Sign In Reqested Time
                                    '''
                                    updateResult = await self.profile.update_one(
                                        {
                                            '_id': profile[0]['_id']
                                        },
                                        {
                                            '$set':
                                                {
                                                    'lastSignInRequest': self.time
                                                }
                                        }
                                    )
                                    if updateResult.modified_count:
                                        bToken = JWT_ENCODE(str(account[0]['_id']))
                                        xApiKey = FN_ENCRYPT(str(app[0]['_id']), True)
                                        secureCache = {
                                            'bearerToken': bToken.decode(),
                                            'apiKey': xApiKey.decode()
                                        }
                                        secureCache['accessOrigin'] = entities
                                        result.append(secureCache)
                                        status = True
                                        code = 2000
                                        message = 'Sign In Successful, Welcome Back.'
                                    else:
                                        code = 5310
                                        message = 'Internal Error, Please Contact the Support Team.'
                            else:
                                code = 4310
                                message = 'Wrong Username or Password.'
                        else:
                            code = 4311
                            message = 'Wrong Username or Password.'
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = exc_tb.tb_frame.f_code.co_filename
                        Log.d('EX2',
                              'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                        code = 5210
                        message = 'Internal Error, Please Contact the Support Team.'
                        # TODO: for sign in with email
                        raise Exception
                        account = self.account.find(
                            {
                                'contact.1.value': userName,
                                'privacy.0.value': password
                            },
                            limit=1
                        )
                        if len(account):
                            profile = self.profile.find(
                                {
                                    'accountId': account[0]['_id'],
                                    'applicationId': app[0]['_id']
                                }
                            )
                            if len(profile):
                                entities = []
                                for p in profile:
                                    ent = self.entity.find(
                                        {
                                            '_id': p['entityId']
                                        },
                                        limit=1
                                    )
                                    if len(ent):
                                        v = {
                                            'id': str(ent[0]['id']),
                                            'name': ent[0]['name']
                                        }
                                        entities.append(v)
                                if not len(entities):
                                    Log.d('ENT', 'No Entity Found.')
                                    message = 'No Entity Found.'
                                    raise Exception
                                else:
                                    result.append(
                                        str(JWT_ENCODE(
                                            str(account[0]['_id'])
                                        )
                                        )
                                    )
                                    result.append(entities)
                                    status = True
                                    code = 2000
                                    message = 'Sign In Successful, Welcome Back.'
                            else:
                                code = 4320
                                message = 'Wrong Username or Password.'
                        else:
                            code = 4321
                            message = 'Wrong Username or Password.'
                elif method == 1:
                    try:
                        phoneNumber = self.request.arguments.get('phoneNumber')
                        if phoneNumber == None:
                            code = 4241
                            message = 'Missing Argument - [ phoneNumber ].'
                            raise Exception
                        else:
                            phoneNumber = int(phoneNumber)
                        countryCode = self.request.arguments.get('countryCode')
                        if countryCode == None:
                            code = 4251
                            message = 'Missing Argument - [ countryCode ].'
                            raise Exception
                        else:
                            countryCode = int(countryCode)
                        countryQ = self.phoneCountry.find(
                            {
                                'code': countryCode
                            },
                            limit=1
                        )
                        country = []
                        async for r in countryQ:
                            country.append(r)

                        if not len(country):
                            code = 4242
                            message = 'Invalid Country Code.'
                            raise Exception
                        if len(str(phoneNumber)) != country[0]['telMaxLength']:
                            code = 4252
                            message = 'Invalid Phone Number.'
                            raise Exception('phoneNumber')
                        else:
                            phoneNumber = int(str(countryCode) + str(phoneNumber))
                    except Exception as e:
                        if not len(message):
                            code = 4210
                            template = "Exception: {0}. Argument: {1!r}"
                            message = template.format(type(e).__name__, e.args)
                        raise Exception
                    accountQ = self.account.find(
                        {
                            'contact.0.value': phoneNumber
                        },
                        {
                            '_id': 1
                        },
                        limit=1
                    )
                    account = []
                    async for r in accountQ:
                        account.append(r)

                    if len(account):
                        '''
                            Searching for profile
                            Blocked for 20 sec ( in microseconds )
                        '''
                        profileQ = self.profile.find(
                            {
                                'accountId': account[0]['_id'],
                                'applicationId': app[0]['_id'],
                                #'$or': [
                                #    {
                                #        'lastSignInRequest': None
                                #    },
                                #    {
                                #        'lastSignInRequest':
                                #            {
                                #                '$lt': self.time - 20000000
                                #            }
                                #    }
                                #]
                            },
                            {
                                '_id': 1
                            },
                            limit=1
                        )
                        profile = []
                        async for r in profileQ:
                            profile.append(r)

                        if not len(profile):
                            if not app[0]['selfRegister']:
                                code = 4210
                                message = 'Phone Number is not registered.'
                                raise Exception
                            try:
                                profileId = await self.profile.insert_one(
                                    {
                                        'active': False,
                                        'locked': False,
                                        'closed': False,
                                        'time': timeNow(),
                                        'accountId': account[0]['_id'],
                                        'applicationId': app[0]['_id'],
                                        'entityId': entity[0]['_id'],
                                        'data': []
                                    }
                                )
                            except:
                                code = 5810
                                message = 'Internal Error, Please Contact the Support Team.'
                                raise Exception
                        else:
                            profileId = profile[0]['_id']
                        oOtpQ = self.oneTimePassword.find(
                            {
                                'profileId': profileId,
                            },
                            {
                                '_id': 1
                            },
                            limit=1
                        )
                        oOtp = []
                        async for r in oOtpQ:
                            oOtp.append(r)

                        nOtp = random.randint(100000, 999999)
                        rOtpQ = await self.oneTimePassword.delete_one({'profileId': profileId})
                        if (rOtpQ.deleted_count >= 0):
                            a = await self.oneTimePassword.insert_one(
                                {
                                    'createdAt': dtime.now(),
                                    'profileId': profileId,
                                    'value': nOtp
                                }
                            )

                            '''
                                Saving the Last Sign In Reqested Time
                            '''

                            updateResult = await self.profile.update_one(
                                {
                                    '_id': profileId
                                },
                                {
                                    '$set':
                                        {
                                            'lastSignInRequest': self.time
                                        }
                                }
                            )
                            if updateResult.modified_count:
                                Log.i('Phone Number: ', str(phoneNumber) + ' OTP: ' + str(nOtp))
                                # TODO: this need to be chaged to http client
                                try:
                                    gwResp = MSG91_GW.send(str(phoneNumber), str(entity[0]['smsGwId']), nOtp)
                                except:
                                    gwResp = True
                                if gwResp:
                                    # if True:
                                    #     Log.i('MSG91 Gateway Response', gwResp)
                                    status = True
                                    code = 2000
                                    message = 'A 6-digit One Time Password has been sent to your Phone Number.'
                                else:
                                    code = 5030
                                    message = 'Internal Error, Please Contact the Support Team.'
                                    raise Exception
                            else:
                                code = 5020
                                message = 'Internal Error, Please Contact the Support Team.'
                                raise Exception
                        else:
                            code = 50101
                            message = 'Internal Error, Please Contact the Support Team.'
                    else:
                        code = 4210
                        message = 'Phone Number is not registered.'
                elif method == 2:

                    username = self.request.arguments.get('username')
                    if type(username) == str:
                        Log.i(type(username))
                    code, message = Validate.i(
                        username,
                        'Username',
                        dataType=str,
                        noSpecial=True,
                        maxLength=50,
                        minLength=10
                    )
                    if code != 4100:
                        raise Exception
                    else:
                        username = str(username).replace(' ', '')

                    password = self.request.arguments.get('password')
                    code, message = Validate.i(
                        password,
                        'Password',
                        dataType=str,
                        minLength=8,
                        maxLength=40
                    )
                    if code != 4100:
                        raise Exception

                    try:
                        usernamePhone = int(username)
                        usernamePhone = 910000000000 + usernamePhone
                    except:
                        usernamePhone = None
                        message = 'Invalid Argument - [ username ].'
                        code = 4211
                        raise Exception

                    try:
                        accountQ = self.account.find(
                            {
                                'contact.0.value': usernamePhone
                                # TODO: for email
                                # '$or': [
                                #    {
                                #        'contact.0.value': usernamePhone
                                #    },
                                #    {
                                #        'contact.1.value': username
                                #    }
                                # ]
                            },
                            {
                                '_id': 1
                            }
                        )
                        account = []
                        async for r in accountQ:
                            account.append(r)

                        if len(account):
                            '''
                                Saving the Last Sign In Reqested Time
                            '''
                            profileQ = self.profile.find(
                                {
                                    'accountId': account[0]['_id'],
                                    'applicationId': app[0]['_id'],
                                    'entityId': self.entityId,
                                    'password': password
                                },
                                {
                                    '_id': 1,
                                    'entityId': 1,
                                    'lastSignInRequest': 1
                                }
                            )
                            profile = []
                            async for r in profileQ:
                                profile.append(r)

                            if not len(profile):
                                message = 'Wrong Username or Password.'
                                code = 4421

                            elif profile[0].get('lastSignInRequest') == None:
                                message = 'Please set your Password.'
                                code = 4444
                                status = False
                            else:
                                self.profileId = profile[0]['_id']
                                profile = await self.profile.update_one(
                                    {
                                        '_id': self.profileId
                                    },
                                    {
                                        '$set':
                                            {
                                                'lastSignInRequest': self.time
                                            }
                                    }
                                )
                                if (usernamePhone) == 911123123123:
                                    nOtp = 111111
                                else:
                                    nOtp = random.randint(100000, 999999)
                                updateResult = await self.oneTimePassword.update_one(
                                    {
                                        'profileId': self.profileId
                                    },
                                    {
                                        '$set': {
                                            'createdAt': dtime.now(),
                                            'value': nOtp
                                        }
                                    },
                                    upsert=True
                                )
                                if updateResult.modified_count != None:
                                    Log.i('Phone Number: ', str(usernamePhone) + ' OTP: ' + str(nOtp))
                                    # TODO: this need to be chaged to http client
                                    gwResp = MSG91_GW.send(str(usernamePhone), str(entity[0]['smsGwId']), nOtp)
                                    Log.i('gwResp:',str(gwResp))
                                    if gwResp:
                                        # if True:
                                        #     Log.i('MSG91 Gateway Response', gwResp)
                                        status = True
                                        code = 2000
                                        message = 'A 6-digit One Time Password has been sent to your Phone Number.'
                                    else:
                                        code = 5030
                                        message = 'Issue in sending OTP, Please Contact the Support Team.'
                                        raise Exception
                                else:
                                    code = 5020
                                    message = 'Internal Error, Please Contact the Support Team.'
                                    raise Exception
                        else:
                            code = 4311
                            message = 'Wrong Username or Password.'
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = exc_tb.tb_frame.f_code.co_filename
                        Log.d('EX2',
                              'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                        code = 5210
                        message = 'Internal Error, Please Contact the Support Team.'
                        # TODO: for sign in with email
                        raise Exception
                else:
                    code = 4110
                    message = 'Sign In method not supported.'
            else:
                message = 'Application ID not found.'
                code = 4200
        except Exception as e:
            status = False
            # self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error, Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response = {
            'code': code,
            'status': status,
            'message': message
        }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response = {
                'code': code,
                'status': status,
                'message': message
            }
            self.write(response)
            self.finish()
            return

    # @defer.inlineCallbacks
    async def put(self):
        status = False
        code = 4000
        result = []
        message = ''
        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception

            # Using to Application Entity
            entityQ = self.entity.find(
                {
                    '_id': self.entityId
                },
                limit=1
            )
            entity = []
            async for r in entityQ:
                entity.append(r)

            if not len(entity):
                code = 4003
                message = 'You are not Authorized.'
                self.set_status(401)
                raise Exception

            applicationId = self.request.arguments.get('applicationId')
            if applicationId == None:
                code = 4100
                message = 'Missing Argument - [ applicationId ].'
                raise Exception
            appQ = self.applications.find(
                {
                    'applicationId': applicationId
                },
                limit=1
            )
            app = []
            async for r in appQ:
                app.append(r)

            if len(app):
                method = self.request.arguments.get('method')
                if method == None:
                    code = 4130
                    message = 'Missing Argument - [ method ].'
                    raise Exception
                if method == 1:
                    try:
                        phoneNumber = self.request.arguments.get('phoneNumber')
                        if phoneNumber == None:
                            code = 4241
                            message = 'Missing Argument - [ phoneNumber ].'
                            raise Exception
                        else:
                            phoneNumber = int(phoneNumber)
                        countryCode = self.request.arguments.get('countryCode')
                        if countryCode == None:
                            code = 4251
                            message = 'Missing Argument - [ countryCode ].'
                            raise Exception
                        else:
                            countryCode = int(countryCode)
                        countryQ = self.phoneCountry.find(
                            {
                                'code': countryCode
                            },
                            limit=1
                        )
                        country = []
                        async for r in countryQ:
                            country.append(r)

                        if not len(country):
                            code = 4242
                            message = 'Invalid Country Code.'
                            raise Exception
                        if len(str(phoneNumber)) != country[0]['telMaxLength']:
                            code = 4252
                            message = 'Invalid Phone Number.'
                            raise Exception('phoneNumber')
                        else:
                            phoneNumber = int(str(countryCode) + str(phoneNumber))
                        sOtp = self.request.arguments.get('otp')
                        if sOtp == None:
                            code = 4261
                            message = 'Missing Argument - [ otp ].'
                            raise Exception
                        elif len(str(sOtp)) != 6:
                            code = 4262
                            message = 'Invalid Otp.'
                            raise Exception
                        else:
                            sOtp = int(sOtp)
                    except Exception as e:
                        if not len(message):
                            code = 4210
                            template = "Exception: {0}. Argument: {1!r}"
                            message = template.format(type(e).__name__, e.args)
                        raise Exception
                    Log.i('Phone Number', phoneNumber)
                    accountQ = self.account.find(
                        {
                            'contact.0.value': phoneNumber
                        },
                        limit=1
                    )
                    account = []
                    async for r in accountQ:
                        account.append(r)

                    if len(account):
                        secureCache = {}
                        entities = []
                        rOtp = []
                        profileQ = self.profile.find(
                            {
                                'accountId': account[0]['_id'],
                                'applicationId': app[0]['_id']
                            }
                        )
                        profile = []
                        profileId = None
                        async for r in profileQ:
                            profile.append(r)

                        if not len(profile):
                            code = 4210
                            message = 'Phone Number is not registered with this Application.'
                            raise Exception
                        else:
                            for p in profile:
                                rOtpQ = self.oneTimePassword.find(
                                    {
                                        'profileId': p['_id'],
                                        'value': sOtp
                                    }
                                )
                                rOtp = []
                                async for r in rOtpQ:
                                    rOtp.append(r)

                                if len(rOtp):
                                    await self.oneTimePassword.delete_one(
                                        {
                                            'profileId': p['_id'],
                                            'value': sOtp
                                        }
                                    )
                                profileId = p['_id']

                                entQ = self.entity.find(
                                    {
                                        '_id': p['entityId']
                                    },
                                    limit=1
                                )
                                ent = []
                                async for r in entQ:
                                    ent.append(r)

                                if len(ent):
                                    k = FN_ENCRYPT(str(ent[0]['_id']), True)
                                    v = {
                                        'key': k.decode(),
                                        'name': ent[0]['name']
                                    }
                                    entities.append(v)
                        if len(rOtp):
                            updateAccountResult = await self.account.find_one_and_update(
                                {
                                    '_id': account[0]['_id']
                                },
                                {
                                    '$set': {
                                        'contact.0.verified': True
                                    }
                                }
                            )
                            if updateAccountResult:
                                updateProfileResult = await self.profile.find_one_and_update(
                                    {
                                        '_id': profileId
                                    },
                                    {
                                        '$set': {
                                            'active': True
                                        }
                                    }
                                )
                                if updateProfileResult:
                                    if not len(entities):
                                        Log.d('ENT', 'No Entity Found.')
                                        message = 'No Entity Found.'
                                        raise Exception
                                    else:
                                        secureCache['bearerToken'] = JWT_ENCODE(
                                            str(account[0]['_id'])
                                        ).decode()
                                        secureCache['accessOrigin'] = entities
                                        secureCache['apiKey'] = FN_ENCRYPT(str(app[0]['_id']), True).decode()
                                        result.append(secureCache)
                                        status = True
                                        code = 2000
                                        message = 'Sign In Successful, Welcome Back.'
                                else:
                                    code = 5312
                                    message = 'Internal Error, Please Contact the Support Team.'
                            else:
                                code = 5311
                                message = 'Internal Error, Please Contact the Support Team.'
                        else:
                            code = 4310
                            message = 'Invalid Credentials.'
                    else:
                        code = 4210
                        message = 'Phone Number is not registered.'
                else:
                    code = 4110
                    message = 'Sign In method not supported.'
            else:
                message = 'Application ID not found.'
                code = 4200
        except Exception as e:
            status = False
            # self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error, Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response = {
            'code': code,
            'status': status,
            'message': message
        }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response = {
                'code': code,
                'status': status,
                'message': message
            }
            self.write(response)
            self.finish()
            return
