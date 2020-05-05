
import 'package:flutter/material.dart';
import 'package:toast/toast.dart';
// import 'package:fluttertoast/fluttertoast.dart';

class Toaster {

  static w(BuildContext buildContext, {String message = ''}) {
    // Fluttertoast.showToast(
    //   msg: message,
    //   toastLength: Toast.LENGTH_LONG,
    //   gravity: ToastGravity.BOTTOM,
    //   timeInSecForIos: 1,
    //   backgroundColor: Colors.blueAccent,
    //   textColor: Colors.white,
    //   fontSize: 16.0,
    // );
    if (buildContext == null) {
      return;
    }
    Toast.show(
      message, 
      buildContext, 
      duration: Toast.LENGTH_SHORT, 
      gravity:  Toast.BOTTOM,
      backgroundColor: Colors.yellow[700],
      textColor: Colors.redAccent,
    );
  }

  static s(BuildContext buildContext, {String message = ''}) {
    // Fluttertoast.showToast(
    //   msg: message,
    //   toastLength: Toast.LENGTH_LONG,
    //   gravity: ToastGravity.BOTTOM,
    //   timeInSecForIos: 1,
    //   backgroundColor: Colors.blueAccent,
    //   textColor: Colors.white,
    //   fontSize: 16.0,
    // );
    if (buildContext == null) {
      return;
    }
    Toast.show(
      message, 
      buildContext, 
      duration: Toast.LENGTH_SHORT, 
      gravity:  Toast.BOTTOM,
      backgroundColor: Colors.green[500],
      textColor: Colors.white,
    );
  }

  static e(BuildContext buildContext, {String message = ''}) {
    // Fluttertoast.showToast(
    //   msg: message,
    //   toastLength: Toast.LENGTH_LONG,
    //   gravity: ToastGravity.BOTTOM,
    //   timeInSecForIos: 1,
    //   backgroundColor: Colors.blueAccent,
    //   textColor: Colors.white,
    //   fontSize: 16.0,
    // );
    if (buildContext == null) {
      return;
    }
    Toast.show(
      message, 
      buildContext, 
      duration: Toast.LENGTH_SHORT, 
      gravity:  Toast.BOTTOM,
      backgroundColor: Colors.redAccent,
      textColor: Colors.white,
    );
  }

  static i(BuildContext buildContext, {String message = ''}) {
    // Fluttertoast.showToast(
    //   msg: message,
    //   toastLength: Toast.LENGTH_LONG,
    //   gravity: ToastGravity.BOTTOM,
    //   timeInSecForIos: 1,
    //   backgroundColor: Colors.blueAccent,
    //   textColor: Colors.white,
    //   fontSize: 16.0,
    // );
    if (buildContext == null) {
      return;
    }
    Toast.show(
      message, 
      buildContext, 
      duration: Toast.LENGTH_SHORT, 
      gravity:  Toast.BOTTOM,
      backgroundColor: Colors.blueAccent,
      textColor: Colors.white,
    );
  }

}