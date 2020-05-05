import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:medservice/authorization/signIn.dart';
import 'package:medservice/authorization/verifyOTP.dart';
import 'package:medservice/handler/build_config.dart';
import 'package:medservice/handler/http_request_handler.dart';
import 'package:medservice/handler/shared_pref_handler.dart';
import 'package:medservice/util/log_util.dart';
import 'package:medservice/util/toast_util.dart';

class SignUpPage extends StatefulWidget {
  @override
  _SignUpPage createState() => new _SignUpPage();
}

class _SignUpPage extends State<SignUpPage> {

  String TAG = 'SignUpPage';
  BuildContext _context;
  HttpRequestHandler httpRequestHandler;
  SharedPrefHandler sharedPrefHandler;
  final signUpFirstName = TextEditingController();
  final signUpLastName = TextEditingController();
  final signUpMobileNumber = TextEditingController();
  final signUpEmail = TextEditingController();

  _SignUpPage() {
    httpRequestHandler = new HttpRequestHandler();
    sharedPrefHandler = new SharedPrefHandler();
  }

  initSignUpRequest() async {
    Object body = {
      "firstName": signUpFirstName.text,
      "lastName": signUpLastName.text,
      "phoneNumber": signUpMobileNumber.text,
      "countryCode": 91,
      "email": signUpEmail.text,
      "method": 2,
      "applicationId": BuildConfig.mainApiId,
    };
    var resp = await httpRequestHandler.authSignUp(body);
    try {
      Log.i(resp);
      if (resp['status']) {
        Toaster.s(message: resp['message']);
        Navigator.of(_context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => VerifyOtpPage(
              signUpMobileNumber.text.toString(),
              2,
            ),
          ),
        );
      } else {
        Toaster.e(message: resp['message']);
      }
    } catch (e) {
      Toaster.e(message: 'Internal Server Response');
    }
  }

  @override
  Widget build(BuildContext context) {
    _context = context;
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
                          "assets/logo.png",
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
                        padding:
                            EdgeInsets.only(left: 16.0, right: 16.0, top: 16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: <Widget>[
                            Text("Sign Up",
                                style: TextStyle(
                                    fontSize:
                                        ScreenUtil.getInstance().setSp(30),
                                    fontFamily: "Poppins-Bold",
                                    letterSpacing: .6)),
                            SizedBox(
                              height: ScreenUtil.getInstance().setHeight(30),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(
                                  top: 0,
                                  left: 15.0,
                                  right: 15.0,
                                  bottom: 15.0),
                              child: Theme(
                                data: ThemeData(
                                  primaryColor: Colors.black,
                                ),
                                child: Column(
                                  children: <Widget>[
                                    TextField(
                                      decoration: InputDecoration(
                                          hintStyle: TextStyle(
                                              color: Colors.black, fontSize: 12.0),
                                          border: OutlineInputBorder(
                                              borderSide:
                                                  BorderSide(color: Colors.black)),
                                          labelText: "First Name",
                                          labelStyle:
                                              TextStyle(color: Colors.black)),
                                      controller: signUpFirstName,
                                      maxLength: 40,
                                      keyboardType: TextInputType.text,
                                      style: TextStyle(fontSize: 16),
                                    ),
                                    TextField(
                                      decoration: InputDecoration(
                                          hintStyle: TextStyle(
                                              color: Colors.black, fontSize: 12.0),
                                          border: OutlineInputBorder(
                                              borderSide:
                                                  BorderSide(color: Colors.black)),
                                          labelText: "Last Name",
                                          labelStyle:
                                              TextStyle(color: Colors.black)),
                                      controller: signUpLastName,
                                      maxLength: 40,
                                      keyboardType: TextInputType.text,
                                      style: TextStyle(fontSize: 16),
                                    ),
                                    TextField(
                                      decoration: InputDecoration(
//                  hintText: "Mobile Number",
                                          hintStyle: TextStyle(
                                              color: Colors.black, fontSize: 12.0),
                                          border: OutlineInputBorder(
                                              borderSide:
                                                  BorderSide(color: Colors.black)),
                                          labelText: "Phone Number",
                                          labelStyle:
                                              TextStyle(color: Colors.black)),
                                      controller: signUpMobileNumber,
                                      maxLength: 10,
                                      keyboardType: TextInputType.phone,
                                      style: TextStyle(fontSize: 16),
                                    ),
                                    TextField(
                                      decoration: InputDecoration(
//                  hintText: "Mobile Number",
                                          hintStyle: TextStyle(
                                              color: Colors.black, fontSize: 12.0),
                                          border: OutlineInputBorder(
                                              borderSide:
                                                  BorderSide(color: Colors.black)),
                                          labelText: "Email ( Optional )",
                                          labelStyle:
                                              TextStyle(color: Colors.black)),
                                      controller: signUpEmail,
                                      maxLength: 40,
                                      keyboardType: TextInputType.emailAddress,
                                      style: TextStyle(fontSize: 16),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            SizedBox(
                              height: ScreenUtil.getInstance().setHeight(20),
                            )
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
                            width: ScreenUtil.getInstance().setWidth(300),
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
                                  initSignUpRequest();
                                },
                                child: Center(
                                  child: Text("Next",
                                      style: TextStyle(
                                          color: Colors.white,
                                          fontFamily: "Poppins-Bold",
                                          fontSize: 18,
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
    Navigator.of(_context).pushReplacement(
      MaterialPageRoute(builder: (context) => SignInPage()),
    );
    signUpFirstName.text = "";
    signUpLastName.text = "";
    signUpMobileNumber.text = "";
    signUpEmail.text = "";
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
