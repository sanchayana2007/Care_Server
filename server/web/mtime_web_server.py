#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import *

class WebServerApplication(cyclone.web.Application):
    def __init__(self, app):

        handlers = [
            # TODO: this will moved to another server
            (r'/web/api/sign/in', SignInHandler),
            (r'/web/api/sign_in', SignInHandler),
            (r'/web/api/sign/up', SignUpHandler),
            (r'/web/api/authorization/changePassword', ChangePasswordHandler),

            (r'/web/socket/admin/realtime/socket', MmsWebAdminRealtimeWebSocketHandler),
            (r'/web/socket/user/realtime/socket', MmsWebUserRealtimeWebSocketHandler),
            (r'/web/socket/driver/realtime/socket', MmsWebDriverRealtimeWebSocketHandler),
            #(r'/web/socket/user/rt_socket', VtsRealtimeWebSocketHandler),

            (r'/web/api/med/book', MedServiceBookHandler),
            (r'/web/api/med/update', MedServiceUpdateHandler),
            (r'/web/api/med/servicelist', MedServiceListHandler),
            (r'/web/api/med/servicemedia', MedServiceMediaHandler),
            (r'/web/api/med/servicesession', MedServiceSessionHandler),


            (r'/web/api/med/restore/book/', MedServiceBookRestoreHandler),
            (r'/web/api/med/restore/list/', MedRestoreServiceListHandler),

            (r'/web/api/component/vehicle', VehicleHandler),
            (r'/web/api/component/device', DeviceHandler),
            (r'/web/api/component/service/area', ServiceAreaHandler),
            (r'/web/api/component/geofence', GeofenceHandler),
            (r'/web/api/component/vehicle/type', VehicleTypeHandler),
            (r'/web/api/component/booking/category', VehicleCategoryHandler),
            (r'/web/api/component/location', LocationPointHandler),
            (r'/web/api/component/country', MtimeWebCountryList),
	    (r'/web/api/component/document', DocumentTypeHandler),
	    (r'/web/api/component/document/list', MtimeWebDocumentList),

	    (r'/web/api/booking/details', MtimeWebBookingDetailsGetHandler),
	    (r'/web/api/test/booking', MtimeWebTestBookingGetHandler),
	    (r'/web/api/test/booking/checkin', MtimeWebTestBookingCinHandler),
	    (r'/web/api/sub/booking/checkin', MtimeWebSubBookingCinHandler),
	    (r'/web/api/test/booking/checkout', MtimeWebTestBookingCoutHandler),
	    (r'/web/api/test/booking/confirm', MtimeWebTestBookingConfirmHandler),
	    (r'/web/api/test/booking/update/details', MtimeWebTestBookingDetailsHandler),
	    (r'/web/api/test/booking/paid', MtimeWebTestBookingPaidHandler),
	    (r'/web/api/test/booking/confirm/sms', MtimeWebTestBookingSMSConfirmHandler),

	    (r'/web/api/test/booking/serviceaccount', MtimeWebServiceAccountHandler),
	    (r'/web/api/test/tourist/verify', MtimeWebTouristVerifyHandler),
	    (r'/web/api/test/tourist/details', MtimeWebTouristDetailsHandler),
	    (r'/web/api/test/service/update', MtimeWebServiceUpdateHandler),
	    (r'/web/api/tourist/service/find', MtimeWebTouristServiceGetHandler),
	    (r'/web/api/tourist/media', MtimeWebCrowdContentHandler),
            (r'/web/api/resource/subadmin', MtimeSubAdminSignUpHandler),
            (r'/web/api/resource/profile', MmsProfileHandler),
            (r'/web/api/tourist/member', MtimeWebSubTouristHandler),
            (r'/web/api/tourist/primary', MtimeWebPrimaryTouristHandler),
            (r'/web/api/accom/tourist', MtimeWebAccTouristHandler),
            (r'/web/api/tourist/nokyc', MtimeWebNoKycTouristHandler),

            (r'/web/api/resource/admin', AdminHandler),
            (r'/web/api/resource/accprov', AccProvHandler),
            (r'/web/api/resource/driver', DriverHandler),
            (r'/web/api/resource/driver/picture/profile', DriverPictureProfileHandler),
            (r'/web/api/resource/user', UserHandler),

            (r'/web/api/element/device/model', DeviceModelHandler),
            (r'/web/api/element/location/source', LocationSourceHandler),
            (r'/web/api/element/phone/country', PhoneCountryHandler),

            (r'/web/api/check/update', CheckUpdateHandler),
            (r'/web/api/check/service', CheckServiceHandler),

            (r'/web/api/booking', MmsWebBookingHandler),
            (r'/web/api/files', FileUploadHandler),

            (r'/web/api/coupon', MmsCouponHandler),
            (r'/web/api/coupon/default', MmsDefaultCouponHandler),
            #
            #    External APIS
            #
            #(r'/web/api/maps/google/distance/matrix', MmsWebMapsGoogleDistanceMatrix),
            (r'/web/api/maps/google/directions', MmsWebMapsGoogleDirections),
            (r'/web/api/maps/google/place/search', MmsWebMapsGooglePlaceSearch),
            (r'/web/api/maps/google/place/auto/search', MmsWebMapsGooglePlaceAutoSearch),
            (r'/web/api/maps/google/place/details', MmsWebMapsGooglePlaceDetails),
            (r'/web/api/maps/google/geocoding/reverse', MmsWebMapsGoogleGeocodingReverse),

            #(r'/(.*)', cyclone.web.StaticFileHandler, {'path': 'static'}),
        ]

        # Connect to Redis.
        #RedisMixin.setup(REDIS_SERVER_HOST, REDIS_SERVER_PORT, REDIS_SERVER_DB_ID, 10)

        cyclone.web.Application.__init__(self, handlers)

application = service.Application('MMS WEB SERVER')
WEB_SERVER_APP = WebServerApplication(application)
server = internet.TCPServer(WEB_SERVER_PORT, WEB_SERVER_APP, interface=WEB_SERVER_INTERFACE)
server.setServiceParent(application)

