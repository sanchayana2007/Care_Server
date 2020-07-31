import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:ohzasProvider/authorization/signUp.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:ohzasProvider/authorization/signIn.dart';
import 'package:ohzasProvider/authorization/verifyOTP.dart';
import 'package:ohzasProvider/handler/build_config.dart';
import 'package:ohzasProvider/handler/http_request_handler.dart';
import 'package:ohzasProvider/handler/shared_pref_handler.dart';
import 'package:ohzasProvider/util/log_util.dart';
import 'package:ohzasProvider/util/toast_util.dart';

class SignUpFailPage extends StatefulWidget {
  @override
  _SignUpFailPage createState() => new _SignUpFailPage();
}

class _SignUpFailPage extends State<SignUpFailPage> {

  String TAG = 'SignUpFailPage';
  BuildContext _context;
  HttpRequestHandler httpRequestHandler;
  SharedPrefHandler sharedPrefHandler;

  _SignUpFailPage() {    
    sharedPrefHandler = new SharedPrefHandler();
  }

  @override
  Widget build(BuildContext context) {
    _context = context;
    httpRequestHandler = new HttpRequestHandler(context);
    ScreenUtil.instance = ScreenUtil.getInstance()..init(context);
    ScreenUtil.instance =
        ScreenUtil(width: 750, height: 1334, allowFontScaling: true);
    return new WillPopScope(
      onWillPop: _onWillPop,
      child: new Scaffold(
        backgroundColor: Colors.white,
        resizeToAvoidBottomPadding: true,
        body: Stack(
          fit: StackFit.expand,
          children: <Widget>[
            Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Expanded(
                  child: Container(),
                ),
                Image.asset(
                  "assets/image_02.png",
                  color: Colors.black,
                )
              ],
            ),
            SingleChildScrollView(
              child: Padding(
                padding: EdgeInsets.only(
                  left: 28.0,
                  right: 28.0,
                  top: 40.0,
                ),
                child: Column(
                  children: <Widget>[
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Image.asset(
                          "assets/logo.jpg",
                          width: ScreenUtil.getInstance().setWidth(250),
                          height: ScreenUtil.getInstance().setHeight(150),
                        )
                      ],
                    ),
                    SizedBox(
                      height: ScreenUtil.getInstance().setHeight(10),
                    ),
                    Container(
                      width: double.infinity,
                      decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(8.0),
                          boxShadow: [
                            BoxShadow(
                                color: Colors.black12,
                                offset: Offset(0.0, 15.0),
                                blurRadius: 15.0),
                            BoxShadow(
                                color: Colors.black12,
                                offset: Offset(0.0, -10.0),
                                blurRadius: 10.0),
                          ]),
                      child: Padding(
                        padding: EdgeInsets.only(left: 16.0, right: 16.0, top: 40.0, bottom:10.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: <Widget>[
                            Text("The phone number which you have entered is not registered in the 'OHZAS' app. Please register it using the button below.",
                                style: TextStyle(
                                    fontSize:
                                      ScreenUtil.getInstance().setSp(35),
                                    fontFamily: "Poppins-Bold",
                                    letterSpacing: .1)),
                            Text("\nआपने जो फ़ोन नंबर दर्ज किया है, वह 'ओजस' ऐप में पंजीकृत नहीं है। कृपया नीचे दिए गए बटन का उपयोग करके इसे पंजीकृत करें।",
                                style: TextStyle(
                                    fontSize:
                                      ScreenUtil.getInstance().setSp(35),
                                    fontFamily: "Poppins-Bold",
                                    letterSpacing: .6)),
                            SizedBox(
                              height: ScreenUtil.getInstance().setHeight(30),
                            ),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(height: ScreenUtil.getInstance().setHeight(40)),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        InkWell(
                          child: Container(
                            width: ScreenUtil.getInstance().setWidth(430),
                            height: ScreenUtil.getInstance().setHeight(100),
                            decoration: BoxDecoration(
                                gradient: LinearGradient(
                                    colors: [Colors.deepOrange[200], Colors.deepOrange]),
                                borderRadius: BorderRadius.circular(6.0),
                                boxShadow: [
                                  BoxShadow(
                                      color: Color(0xFF6078ea).withOpacity(.3),
                                      offset: Offset(0.0, 8.0),
                                      blurRadius: 8.0)
                                ]),
                            child: Material(
                              color: Colors.transparent,
                              child: InkWell(
                                onTap: () {
                              Navigator.of(context).pushReplacement(
                                  MaterialPageRoute(
                                      builder: (context) => SignUpPage()),
                              );
                            },
                                child: Center(
                                  child: Text("Sign-Up / रजिस्टर करें",
                                      style: TextStyle(
                                          color: Colors.white,
                                          fontFamily: "Poppins-Bold",
                                          fontSize: 16,
                                          letterSpacing: 1.0)),
                                ),
                              ),
                            ),
                          ),
                        )
                      ],
                    ),
                    SizedBox(
                      height: ScreenUtil.getInstance().setHeight(10),
                    ),
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  goBack() {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => SignInPage()),
      );
  }

  Future<bool> _onWillPop() async {
    return (await showDialog(
          context: context,
          builder: (context) => new AlertDialog(
            title: new Text('Do you want to go back?'),
            content: new Text(''),
            actions: <Widget>[
              new FlatButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: new Text('No'),
              ),
              new FlatButton(
                onPressed: () => {goBack()},
                child: new Text('Yes'),
              ),
            ],
          ),
        )) ??
        false;
  }
}
