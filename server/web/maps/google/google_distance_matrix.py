#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib import *

@xenSecureV1
class MmsWebMapsGoogleDistanceMatrix(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('GET')

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # TODO: this need to be moved in a global class, from here
            profile = yield self.profile.find(
                            {
                                'entityId': self.entityId,
                                'accountId': self.accountId,
                                'applicationId': self.applicationId
                            },
                            limit=1
                        )
            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                app = yield self.applications.find(
                            {
                                '_id': profile[0]['applicationId']
                            },
                            limit=1
                        )
                if len(app):
                    if app[0]['apiId'] == 40216: # TODO: till here
                        try:
                            origins = str(self.get_arguments('origins')[0]).split(',')
                            code, message = Validate.i(
                                origins,
                                'Origins',
                                dataType=list,
                                maxLength=2,
                                minLength=2
                            )
                            if code != 4100:
                                raise Exception
                            destinations = str(self.get_arguments('destinations')[0]).split(',')
                            code, message = Validate.i(
                                destinations,
                                'Destinations',
                                dataType=list,
                                maxLength=2,
                                minLength=2
                            )
                            if code != 4100:
                                raise Exception
                        except:
                            if not len(message):
                                message = 'Invalid Systax.'
                                code = 4201
                            raise Exception

                        API_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?' + \
                                'origins={0}&destinations={1}&key={2}'
                        API_URL = API_URL.format(
                                            origins[0] + ',' + origins[1],
                                            destinations[0] + ',' + destinations[1],
                                            MAPS_GOOGLE_KEY
                                        )
                        client = httplib2.Http()
                        resp, content = yield client.request(
                                API_URL, 'GET'
                            )
                        if int(resp['status']) == 200:
                            response = json.loads(content.decode())
                            self.write(response)
                            self.finish()
                            return
                        else:
                            rcode = False
                            rmsg = 'Internal Error, Please Conatct the Support Team.'
                            ecode = 5201
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not Authorized.'
                else:
                    code = 4003
                    self.set_status(401)
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
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
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
            message = 'Internal Error Please Contact the Support Team.'
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
