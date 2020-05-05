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

from __future__ import division
from lib import *
from PIL import Image

@xenSecureV1
class MtimeWebCrowdContentHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

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

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]

    bookingCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][1]['name']
                ]

    vehicle = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][4]['name']
                ]

    vehicleType = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
                ]

    booking = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][10]['name']
                ]

    coupon = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][11]['name']
                ]
    testBooking = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][12]['name']
                ]
    locationPoint = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][13]['name']
                ]
    crowdContent = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][14]['name']
                ]

    fu = FileUtil()

    @defer.inlineCallbacks
    def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # GET FILES FROM REQUEST BODY
            try:
                media = self.request.files['media'][0]
            except Exception as e:
                code = 4100
                message = 'Media file missing'
                raise Exception

            # TODO: this need to be moved in a global class, from here
	    profile = yield self.profile.find(
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
            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                app = yield self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            {
                                '_id': 1,
                                'apiId': 1
                            },
                            limit=1
                        )
                if len(app):
                    self.apiId = app[0]['apiId']
		    if self.apiId in [ 402022,402020 ]:
			if self.apiId == 402020: # TODO: till here
                            try:
                                aLatitude = float(self.request.arguments['latitude'][0])
                                code, message = Validate.i(
                                    aLatitude,
                                    'latitude',
                                    maxNumber=90,
                                    minNumber=-90
                                )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ latitude ].'
                                raise Exception

                            try:
                                aLongitude = float(self.request.arguments['longitude'][0])
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


                            filepath = []

                            mediaType = media['content_type']
                            mediaType = yield mimetypes.guess_extension(
                                            mediaType,
                                            strict=True
                                )

                            mediaTime = timeNow()
                            if str(mediaType) in ['.jpeg', '.jpg', '.jpe']:
                                fName = mediaTime
                                fRaw = media['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + mediaType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                # Converting to PNG
                                mediaType = '.png'
                                fpx = fp + '/' + str(fName) + mediaType
                                filepath.append(fpx)
                                im = Image.open(fpm)
                                im.save(fpx, 'PNG')
                                os.system('rm ' + fpm)
                                os.system('chmod 755 -R ' + fp + '*')

                            elif str(mediaType) in ['.mp4']:
                                fName = mediaTime
                                fRaw = media['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + mediaType
                                filepath.append(fpm)
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                            elif str(mediaType) in ['.png']:
                                fName = mediaTime
                                fRaw = media['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + mediaType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                # Converting to PNG
                                mediaType = '.png'
                                fpx = fp + '/' + str(fName) + mediaType
                                filepath.append(fpx)
                                im = Image.open(fpm)
                                im.save(fpx, 'PNG')
                                os.system('chmod 755 -R ' + fp + '*')

                            else:
                                message = 'Invalid File Type'
                                code = 4011
                                raise Exception


                            crowdContentId = yield self.crowdContent.insert(
                                    {
                                        'disabled':False,
                                        'verified':False,
                                        'profileId':self.profileId,
                                        'accountId':self.accountId,
                                        'entityId':self.entityId,
                                        'location': [
                                                {
                                                    'type': 'Point',
                                                    'coordinates': [aLongitude, aLatitude]
                                                }
                                        ],
                                        'media':[
                                                    {
                                                        'mimeType':mediaType,
                                                        'time':mediaTime
                                                    }
                                        ]
                                    }
                                )
                            # Moving Temp dir to crowdcontent dir
                            uPath = self.fu.uploads + '/' + str(self.entityId)
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            uPath = uPath + '/crowd_content/'

                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            uPath = uPath + str(self.profileId) + '/'

                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            uPath = uPath + str(crowdContentId) + '/'

                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            for i in filepath:
                                os.system('mv ' + i + ' ' + uPath)

                            Log.d(uPath)

                            os.system('chmod 755 -R ' + uPath + '*')
                            result.append(str(crowdContentId))


                            code = 2000
                            status = True
                            message = "All Documents have been successfully uploaded."
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
            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                app = yield self.applications.find(
                            {
                                'disabled': False,
                                '_id': self.applicationId
                            },
                            {
                                'apiId': 1
                            },
                            limit=1
                        )
                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [402022,402021]:
                        if self.apiId in [ 402022 ]: # TODO: till here

                            statusValue = self.request.arguments.get('statusValue')
                            code,message = Validate.i(
                                            statusValue,
                                            'Status Value',
                                            dataType = bool,
                                        )
                            if code != 4100:
                                raise Exception
                            crowdContentId = self.request.arguments.get('crowdContentId')
                            locId = self.request.arguments.get('locId')
                            nearBy = yield self.locationPoint.find(
                                    {
                                        'entityId': self.entityId,
                                        '_id':ObjectId(locId)
                                    }
                                )
                            if len(nearBy):
                                longLat = nearBy[0]['location'][0]['coordinates']
                            else:
                                status = False
                                message = "Invalid Location"
                                code = 4550
                                raise Exception
                            if len(longLat):
                                crowdContentVerify = yield self.crowdContent.update(
                                                {
                                                    '_id':ObjectId(crowdContentId)
                                                },
                                                {
                                                '$set': {
                                                            'verified': statusValue,
                                                            'location': [
                                                                            {
                                                                                'type': 'Point',
                                                                                'coordinates': longLat
                                                                            }
                                                                        ],
                                                        }
                                                }
                                            )
                            else:
                                code = 2003
                                status = False
                                message = "Invalid location"
                                raise Exception
                            if crowdContentVerify['n']:
                                code = 2000
                                status = True
                                if statusValue:
                                    message = "CrowdContent has been approved."
                                else:
                                    message = "CrowdContent has been declined."
                            else:
                                code = 2003
                                status = False
                                message = "Invalid verification request"
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

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            locId = ObjectId(self.request.arguments['id'][0])
        except:
            locId = None

        try:
            # TODO: this need to be moved in a global class
            profile = yield self.profile.find(
                            {
                                'entityId': self.entityId,
                                'accountId': self.accountId,
                                'applicationId': self.applicationId
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
                        if locId:
                            locDetails = yield self.crowdContent.find(
                                            {
                                                'entityId': self.entityId,
                                                '_id':locId
                                            },
                                            {
                                            '_id':1,
                                            'entityId':1,
                                            'profileId':1,
                                            'accountId':1,
                                            'disabled':1,
                                            'verified':1,
                                            'location':1,
                                            'media':1
                                            }
                                        )
                            if len(locDetails):
                                for docx in locDetails[0]['media']:
                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(locDetails[0]['entityId']) + '/crowd_content/' \
                                                    + str(locDetails[0]['profileId'])  + '/' \
                                                    + str(locDetails[0]['_id']) + '/' + \
                                                    str(docx['time']) + docx['mimeType']
                                    locDetails[0]['id'] = str(locDetails[0]['_id'])
                                    locDetails[0]['entity'] = str(locDetails[0]['entityId'])
                                    locDetails[0]['profile'] = str(locDetails[0]['profileId'])
                                    nearby = yield self.locationPoint.find(
                                            {
                                                'entityId': self.entityId,
                                                'location.0' :
                                                { '$near' :
                                                    {
                                                        '$geometry' :
                                                        {
                                                            'type' : "Point",
                                                            'coordinates' : locDetails[0]['location'][0]['coordinates']
                                                        },
                                                        '$minDistance' : 0,
                                                        '$maxDistance' : 1000
                                                    }
                                                }
                                            },
                                            {
                                            '_id':1,
                                            'locName':1
                                            }
                                        )
                                    if len(nearby):
                                        locDetails[0]['nearby'] = []
                                        for loc in nearby:
                                            v = {
                                                    'id':str(loc['_id']),
                                                    'locName':loc['locName']
                                                }
                                            locDetails[0]['nearby'].append(v)
                                    else:
                                        locDetails[0]['nearby'] = []
                                    accDetails = yield self.account.find(
                                                    {
                                                        '_id':locDetails[0]['accountId']
                                                    },
                                                    {
                                                        '_id':0,
                                                        'firstName':1,
                                                        'lastName':1,
                                                        'contact':1,
                                                    }
                                                )
                                    if len(accDetails):
                                        locDetails[0]['touristInfo'] = accDetails
                                    else:
                                        locDetails[0]['touristInfo'] = []
                                    del locDetails[0]['_id']
                                    del locDetails[0]['entityId']
                                    del locDetails[0]['accountId']
                                    del locDetails[0]['profileId']
                                    code = 2000
                                    status = True
                                result.append(locDetails[0])
                            else:
                                code = 4004
                                status = False
                                message = "No Data Found"
                        else:
                            locDetails = yield self.crowdContent.find(
                                            {
                                                'entityId': self.entityId,
                                            },
                                            {
                                            '_id':1,
                                            'entityId':1,
                                            'accountId':1,
                                            'profileId':1,
                                            'disabled':1,
                                            'verified':1,
                                            'location':1,
                                            'media':1
                                            }
                                        )
                            if len(locDetails):
                                code = 2000
                                status = True
                                for docx in locDetails:
                                    docx['media'][0]['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(docx['entityId']) + '/crowd_content/' \
                                                    + str(docx['profileId'])  + '/' \
                                                    + str(docx['_id']) + '/' + \
                                                    str(docx['media'][0]['time']) + docx['media'][0]['mimeType']
                                    docx['id'] = str(docx['_id'])
                                    docx['entity'] = str(docx['entityId'])
                                    accDetails = yield self.account.find(
                                                    {
                                                        '_id':docx['accountId']
                                                    },
                                                    {
                                                        '_id':0,
                                                        'firstName':1,
                                                        'lastName':1,
                                                        'contact':1,
                                                    }
                                                )
                                    if len(accDetails):
                                        docx['touristInfo'] = accDetails
                                    else:
                                        docx['touristInfo'] = []
                                    del docx['profileId']
                                    del docx['_id']
                                    del docx['entityId']
                                    del docx['accountId']
                                    result.append(docx)
                            else:
                                code = 4004
                                status = False
                                message = "No Data Found"
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

