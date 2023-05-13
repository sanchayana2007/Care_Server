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

    clinic_list  = MongoMixin.medicineDb[
                   CONFIG['database'][2]['table'][1]['name']
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

                # Signin Back
                if method == 0:
                    Log.i('Method 0 is not implemented')
                    pass
                #Account,Profile is present . Validate uisng OTP
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
                                result = {'Phone Number': str(phoneNumber) , 'OTP': str(nOtp)}
                                # TODO: this need to be chaged to http client
                                try:
                                    #gwResp = MSG91_GW.send(str(phoneNumber), str(entity[0]['smsGwId']), nOtp)
                                    gwResp = MSG91_GW.send('919886285077', str(entity[0]['smsGwId']), nOtp)
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

       
                    code = 4311
                    message = 'Unimplemented method : 2 '
                    
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
            print("self.entityId", self.entityId)
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
                        firstname = account[0]['firstName']
                        lastname = account[0]['lastName']
                        clinic= []

                        if app[0]['apiId'] == 502021:
                            print('account id fro clinic', account[0]['_id'])
                            clinicQ = self.clinic_list.find(
                                            {
                                                #'account_id': ObjectId(account[0]['_id']),
                                                'account_id': account[0]['_id'],
                                                
                                            },
                                            {   '_id': 1,
                                                    'verfiedClinic' : 1,  
                                                    'clinic_name':  1,
                                                    'clinic_type':  1  
                                          }, 
                                          limit =1
                                        )

                            async for r in clinicQ:
                                clinic.append(r)
                            
                            if  len(clinic):
                            
                                verifiedclinci = clinic[0]['verfiedClinic']  
                                clinic_name = clinic[0]['clinic_name']
                                clinic_type = clinic[0]['clinic_type']
                                clinic_id = str(clinic[0]['_id'])
                            Log.i("Clinic_id",clinic_id )
                            Log.i("clinic_type",clinic_type )
                            Log.i("verifiedclinci",verifiedclinci )
                            Log.i("clinic_name ",clinic_name )
                                                
                        
                        account_details= firstname+ lastname + str(phoneNumber)
                        print("Registerd user" ,account_details)

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
                                Log.i("###profileId",profileId)
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

                                        if app[0]['apiId'] == 502020:
                        
                                            result.append({'firstname': firstname, 'lastname':lastname,'phonenumber': phoneNumber})
                                        
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
            print("self.entityId", self.entityId)
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
                        firstname = account[0]['firstName']
                        lastname = account[0]['lastName']
                        clinic= []

                        if app[0]['apiId'] == 502021:
                            print('account id fro clinic', account[0]['_id'])
                            clinicQ = self.clinic_list.find(
                                            {
                                                #'account_id': ObjectId(account[0]['_id']),
                                                'account_id': account[0]['_id'],
                                                
                                            },
                                            {   '_id': 1,
                                                    'verfiedClinic' : 1,  
                                                    'clinic_name':  1,
                                                    'clinic_type':  1  
                                          }, 
                                          limit =1
                                        )

                            async for r in clinicQ:
                                clinic.append(r)
                            
                            if  len(clinic):
                            
                                verifiedclinci = clinic[0]['verfiedClinic']  
                                clinic_name = clinic[0]['clinic_name']
                                clinic_type = clinic[0]['clinic_type']
                                clinic_id = str(clinic[0]['_id'])
                            Log.i("Clinic_id",clinic_id )
                            Log.i("clinic_type",clinic_type )
                            Log.i("verifiedclinci",verifiedclinci )
                            Log.i("clinic_name ",clinic_name )
                                                
                        
                        account_details= firstname+ lastname + str(phoneNumber)
                        print("Registerd user" ,account_details)

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
                                Log.i("###profileId",profileId)
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

                                        if app[0]['apiId'] == 502020:
                        
                                            result.append({'firstname': firstname, 'lastname':lastname,'phonenumber': phoneNumber})
                                        
                                        
                                        elif app[0]['apiId'] == 502021:
                                            if phoneNumber == 911472583690 :

                                                result.append({'firstname': firstname, 'lastname':lastname,'phonenumber': phoneNumber , 'verfiedClinic': True,'clinic_name': clinic_name,'clinic_type': clinic_type,'clinic_id':clinic_id })
                                            else:
                                                result.append({'firstname': firstname, 'lastname':lastname,'phonenumber': phoneNumber , 'verfiedClinic': verifiedclinci,'clinic_name': clinic_name,'clinic_type': clinic_type,'clinic_id':clinic_id })

                                        else:
                                            print("Application ID is not supported", app[0]['apiId'] )
                                        
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
                            message = 'Wrong OTP provided , Please generate new one'
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
