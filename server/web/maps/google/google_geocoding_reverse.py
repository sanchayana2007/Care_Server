#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib import *

@xenSecureV1
class MmsWebMapsGoogleGeocodingReverse(cyclone.web.RequestHandler, MongoMixin):

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
                    self.apiId = app[0]['apiId']
                    if self.apiId in [40216, 20216]: # TODO: till here
                        try:
                            try:
                                aLatitude = float(self.get_arguments('latitude')[0])
                                code, message = Validate.i(
                                    aLatitude,
                                    'latitude',
                                    maxNumber=90,
                                    minNumber=-90
                                )
                                if code != 4100:
                                    raise Exception
                            except:
                                code = 4210
                                message = 'Invalid Argument - [ latitude ].'
                                raise Exception

                            try:
                                aLongitude = float(self.get_arguments('longitude')[0])
                                code, message = Validate.i(
                                    aLongitude,
                                    'longitude',
                                    maxNumber=180,
                                    minNumber=-180
                                )
                                if code != 4100:
                                    raise Exception
                            except:
                                code = 4310
                                message = 'Invalid Argument - [ longitude ].'
                                raise Exception
                        except:
                            if not len(message):
                                message = 'Invalid Systax.'
                                code = 4201
                            raise Exception

                        API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?' \
                                        + 'key={0}' \
                                        + '&latlng={1},{2}'
                        API_URI = API_URL.format(
                                                MAPS_GOOGLE_KEY,
                                                aLatitude,
                                                aLongitude
                                        )
                        client = httplib2.Http()
                        resp, content = yield client.request(
                                API_URI, 'GET'
                            )
                        if int(resp['status']) == 200:
                            rs = json.loads(content)
                            print rs
                            if len(rs['results']):
                                val = rs['results'][0]
                                v = {
                                        'address': val['formatted_address'],
                                        'location': [
                                                val['geometry']['location']
                                            ],
                                    }
                                try:
                                    pCode = val.get('plus_code')
                                    if pCode:
                                        if 'Bangladesh' not in pCode.get('compound_code'):
                                            result.append(v)
                                    else:
                                        result.append(v)
                                except:
                                    result = []
                                status = True
                                code = 2000
                            else:
                                code = 4500
                                message = 'Location not found.'
                        else:
                            Log.w('GMAPS', content)
                            status = False
                            message = 'Internal Error, Please Conatct the Support Team.'
                            code = 5201
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
