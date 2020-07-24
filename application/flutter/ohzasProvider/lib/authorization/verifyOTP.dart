// Library Imports
import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:ohzasProvider/app-state/default/app_home_page.dart';
import 'package:ohzasProvider/authorization/signIn.dart';
import 'package:ohzasProvider/handler/build_config.dart';
import 'package:ohzasProvider/handler/http_request_handler.dart';
import 'package:ohzasProvider/handler/shared_pref_handler.dart';
import 'package:ohzasProvider/util/log_util.dart';
import 'package:ohzasProvider/util/toast_util.dart';
import 'signUp.dart';

var pageParent = 0;

class VerifyOtpPage extends StatefulWidget {
  final parent;
  final signedPhoneNumber;
  VerifyOtpPage(this.signedPhoneNumber, this.parent);

  @override
  _VerifyOtpPage createState() => new _VerifyOtpPage();
}

class _VerifyOtpPage extends State<VerifyOtpPage> {

  HttpRequestHandler _requestHandler;
  SharedPrefHandler _prefHandler;

  _VerifyOtpPage() {
    _prefHandler = new SharedPrefHandler();
  }

  BuildContext _context;
  final verifyOtp = TextEditingController();


  initVerifyRequest() async {
    Object body = {
      "phoneNumber": widget.signedPhoneNumber,
      "countryCode": 91,
      "method": 1,
      'otp': verifyOtp.text.toString(),
      "applicationId": BuildConfig.mainApiId
    };
    var resp = await _requestHandler.authVerify(body);
    try {
      Log.i(resp);
      if (resp['status']) {
        Toaster.s(context, message: resp['message']);
        onSignInSuccess(resp['result'][0]);
      } else {
        Toaster.e(context, message: resp['message']);
      }
    } catch (e) {
      Toaster.e(context, message: 'Internal Server Response');
    }
  }

  onSignInSuccess(Map resp) async {
    try {
      await _prefHandler.setString(_prefHandler.xApiKey, resp['apiKey']);
      await _prefHandler.setString(_prefHandler.xOriginKey, BuildConfig.xOriginKey);
      await _prefHandler.setString(_prefHandler.xAuthorizationKey, resp['bearerToken']);
      Navigator.of(_context).pushReplacement(
        MaterialPageRoute(
          builder: (context) => AppHomePage(),
        ),
      );
    } catch (e) {
      Toaster.e(context, message: 'Internal Error: Code 2212');
      await _prefHandler.clearData();
    }
  }

  @override
  Widget build(BuildContext context) {
    _context = context;
    _requestHandler = new HttpRequestHandler(context);
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
              children: <Widget>[
                Expanded(
                  child: Container(),
                ),
                Image.asset(
                  'assets/image_02.png',
                  color: Colors.black,
                )
              ],
            ),
            SingleChildScrollView(
              child: Padding(
                padding: EdgeInsets.only(left: 28.0, right: 28.0, top: 60.0),
                child: Column(
                  children: <Widget>[
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Image.asset(
                          'assets/logo.jpg',
                          width: ScreenUtil.getInstance().setWidth(250),
                          height: ScreenUtil.getInstance().setHeight(250),
                        )
                      ],
                    ),
                    SizedBox(
                      height: ScreenUtil.getInstance().setHeight(40),
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
                        padding: EdgeInsets.only(left: 16.0, right: 16.0, top: 16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: <Widget>[
                            Text("Verify OTP",
                                style: TextStyle(
                                    fontSize:
                                      ScreenUtil.getInstance().setSp(35),
                                    fontFamily: "Poppins-Bold",
                                    letterSpacing: .6)),
                            SizedBox(
                              height: ScreenUtil.getInstance().setHeight(30),
                            ),
                            Padding(
                              padding: const EdgeInsets.all(15.0),
                              child: Theme(
                                data: ThemeData(
                                  primaryColor: Colors.black,
                                  cursorColor: Colors.black,
                                ),
                                child: TextField(
                                  decoration: InputDecoration(
                                      hintStyle: TextStyle(color: Colors.black, fontSize: 12.0),
                                      border: OutlineInputBorder(
                                          borderSide: BorderSide(color: Colors.black)),
                                      labelText: "One Time Password (OTP).",
                                      labelStyle: TextStyle(color: Colors.black)),
                                  controller: verifyOtp,
                                  maxLength: 6,
                                  keyboardType: TextInputType.phone,
                                  style: TextStyle(fontSize: 18),
                                ),
                              ),
                            ),
                            SizedBox(
                              height: ScreenUtil.getInstance().setHeight(80),
                            ),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(height: ScreenUtil.getInstance().setHeight(40)),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Visibility(
                          visible: false,
                          child: InkWell(
                            child: Container(
//                            width: ScreenUtil.getInstance().setWidth(300),
                              height: ScreenUtil.getInstance().setHeight(80),
                              decoration: BoxDecoration(
                                  gradient: LinearGradient(
                                      colors: [Colors.deepOrange[100], Colors.deepOrange]),
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
                                    initVerifyRequest();
                                  },
                                  child: Center(
                                    child: Text('Resend Sms',
                                        style: TextStyle(
                                            color: Colors.white,
                                            fontFamily: 'Poppins-Bold',
                                            fontSize: 18,
                                            letterSpacing: 1.0)),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                        InkWell(
                          child: Container(
                            width: ScreenUtil.getInstance().setWidth(300),
                            height: ScreenUtil.getInstance().setHeight(60),
                            decoration: BoxDecoration(
                                gradient: LinearGradient(
                                    colors: [Colors.deepOrange[100], Colors.deepOrange]),
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
                                  initVerifyRequest();
                                },
                                child: Center(
                                  child: Text('Verify',
                                      style: TextStyle(
                                          color: Colors.white,
                                          fontFamily: 'Poppins-Bold',
                                          fontSize: 16,
                                          letterSpacing: 1.0,
                                      ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(
                      height: ScreenUtil.getInstance().setHeight(40),
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
    verifyOtp.text = '';
    if (widget.parent == 1) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => SignInPage()),
      );
    } else if (widget.parent == 2) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => SignUpPage()),
      );
    } else {
      Navigator.of(context).pop(true);
    }
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
