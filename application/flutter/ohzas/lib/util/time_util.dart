import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:ohzas/handler/build_config.dart';
import 'package:ohzas/util/log_util.dart';

class TimeUtil {
  // ignore: non_constant_identifier_names
  static String TAG = 'TIME-UTIL';

  static String getStringTimeFromIntTime(
      {int timeInMicroSeconds = 0,
      String dateFormat = '',
      int timeZoneOffset = 0}) {
    String stringTime = '';
    try {
      if (timeZoneOffset == -1) {
        // Adding Default Time Zone offset
        timeZoneOffset = BuildConfig.timeZoneOffset;
      }
      timeInMicroSeconds = (timeInMicroSeconds + timeZoneOffset).round();
      DateTime dateTime =
          new DateTime.fromMicrosecondsSinceEpoch(timeInMicroSeconds);
      stringTime = new DateFormat(dateFormat).format(dateTime);
    } catch (e) {
      Log.w(TAG, e);
    }
    return stringTime;
  }

  static int getIntTimeFromStringTime(
      {String timeInString = '',
      String dateFormat = '',
      int timeZoneOffset = 0}) {
    int intTime = 0;
    try {
      if (timeZoneOffset == -1) {
        // Adding Default Time Zone offset
        timeZoneOffset = BuildConfig.timeZoneOffset;
      }
      DateTime dateTime = DateTime.parse(timeInString);
      intTime = dateTime.microsecondsSinceEpoch;
      intTime = (intTime + timeZoneOffset).round();
    } catch (e) {
      Log.w(TAG, e);
    }
    return intTime;
  }

  static int timeNow() {
    return new DateTime.now().microsecondsSinceEpoch;
  }

  static convert12StringTo24String({String timeIn12Hour = '', String inputFormat = '', String outputFormat = ''}) {
    String hour24inString = '';
    try {
      DateTime date2 = DateFormat(inputFormat).parse(timeIn12Hour);
      hour24inString = DateFormat(outputFormat).format(date2);
    } catch (e) {
      hour24inString = '';
    }
    return hour24inString;
  }
}
