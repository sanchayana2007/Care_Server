import 'dart:io';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:ohzas/util/log_util.dart';
import 'package:ohzas/util/toast_util.dart';

class NetworkHandler {
  
  static Future<bool> isOnline() async {
    try {
      if (Platform.isAndroid || Platform.isIOS) {
        var connectivityResult = await (Connectivity().checkConnectivity());
        if (connectivityResult == ConnectivityResult.mobile) {
          // I am connected to a mobile network.
          return true;
        } else if (connectivityResult == ConnectivityResult.wifi) {
          // I am connected to a wifi network.
          return true;
        }
      }
    } catch (e) {
      Log.w(e);
    }
    return true;
  }

  static Future<bool> isOnlineWithToast(BuildContext context) async {
    try {
      if (Platform.isAndroid || Platform.isIOS) {
        var connectivityResult = await (Connectivity().checkConnectivity());
        if (connectivityResult == ConnectivityResult.mobile) {
          // I am connected to a mobile network.
          return true;
        } else if (connectivityResult == ConnectivityResult.wifi) {
          // I am connected to a wifi network.
          return true;
        }
        Toaster.e(context, message: 'Internet connection is not available.');
        return false;
      } else {
        return true;
      }
    } catch (e) {
      Log.w(e);
    }
    return true;
  }
}
