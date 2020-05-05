#!/usr/bin/VtsAdminSignInHandler
# -*- coding: utf-8 -*-

'''
'''


from lib import *

@noXenSecureV1
class SignInHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('POST')

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


    @defer.inlineCallbacks
    def post(self):
        status = False
        code = 4000
        result = []
        message = ''
        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body)
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception

            entity = yield self.entity.find(
                                {
                                    '_id': self.entityId
                                },
                                limit=1
                            )
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
            app = yield self.applications.find(
                    {
                        'applicationId': applicationId
                    },
                    limit=1
                )
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
                        usernamePhone = long(username)
                    except:
                        usernamePhone = None

                    try:
                        account = yield self.account.find(
                                {
                                    'privacy.0.value': password,
                                    '$or': [
                                        {
                                            'contact.0.value': usernamePhone
                                        },
                                        {
                                            'contact.1.value': username
                                        }
                                    ]
                                },
                                {
                                    '_id': 1
                                },
                                limit=1
                            )
                        if len(account):
                            '''
                                Searching for profile
                                Blocked for 20 sec ( in microseconds )
                            '''
                            profile = yield self.profile.find(
                                {
                                    'accountId': account[0]['_id'],
                                    'applicationId': app[0]['_id'],
                                    '$or': [
                                        {
                                            'lastSignInRequest': None
                                        },
                                        {
                                            'lastSignInRequest':
                                            {
                                                '$lt': self.time - 20000000
                                            }
                                        }
                                    ]
                                },
                                {
                                    '_id': 1,
                                    'entityId': 1
                                },
                                limit=1
                            )
                            if len(profile) and profile:
                                entities = []
                                for p in profile:
                                    ent = yield self.entity.find(
                                                {
                                                    '_id': p['entityId']
                                                },
                                                {
                                                    '_id': 1,
                                                    'name': 1
                                                },
                                                limit=1
                                            )
                                    if len(ent):
                                        k = FN_ENCRYPT(str(ent[0]['_id']))
                                        v = {
                                                'key': k,
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
                                    updateResult = yield self.profile.update(
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
                                    if updateResult['n']:
                                        secureCache = {
                                            'bearerToken': JWT_ENCODE(
                                                str(account[0]['_id'])
                                                ),
                                            'apiKey': FN_ENCRYPT(str(app[0]['_id']))
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
                        Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                        code = 5210
                        message = 'Internal Error, Please Contact the Support Team.'
                        # TODO: for sign in with email
                        raise Exception
                        account = yield self.account.find(
                                {
                                    'contact.1.value': userName,
                                    'privacy.0.value': password
                                },
                                limit=1
                            )
                        if len(account):
                            profile = yield self.profile.find(
                                {
                                    'accountId': account[0]['_id'],
                                    'applicationId': app[0]['_id']
                                }
                            )
                            if len(profile):
                                entities = []
                                for p in profile:
                                    ent = yield self.entity.find(
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
                                            JWT_ENCODE(
                                                    str(account[0]['_id'])
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
                            phoneNumber = long(phoneNumber)
                        countryCode = self.request.arguments.get('countryCode')
                        if countryCode == None:
                            code = 4251
                            message = 'Missing Argument - [ countryCode ].'
                            raise Exception
                        else:
                            countryCode = int(countryCode)
                        country = yield self.phoneCountry.find(
                                    {
                                        'code': countryCode
                                    },
                                    limit=1
                                )
                        if not len(country):
                            code = 4242
                            message = 'Invalid Country Code.'
                            raise Exception
                        if len(str(phoneNumber)) != country[0]['telMaxLength']:
                            code = 4252
                            message = 'Invalid Phone Number.'
                            raise Exception('phoneNumber')
                        else:
                            phoneNumber = long(str(countryCode) + str(phoneNumber))
                    except Exception as e:
                        if not len(message):
                            code = 4210
                            template = "Exception: {0}. Argument: {1!r}"
                            message = template.format(type(e).__name__, e.args)
                        raise Exception
                    account = yield self.account.find(
                                    {
                                        'contact.0.value': phoneNumber
                                    },
                                    {
                                        '_id': 1
                                    },
                                    limit=1
                                )
                    if len(account):
                        '''
                            Searching for profile
                            Blocked for 20 sec ( in microseconds )
                        '''
                        profile = yield self.profile.find(
                                    {
                                        'accountId': account[0]['_id'],
                                        'applicationId': app[0]['_id'],
                                        '$or': [
                                            {
                                                'lastSignInRequest': None
                                            },
                                            {
                                                'lastSignInRequest':
                                                {
                                                    '$lt': self.time - 20000000
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        '_id': 1
                                    },
                                    limit=1
                                )
                        if not len(profile):
                            if not app[0]['selfRegister']:
                                code = 4210
                                message = 'Phone Number is not registered.'
                                raise Exception
                            try:
                                profileId = yield self.profile.insert(
                                    {
                                        'active': False,
                                        'locked': False,
                                        'closed': False,
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
                        oOtp = yield self.oneTimePassword.find(
                                        {
                                            'profileId': profileId,
                                        },
                                        {
                                            '_id': 1
                                        },
                                        limit=1
                                    )
                        nOtp = randint(100000, 999999)
                        if (yield self.oneTimePassword.remove({'profileId': profileId})):
                            yield self.oneTimePassword.insert(
                                    {
                                        'createdAt': dtime.now(),
                                        'profileId': profileId,
                                        'value': nOtp
                                    }
                                )
                            '''
                                Saving the Last Sign In Reqested Time
                            '''
                            updateResult = yield self.profile.update(
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
                            if updateResult['n']:
                                Log.i('Phone Number: ', str(phoneNumber) + ' OTP: ' + str(nOtp))
                                # TODO: this need to be chaged to http client
                                gwResp = yield MSG91_GW.send(str(phoneNumber), str(entity[0]['smsGwId']), nOtp)
                                if gwResp:
                                #if True:
                                    Log.i('MSG91 Gateway Response', gwResp)
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
                            code = 5010
                            message = 'Internal Error, Please Contact the Support Team.'
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
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error, Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
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
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return

