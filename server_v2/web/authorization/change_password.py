#!/usr/bin/VtsAdminSignInHandler
# -*- coding: utf-8 -*-

'''
'''


from lib import *

@noXenSecureV1
class ChangePasswordHandler(tornado.web.RequestHandler, MongoMixin):

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
                if method == 1:
                    try:
                        # TODO: need to give validation
                        username = str(self.request.arguments['username'])
                        oldPassword = str(self.request.arguments['oldPassword'])
                    except Exception as e:
                        code = 4120
                        template = "Exception: {0}. Argument: {1!r}"
                        message = template.format(type(e).__name__, e.args)
                        raise Exception

                    try:
                        usernamePhone = long(username)
                        usernamePhone = 910000000000 + usernamePhone
                    except:
                        usernamePhone = None
                        message = 'Invalid Argument - [ username ].'
                        code = 4211
                        raise Exception

                    try:
                        newPaasword = str(self.request.arguments['newPassword'])
                    except Exception as e:
                        message = 'Invalid Argument - [ newPassword ].'
                        code = 4212
                        raise Exception

                    try:
                        account = yield self.account.find(
                                {
                                    'contact.0.value': usernamePhone
                                    # TODO: for email
                                    #'$or': [
                                    #    {
                                    #        'contact.0.value': usernamePhone
                                    #    },
                                    #    {
                                    #        'contact.1.value': username
                                    #    }
                                    #]
                                },
                                {
                                    '_id': 1
                                }
                            )
                        if len(account):
                            Log.i(account, 'eeeeeeeeeeeee')
                            '''
                                Saving the Last Sign In Reqested Time
                            '''
                            profile = yield self.profile.find_and_modify(
                                query = {
                                    'accountId': account[0]['_id'],
                                    'applicationId': app[0]['_id'],
                                    'entityId': self.entityId,
                                    'password': oldPassword
                                },
                                update = {
                                            '$set':
                                            {
                                                'lastSignInRequest': self.time,
                                                'password': newPaasword
                                            }
                                },
                                fields = {
                                    '_id': 1,
                                    'entityId': 1
                                }
                            )
                            if profile:
                                Log.i(profile)
                                self.profileId = profile['_id']
                                Log.i(self.profileId)
                                nOtp = randint(100000, 999999)
                                updateResult = yield self.oneTimePassword.update(
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
                                if updateResult['n']:
                                    Log.i('Phone Number: ', str(usernamePhone) + ' OTP: ' + str(nOtp))
                                    # TODO: this need to be chaged to http client
                                    gwResp = yield MSG91_GW.send(str(usernamePhone), str(entity[0]['smsGwId']), nOtp)
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
                                code = 4309
                                message = 'Wrong Password.'
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

