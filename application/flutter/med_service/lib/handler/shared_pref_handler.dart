import 'package:medservice/util/log_util.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SharedPrefHandler {

  final String signedInAppId = "signedInAppId";
  final String xOriginKey = "xOriginKey";
  final String xApiKey = "xApiKey";
  final String xAuthorizationKey = "xAuthorizationKey";

  Future<String> getString(String key) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString(key) ?? '';
  }

  Future<bool> setString(String key, String value) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.setString(key, value);
  }

  Future<double> getDouble(String key) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getDouble(key) ?? -1.0;
  }

  Future<bool> setDouble(String key, double value) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.setDouble(key, value);
  }

  Future<int> getInt(String key) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getInt(key) ?? -1;
  }

  Future<bool> setInt(String key, int value) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.setInt(key, value);
  }

  Future<bool> getBool(String key) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getBool(key) ?? false;
  }

  Future<bool> setBool(String key, bool value) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.setBool(key, value);
  }


  Future<bool> clearData() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return await prefs.clear();
  }

}
