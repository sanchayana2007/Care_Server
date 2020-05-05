
import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';

class NetworkHandler {
  static Future<bool> isOnline() async {
    var connectivityResult = await (Connectivity().checkConnectivity());
    if (connectivityResult == ConnectivityResult.mobile) {
      // I am connected to a mobile network.
      return true;
    } else if (connectivityResult == ConnectivityResult.wifi) {
      // I am connected to a wifi network.
      return true;
    }
    return false;
  }

  static Future<bool> isOnlineWithToast() async {
    var connectivityResult = await (Connectivity().checkConnectivity());
    if (connectivityResult == ConnectivityResult.mobile) {
      // I am connected to a mobile network.
      return true;
    } else if (connectivityResult == ConnectivityResult.wifi) {
      // I am connected to a wifi network.
      return true;
    }
    Fluttertoast.showToast(
      msg: 'Internet connection is not available.',
      toastLength: Toast.LENGTH_SHORT,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIos: 5,
      backgroundColor: Colors.yellow[500],
      textColor: Colors.red,
      fontSize: 16.0,
    );
    return false;
  }

}