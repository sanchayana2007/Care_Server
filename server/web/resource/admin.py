#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    1.  VtsVehicleHandler
        Type: Class
        Methods:
            A.GET:
                Get all vehicle  details under that entity
                Line: 39
            B.POST:
                Will create new row vehicles
                Line: 162
            C.PUT:
                Update Vehicle details on vehicles.
                Line: 335
            D:DELETE:
                Delete the Vehicle from Vehicles.
                Line: 523
'''


from lib import *

@xenSecureV1
class AdminHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE','PUT')

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]

    vehicleCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][1]['name']
                ]

    vehicleSubCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
                ]

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # TODO: this need to be moved in a global class
            profile = yield self.profile.find(
                            {
                                'accountId': self.accountId,
                                'applicationId': self.applicationId,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
            print profile
            if len(profile):
                app = yield self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            limit=1
                        )
                if len(app):
                    if app[0]['apiId'] == 502022: # TODO: till here
                        self.apiId = app[0]['apiId']
                        Log.i(self.apiId)
                        profileApplication = yield self.applications.find(
                            {
                                'apiId': 502022,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
                        if not len(profileApplication):
                            raise Exception
                        else:
                            profileApplicationId = profileApplication[0]['_id']

                        try:
                            aClosed = bool(int(self.get_arguments('closed')[0]))
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ closed ].'
                            raise Exception

                        try:
                            profileId = ObjectId(self.get_arguments('id')[0])
                        except:
                            profileId = None
                        if profileId != None:
                            aProfile = yield self.profile.find(
                                {
                                    '_id': profileId,
                                    'closed': aClosed,
                                    'entityId': self.entityId,
                                    'applicationId': profileApplicationId
                                },
                                limit=1
                            )
                            if len(aProfile):
                                pAccount = yield self.account.find(
                                            {
                                                '_id': aProfile[0]['accountId']
                                            },
                                            limit=1
                                        )
                                if len(pAccount):
                                    v = {}
                                    v['closed'] = aProfile[0]['closed']
                                    v['locked'] = aProfile[0]['locked']
                                    v['active'] = aProfile[0]['active']
                                    v['id'] = str(aProfile[0].get('_id'))
                                    v['firstName'] = pAccount[0].get('firstName')
                                    v['lastName'] = pAccount[0].get('lastName')
                                    v['contact'] = pAccount[0].get('contact')
                                    pServiceAccount = yield self.serviceAccount.find(
                                                {
                                                    'profileId': aProfile[0]['_id'],
                                                    'entityId': self.entityId
                                                },
                                                limit=1
                                            )
                                    if len(pServiceAccount):
                                        v['firstName'] = pServiceAccount[0].get('firstName')
                                        v['lastName'] = pServiceAccount[0].get('lastName')
                                    result.append(v)
                                else:
                                    code = 3002
                                    message = 'No Admin Account Found.'
                            else:
                                code = 3001
                                message = 'No Admin Account Found.'
                        else:
                            try:
                                limit = int(self.get_arguments('limit')[0])
                            except:
                                limit = None

                            try:
                                skip = int(self.get_arguments('skip')[0])
                            except:
                                skip = 0
                            if limit != None:
                                aProfiles = yield self.profile.find(
                                    {
                                        'closed': aClosed,
                                        'entityId': self.entityId,
                                        'applicationId': profileApplicationId
                                    },
                                    limit=limit,
                                    skip=skip
                                )
                                if len(aProfiles):
                                    for p in aProfiles:
                                        pAccount = yield self.account.find(
                                                {
                                                    '_id': p['accountId']
                                                },
                                                limit=1
                                            )
                                        if len(pAccount):
                                            v = {}
                                            v['closed'] = p['closed']
                                            v['locked'] = p['locked']
                                            v['active'] = p['active']
                                            v['id'] = str(p.get('_id'))
                                            v['firstName'] = pAccount[0].get('firstName')
                                            v['lastName'] = pAccount[0].get('lastName')
                                            v['contact'] = pAccount[0].get('contact')
                                            pServiceAccount = yield self.serviceAccount.find(
                                                    {
                                                        'profileId': p['_id'],
                                                        'entityId': self.entityId
                                                    },
                                                    limit=1
                                                )
                                            if len(pServiceAccount):
                                                v['firstName'] = pServiceAccount[0].get('firstName')
                                                v['lastName'] = pServiceAccount[0].get('lastName')
                                            result.append(v)
                                    if len(result):
                                        status = True
                                        code = 2000
                                        result.reverse()
                                    else:
                                        code = 3030
                                        message = 'No Admin Account Found.'
                                else:
                                    code = 3030
                                    message = 'No Admin Account Found.'
                            else:
                                aProfiles = yield self.profile.find(
                                    {
                                        'closed': aClosed,
                                        'entityId': self.entityId,
                                        'applicationId': profileApplicationId
                                    }
                                )
                                if len(aProfiles):
                                    for p in aProfiles:
                                        pAccount = yield self.account.find(
                                                {
                                                    '_id': p['accountId']
                                                },
                                                limit=1
                                            )
                                        if len(pAccount):
                                            v = {}
                                            v['closed'] = p['closed']
                                            v['locked'] = p['locked']
                                            v['active'] = p['active']
                                            v['id'] = str(p.get('_id'))
                                            v['firstName'] = pAccount[0].get('firstName')
                                            v['lastName'] = pAccount[0].get('lastName')
                                            v['contact'] = pAccount[0].get('contact')
                                            pServiceAccount = yield self.serviceAccount.find(
                                                    {
                                                        'profileId': p['_id'],
                                                        'entityId': self.entityId
                                                    },
                                                    limit=1
                                                )
                                            if len(pServiceAccount):
                                                v['firstName'] = pServiceAccount[0].get('firstName')
                                                v['lastName'] = pServiceAccount[0].get('lastName')
                                            result.append(v)
                                    if len(result):
                                        status = True
                                        code = 2000
                                        result.reverse()
                                    else:
                                        code = 3030
                                        message = 'No Admin Account Found.'
                                else:
                                    code = 3030
                                    message = 'No Admin Account Found.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not authorized.'
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
            # TODO: this need to be moved in a global class, from here
            profile = yield self.profile.find(
                            {
                                'accountId': self.accountId,
                                'applicationId': self.applicationId,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
            if len(profile):
                app = yield self.applications.find(
                            {
                                '_id': profile[0]['applicationId']
                            },
                            limit=1
                        )
                if len(app):
                    if app[0]['apiId'] == 402022: # TODO: till here

                        firstName = self.request.arguments.get('firstName')
                        code, message = Validate.i(
                                    firstName,
                                    'First Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=50,
                                    noSpace=True
                                )
                        if code != 4100:
                            raise Exception
                        lastName = self.request.arguments.get('lastName')
                        code, message = Validate.i(
                                    lastName,
                                    'Last Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=50,
                                    noSpace=True
                                )
                        if code != 4100:
                            raise Exception

                        phoneNumber = self.request.arguments.get('phoneNumber')
                        code, message = Validate.i(
                                    phoneNumber,
                                    'Phone Number',
                                    dataType=int,
                                )
                        if code != 4100:
                            raise Exception

                        countryCode = self.request.arguments.get('countryCode')
                        if countryCode == None:
                            code = 4251
                            message = 'Missing Argument - [ countryCode ].'
                            raise Exception
                        elif type(countryCode) != int:
                            code = 4552
                            message = 'Invalid Argument - [ countryCode ].'
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
                            message = 'Please enter a valid Country Code.'
                            raise Exception
                        if len(str(phoneNumber)) != country[0]['telMaxLength']:
                            code = 4252
                            message = 'Please enter a valid Phone Number.'
                            raise Exception('phoneNumber')
                        else:
                            phoneNumber = long(str(countryCode) + str(phoneNumber))

                        email = self.request.arguments.get('email')
                        if email != None:
                            code, message = Validate.i(
                                    email,
                                    'Email',
                                    dataType=unicode,
                                    notEmpty=True,
                                    inputType='email',
                                    maxLength=80,
                                    noSpace=True
                                )
                            if code != 4100:
                                raise Exception

                        profileApplication = yield self.applications.find(
                            {
                                'apiId': 402022,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
                        if not len(profileApplication):
                            raise Exception
                        else:
                            profileApplicationId = profileApplication[0]['_id']
                            accountData =   {
                                                'firstName': firstName,
                                                'lastName': lastName,
                                                'contact':  [
                                                        {
                                                            'verified': False,
                                                            'value': phoneNumber
                                                        }
                                                    ]
                                            }
                            if email:
                                accountData['contact'].append(
                                    {
                                        'verified': False,
                                        'value': email
                                    }
                                )
                            try:
                                acState = 0
                                try:
                                    accountId = yield self.account.insert(accountData)
                                except:
                                    pAccount = yield self.account.find(
                                            {
                                                'contact.0.value': phoneNumber
                                            },
                                            limit=1
                                        )
                                    if len(pAccount):
                                        acState = 1
                                        accountId = pAccount[0]['_id']
                                    if email:
                                        pAccount = yield self.account.find(
                                            {
                                                'contact.1.value': email
                                            },
                                            limit=1
                                        )
                                        if len(pAccount):
                                            acState = 2
                                            accountId = pAccount[0]['_id']
                                profileId = yield self.profile.insert(
                                    {
                                        'active': False,
                                        'locked': False,
                                        'closed': False,
                                        'accountId': accountId,
                                        'applicationId': profileApplicationId,
                                        'entityId': self.entityId,
                                        'data': []
                                    }
                                )
                                try:
                                    yield self.serviceAccount.insert(
                                        {
                                            'profileId': profileId,
                                            'firstName': firstName,
                                            'lastName': lastName,
                                            'entityId': self.entityId
                                        }
                                    )
                                except:
                                    yield self.serviceAccount.find_and_modify(
                                        query = {
                                                'profileId': profileId
                                            },
                                        update = {
                                            '$set': {
                                                'firstName': firstName,
                                                'lastName': lastName,
                                            }
                                        }
                                    )
                                code = 2000
                                message = 'New Admin Account has been created.'
                                status = True
                            except:
                                code = 5833
                                message = 'Internal Error, Please Contact the Support Team.'
                                if acState == 1:
                                    code = 4281
                                    message = 'Phone Number is already Registered.'
                                elif acState == 2:
                                    code = 4282
                                    message = 'Email is already Registered.'
                                raise Exception
                    else:
                        self.set_status(401)
                        code = 4003
                        message = 'You are not Authorized.'
                else:
                    self.set_status(401)
                    code = 4003
                    message = 'You are not Authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not Authorized.'
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

    @defer.inlineCallbacks
    def put(self):

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
            # TODO: this need to be moved in a global class, from here
            profile = yield self.profile.find(
                            {
                                'accountId': self.accountId,
                                'applicationId': self.applicationId,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
            if len(profile):
                app = yield self.applications.find(
                            {
                                '_id': profile[0]['applicationId']
                            },
                            limit=1
                        )
                if len(app):
                    if app[0]['apiId'] == 402022: # TODO: till here

                        try:
                            profileId = ObjectId(self.request.arguments['id'])
                        except:
                            code = 4120
                            message = 'Invalid Argument - [ id ].'
                            raise Exception

                        aClosed = self.request.arguments.get('closed')
                        code, message = Validate.i(
                                    aClosed,
                                    'Closed',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception

                        firstName = self.request.arguments.get('firstName')
                        code, message = Validate.i(
                                    firstName,
                                    'First Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=50,
                                    noSpace=True
                                )
                        if code != 4100:
                            raise Exception
                        lastName = self.request.arguments.get('lastName')
                        code, message = Validate.i(
                                    lastName,
                                    'Last Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=50,
                                    noSpace=True
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            yield self.serviceAccount.insert(
                                    {
                                        'profileId': profileId,
                                        'firstName': firstName,
                                        'lastName': lastName,
                                        'entityId': self.entityId
                                    }
                                )
                        except:
                            yield self.serviceAccount.find_and_modify(
                                query = {
                                        'profileId': profileId
                                    },
                                update = {
                                    '$set': {
                                        'firstName': firstName,
                                        'lastName': lastName,
                                    }
                                }
                            )
                        updateResult = yield self.profile.find_and_modify(
                                        query = {
                                            '_id': profileId,
                                            'entityId': self.entityId
                                        },
                                        update = {
                                            '$set': {
                                                'closed': aClosed
                                                }
                                        }
                                    )
                        if updateResult:
                            status = True
                            code = 2000
                            message = 'Admin Account details has been updated.'
                        else:
                            code = 4210
                            message = 'This Admin Account does not exist.'
                    else:
                        self.set_status(401)
                        code = 4003
                        message = 'You are not Authorized.'
                else:
                    self.set_status(401)
                    code = 4003
                    message = 'You are not Authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not Authorized.'
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

    @defer.inlineCallbacks
    def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # TODO: this need to be moved in a global class, from here
            profile = yield self.profile.find(
                            {
                                'accountId': self.accountId,
                                'applicationId': self.applicationId,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
            if len(profile):
                app = yield self.applications.find(
                            {
                                '_id': profile[0]['applicationId']
                            },
                            limit=1
                        )
                if len(app):
                    if app[0]['apiId'] == 502022: # TODO: till here
                        try:
                            profileId = ObjectId(self.get_arguments('id')[0])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception
                        updateResult = yield self.profile.find_and_modify(
                                    query = {
                                            '_id': profileId,
                                            'entityId': self.entityId,
                                            'closed': False
                                        },
                                    update = {
                                        '$set': {
                                            'closed': True
                                        }
                                    }
                            )
                        if updateResult:
                            status = True
                            code = 2000
                            message = 'Admin Account has been Closed.'
                        else:
                            code = 4210
                            message = 'This Admin Account does not exist.'
                    else:
                        code = 4003
                        message = 'You are not Authorized.'
                        self.set_status(401)
                else:
                    code = 4003
                    message = 'You are not Authorized.'
                    self.set_status(401)
            else:
                code = 4003
                message = 'You are not Authorized.'
                self.set_status(401)
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

