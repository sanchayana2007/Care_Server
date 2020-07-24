import 'dart:io';
import 'package:flutter/foundation.dart' show kIsWeb;


class BuildConfig {

  static var mainApiId = 'medservice.app.user.in';

  static final timeZoneOffset =
      new DateTime.now().timeZoneOffset.inMicroseconds;
  static var signedInAppId = '';
  static var databaseSchema = '_04_03_2020.db';
  static var serverUrl = 'https://medix.xlayer.in';
  static var xOriginKey =
      'gAAAAABeka_J124HZJ0ERgFU_K7L3HeMFCUMaqRXuPd0SaaBzO09BdndXhZPROmE2DKwMqvWbGEiAtbIe1BVRAC_olGghhy9rM8j6ztXt5xOpwuI_SjMywQ=';
  static var xApiKey = '';
  static var xAuthorization = '';

  static isAndroid() {
    try {
      if (Platform.isAndroid) {
        return true;
      } else {
        return false;
      }
    } catch (e) {
      return false;
    }
  }
  static isIOS() {
    try {
      if (Platform.isIOS) {
        return true;
      } else {
        return false;
      }
    } catch (e) {
      return false;
    }
  }

  static isWeb() {
    try {
      if (kIsWeb) {
        return true;
      } else {
        return false;
      }
    } catch (e) {
      return false;
    }
  }

}
