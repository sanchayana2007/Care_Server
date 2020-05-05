
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';

class Toaster {

  static w({String message = ''}) {
    Fluttertoast.showToast(
      msg: message,
      toastLength: Toast.LENGTH_LONG,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIos: 1,
      backgroundColor: Colors.yellow[400],
      textColor: Colors.red,
      fontSize: 16.0,
    );
  }

  static s({String message = ''}) {
    Fluttertoast.showToast(
      msg: message,
      toastLength: Toast.LENGTH_LONG,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIos: 1,
      backgroundColor: Colors.green[500],
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }

  static e({String message = ''}) {
    Fluttertoast.showToast(
      msg: message,
      toastLength: Toast.LENGTH_LONG,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIos: 1,
      backgroundColor: Colors.redAccent,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }

  static i({String message = ''}) {
    Fluttertoast.showToast(
      msg: message,
      toastLength: Toast.LENGTH_LONG,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIos: 1,
      backgroundColor: Colors.blueAccent,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }

}