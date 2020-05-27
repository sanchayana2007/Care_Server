import 'dart:convert';
import 'dart:io';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:ohzas/handler/build_config.dart';
import 'package:ohzas/handler/network_handler.dart';
import 'package:ohzas/handler/shared_pref_handler.dart';
import 'package:ohzas/util/log_util.dart';
import 'package:ohzas/util/toast_util.dart';

class HttpRequestHandler {
  String xApiKey = BuildConfig.xApiKey;
  String xAuthorizationKey = BuildConfig.xAuthorization;
  String xOriginKey = BuildConfig.xOriginKey;
  SharedPrefHandler sharedPreferencesHandler;
  Map<String, String> headers = {};
  Map<String, String> authHeaders = {};
  BuildContext context;

  HttpRequestHandler(BuildContext buildContext) {
    this.sharedPreferencesHandler = new SharedPrefHandler();
    this.authHeaders = {
      'x-Origin-Key': this.xOriginKey,
      'Content-Type': 'application/json',
    };
    this.context = buildContext;
    getHeaders();
  }

  getHeaders() async {
    this.headers = {
      'Authorization': 'Bearer ' + await sharedPreferencesHandler.getString(sharedPreferencesHandler.xAuthorizationKey),
      'x-Origin-Key': await sharedPreferencesHandler.getString(sharedPreferencesHandler.xOriginKey),
      'x-Api-Key': await sharedPreferencesHandler.getString(sharedPreferencesHandler.xApiKey),
      'Content-Type': 'application/json',
    };
  }

  Future<Map<String, dynamic>> authSignIn(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/sign/in'),
        headers: authHeaders,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      Toaster.e(context, message: 'Invalid Server Response.');
      return null;
    }
  }

  Future<Map<String, dynamic>> authVerify(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.put(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/sign/in'),
        headers: authHeaders,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      Toaster.e(context, message: 'Invalid Server Response.');
      return null;
    }
  }

  Future<Map<String, dynamic>> authSignUp(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/sign/up'),
        headers: authHeaders,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      Toaster.e(context, message: 'Invalid Server Response.');
      return null;
    }
  }

  Future<Map<String, dynamic>> getProfile(Object jsonBody) async {
    http.Response response = await http.get(
      Uri.encodeFull(BuildConfig.serverUrl + '/web/api/resource/profile'),
      headers: headers,
    );
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> getServiceAccount() async {
    http.Response response = await http.get(
      Uri.encodeFull(BuildConfig.serverUrl +
          '/web/api/test/booking/serviceaccount',
      ),
      headers: headers,
    );
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> getTrstServiceAccount() async {
    http.Response response = await http.get(
      Uri.encodeFull(BuildConfig.serverUrl +
          '/web/api/test/tourist/verify',
      ),
      headers: headers,
    );
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postTrstServiceAccDetails(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/test/tourist/details'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> putTrstSubServiceAccDetails(Object jsonBody) async {
    http.Response response = await http.put(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/tourist/member'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> getServiceList() async {
    http.Response response = await http.get(
      Uri.encodeFull(BuildConfig.serverUrl +
          '/web/api/med/servicelist'),
      headers: headers,
    );
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> getAppointmentBooking() async {
    if (headers.isEmpty) {
      await getHeaders();
    }
    http.Response response = await http.get(
      Uri.encodeFull(BuildConfig.serverUrl +
          '/web/api/med/book'),
      headers: headers,
    );
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> getTrstMembers() async {
    http.Response response = await http.get(
      Uri.encodeFull(BuildConfig.serverUrl +
          '/web/api/tourist/member',
      ),
      headers: headers,
    );
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> getSubTrstMembersFromPhoneNum(String phoneNum) async {
    http.Response response = await http.get(
      Uri.encodeFull(BuildConfig.serverUrl +
          '/web/api/accom/tourist?pNum=' + phoneNum,
      ),
      headers: headers,
    );
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postBookingStep2(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.put(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/test/booking/checkin'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postBookingStep2Update(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.put(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/test/booking/update/details'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postSubmitBooking(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/med/book'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> putSubmitBooking(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    await getHeaders();
    http.Response response = await http.put(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/med/book'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postPreRegisteredBooking(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/accom/tourist'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postSetTouristPrimary(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/tourist/primary'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> deleteTourist(String memberId) async {
    http.Response response = await http.delete(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/tourist/member?id=' + memberId),
        headers: headers,
//        body: jsonEncode(jsonBody),
    );
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postBookingSendSms(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl + '/web/api/test/booking/confirm/sms'),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postServiceAccount(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl +
            '/web/api/test/booking/serviceaccount',
        ),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> putServiceAccount(Object jsonBody) async {
    http.Response response = await http.put(
        Uri.encodeFull(BuildConfig.serverUrl +
            '/web/api/test/booking/serviceaccount',
        ),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>> postServiceAccountDetails(Object jsonBody) async {
    if (!await NetworkHandler.isOnlineWithToast(context)) {
      return null;
    }
    http.Response response = await http.post(
        Uri.encodeFull(BuildConfig.serverUrl +
            '/web/api/test/service/update',
        ),
        headers: headers,
        body: jsonEncode(jsonBody));
    try {
      Map<String, dynamic> respJson = jsonDecode(response.body);
      return respJson;
    } catch (e) {
      return null;
    }
  }

}
