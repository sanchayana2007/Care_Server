#!/usr/bin/VtsAdminSignInHandler
# -*- coding: utf-8 -*-

from __future__ import division

'''
'''
from typing import Optional, Awaitable
from ..lib.lib import *


@xenSecureV1
class PassQRHandler(tornado.web.RequestHandler,
                    MongoMixin):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    SUPPORTED_METHODS = ('POST', 'PUT', 'GET')

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
    touristPass = MongoMixin.serviceDb[
        CONFIG['database'][1]['table'][20]['name']
    ]
    subTourist = MongoMixin.serviceDb[
        CONFIG['database'][1]['table'][17]['name']
    ]

    fu = FileUtil()

    # @defer.inlineCallbacks
    async def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # TODO: this need to be moved in a global class
            profileQ = self.profile.find(
                {
                    'closed': False,
                    'entityId': self.entityId,
                    'accountId': self.accountId,
                    'applicationId': self.applicationId
                },
                {
                    '_id': 1
                },
                limit=1
            )
            profile = []
            async for r in profileQ:
                profile.append(r)

            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                    {
                        '_id': self.applicationId
                    },
                    {
                        '_id': 0,
                        'apiId': 1
                    },
                    limit=1
                )
                app = []
                async for r in appQ:
                    app.append(r)

                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] in [402021, 402022]:  # TODO: till here
                        if self.apiId == 402021:
                            passDetails = []
                            passId = str(self.request.arguments['passId'][0].decode())
                            code, message = Validate.i(
                                passId,
                                dataType=str,
                                maxLength=8,
                                minLength=6
                            )
                            if code != 4100:
                                raise Exception

                            passDetailsQ = self.touristPass.find(
                                {
                                    'passIdn': passId
                                },
                                limit=1
                            )
                            async for r in passDetailsQ:
                                passDetails.append(r)

                            if not len(passDetails):
                                code = 4040
                                message = 'Invalid Pass Id'
                                raise Exception

                            accFindQ = self.account.find(
                                {
                                    '_id': passDetails[0]['accountId']
                                },
                                {
                                    '_id': 1,
                                    'firstName': 1,
                                    'lastName': 1,
                                    'contact': 1
                                },
                                limit=1
                            )
                            accFind = []
                            async for r in accFindQ:
                                accFind.append(r)

                            if not len(accFind):
                                status = False
                                code = 4550
                                message = "No Account found"
                                raise Exception
                            for i in passDetails[0]['touristMem']:
                                resQ = self.subTourist.find(
                                    {
                                        '_id': ObjectId(i),
                                        '$where': 'this.subTouristDetails != null'
                                    },
                                    {
                                        '_id': 1,
                                        'verified': 1,
                                        'disabled': 1,
                                        'primary': 1,
                                        'subTouristDetails': 1,
                                        'documents': 1,
                                        'faceProof': 1,
                                        'location': 1,
                                        'submitRequest': 1
                                    }
                                )
                                res = []
                                async for r in resQ:
                                    res.append(r)

                                if len(res):
                                    res = res[0]
                                    for docx in res['documents']:
                                        docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                       + str(self.entityId) + '/tourist_kyc/' \
                                                       + 'subtourist/' + str(res['_id']) \
                                                       + '/' + str(docx['time']) + docx['mimeType']
                                    for docx in res['faceProof']:
                                        docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                       + str(self.entityId) + '/tourist_kyc/' \
                                                       + 'subtourist/' + str(res['_id']) \
                                                       + '/' + str(docx['time']) + docx['mimeType']
                                    res['id'] = str(res['_id'])
                                    # res['touristProfile'] = str(passDetails[0]['profileId'])
                                    del res['_id']
                                    result.append(res)

                            accFind[0]['_id'] = str(accFind[0]['_id'])
                            accFind[0]['profileId'] = str(passDetails[0]['profileId'])
                            result = [
                                {
                                    'account': accFind[0],
                                    'members': result
                                }
                            ]
                            status = True
                            code = 2000
                            message = "List of tourist members"
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
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not authorized.'
        except Exception as e:
            status = False
            result = []
            # self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error Please Contact the Support Team.'
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
            await self.finish()
            return
        except Exception as e:
            status = False
            result = []
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
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
            await self.finish()
            return
