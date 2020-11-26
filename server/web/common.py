#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../lib')
sys.path.append('../lib/utils')

from lib import *

sys.path.insert(0, './authorization')
sys.path.insert(0, './resource/')
sys.path.insert(0, './component/')
sys.path.insert(0, './element/')
sys.path.insert(0, './check/')
sys.path.insert(0, './socket/')
sys.path.insert(0, './booking/')
sys.path.insert(0, './coupon/')
sys.path.insert(0, './maps/google/')
sys.path.insert(0, './test/')
sys.path.insert(0, './tourist/')


sys.path.insert(0, './med/')

from admin_rt_socket import MmsWebAdminRealtimeWebSocketHandler
from user_rt_socket import MmsWebUserRealtimeWebSocketHandler
from driver_rt_socket import MmsWebDriverRealtimeWebSocketHandler
from rt_socket import VtsRealtimeWebSocketHandler

from medservice import MedServiceBookHandler
from medserviceupdate import MedServiceUpdateHandler
from medservicelist import MedServiceListHandler
from medservicemedia import MedServiceMediaHandler
from medservicesession import MedServiceSessionHandler
from account_overview import MedServiceAccountOverviewHandler
from provider_service_list import MedServiceProviderServiceHandler
from service_info_provider import MedServiceServiceInfoProviderHandler
from assign_medservice import MedServiceAssignServiceHandler

from send_sms import MedServiceSendSMSHandler

from state_info import MedServiceStateInfoHandler
from district_info import MedServiceDistrictInfoHandler
from place_info import MedServicePlaceInfoHandler

from restoremedservice import MedServiceBookRestoreHandler
from restoremedservicelist import MedRestoreServiceListHandler

from userinfo import MedServiceInfoHandler
from service_provider import MedServiceProviderHandler
from service_provider_v2 import MedServiceProviderV2Handler

from service_product import MedServiceProductHandler

from files import *
from sign_in import SignInHandler
from sign_up import SignUpHandler
from change_password import ChangePasswordHandler

from booking_test import MtimeWebTestBookingGetHandler
from booking_test_checkin import MtimeWebTestBookingCinHandler
from booking_test_checkout import MtimeWebTestBookingCoutHandler
from booking_test_confirm import MtimeWebTestBookingConfirmHandler
from booking_test_paid import MtimeWebTestBookingPaidHandler
from booking_details import MtimeWebTestBookingDetailsHandler
from booking_test_sms_confirm import MtimeWebTestBookingSMSConfirmHandler
from sub_admin import MtimeSubAdminSignUpHandler
from subtourist import MtimeWebSubTouristHandler
from primary_tourist import MtimeWebPrimaryTouristHandler
from acc_tourist import MtimeWebAccTouristHandler
from acc_tourist_nokyc import MtimeWebNoKycTouristHandler
from book import MtimeWebBookingDetailsGetHandler
from booking_subtourist import MtimeWebSubBookingCinHandler

from service_account_test import MtimeWebServiceAccountHandler
from tourist_verify import MtimeWebTouristVerifyHandler
from tourist_details import MtimeWebTouristDetailsHandler
from service_update import MtimeWebServiceUpdateHandler
from document_type import DocumentTypeHandler
from document_list import MtimeWebDocumentList

from acc_service_find import MtimeWebTouristServiceGetHandler
from crowd_content import MtimeWebCrowdContentHandler

from admin import AdminHandler
from acc_prov import AccProvHandler
from driver import DriverHandler
from driver_picture import DriverPictureProfileHandler
from user import UserHandler

from profile import MmsProfileHandler

from vehicle_categories import VehicleCategoryHandler
from vehicle_type import VehicleTypeHandler
from device import DeviceHandler
from service_area import ServiceAreaHandler
from geofence import GeofenceHandler
from vehicle import VehicleHandler
from location_point import LocationPointHandler
from country_list import MtimeWebCountryList

from device_model import DeviceModelHandler
from location_source import LocationSourceHandler
from phone_country import PhoneCountryHandler

from check_update import CheckUpdateHandler
from check_service import CheckServiceHandler

from coupon import MmsCouponHandler
from default_coupon import MmsDefaultCouponHandler
from booking import MmsWebBookingHandler
#from driver_booking import MmsWebDriverBookingHandler
from files import *

from google_distance_matrix import MmsWebMapsGoogleDistanceMatrix
from google_directions import MmsWebMapsGoogleDirections
from google_place_search import MmsWebMapsGooglePlaceSearch
from google_place_auto_search import MmsWebMapsGooglePlaceAutoSearch
from google_place_details import MmsWebMapsGooglePlaceDetails
from google_geocoding_reverse import MmsWebMapsGoogleGeocodingReverse

