import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:ohzas/authorization/signUp.dart';
import 'package:ohzas/authorization/verifyOTP.dart';
import 'package:ohzas/handler/build_config.dart';
import 'package:ohzas/handler/http_request_handler.dart';
import 'package:ohzas/handler/network_handler.dart';
import 'package:ohzas/util/log_util.dart';
import 'package:ohzas/util/toast_util.dart';
import 'package:toast/toast.dart';
import 'package:ohzas/authorization/signUpFail.dart';
import 'package:url_launcher/url_launcher.dart';

class SignInPage extends StatefulWidget {
  @override
  _SignInPage createState() => new _SignInPage();
}

class _SignInPage extends State<SignInPage> {
  BuildContext _context;
  final signInMobileNumber = TextEditingController();

  HttpRequestHandler _requestHandler;

  _SignInPage() {}

  initSignInRequest() async {
    if (signInMobileNumber.text.length == 0) {
      Toaster.e(context, message: 'Please enter your Phone Number.');
      return;
    }
    Object body = {
      "phoneNumber": signInMobileNumber.text.toString(),
      "countryCode": 91,
      "method": 1,
      "applicationId": BuildConfig.mainApiId
    };
    var resp = await _requestHandler.authSignIn(body);
    try {
      Log.i(resp);
      if (resp['status']) {
        Toaster.s(context, message: resp['message']);
        Navigator.of(_context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => VerifyOtpPage(
              signInMobileNumber.text.toString(),
              1,
            ),
          ),
        );
      } else {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => SignUpFailPage()),
        );
        //Toaster.e(context, message: resp['message']);
      }
    } catch (e) {
      Toaster.e(context, message: 'Internal Server Response');
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
              crossAxisAlignment: CrossAxisAlignment.end,
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
                padding: EdgeInsets.only(left: 28.0, right: 28.0, top: 60.0),
                child: Column(
                  children: <Widget>[
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Image.asset(
                          "assets/logo.jpg",
                          width: ScreenUtil.getInstance().setWidth(250),
                          height: ScreenUtil.getInstance().setHeight(250),
                        )
                      ],
                    ),
                    SizedBox(
                      height: ScreenUtil.getInstance().setHeight(80),
                    ),
                    new Container(
                      width: double.infinity,
//      height: ScreenUtil.getInstance().setHeight(600),
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
                            Text("Sign In",
                                style: TextStyle(
                                    fontSize:
                                        ScreenUtil.getInstance().setSp(35),
                                    fontFamily: "Poppins-Bold",
                                    letterSpacing: .6)),
                            SizedBox(
                              height: ScreenUtil.getInstance().setHeight(30),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(
                                  top: 10, left: 15, right: 15),
                              child: Theme(
                                data: ThemeData(
                                  primaryColor: Colors.black,
                                  accentColor: Colors.black,
                                  cursorColor: Colors.black,
                                ),
                                child: TextField(
                                  decoration: InputDecoration(
                                    hintStyle: TextStyle(
                                        color: Colors.grey, fontSize: 12.0),
                                    border: OutlineInputBorder(
                                      borderSide: BorderSide(
                                        color: Colors.black,
                                      ),
                                    ),
                                    labelText: "Phone Number",
                                    labelStyle: TextStyle(
                                        color: Colors.black, fontSize: 18),
                                  ),
                                  controller: signInMobileNumber,
                                  maxLength: 10,
                                  keyboardType: TextInputType.phone,
                                  style: TextStyle(fontSize: 20),
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
                        InkWell(
                          child: Container(
                            width: ScreenUtil.getInstance().setWidth(300),
                            height: ScreenUtil.getInstance().setHeight(60),
                            decoration: BoxDecoration(
                                gradient: LinearGradient(colors: [
                                  Colors.deepOrange[200],
                                  Colors.deepOrange[500]
                                ]),
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
                                  initSignInRequest();
                                },
                                child: Center(
                                  child: Text(
                                    "Next",
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontFamily: "Poppins-Bold",
                                      fontSize: 18,
                                      letterSpacing: 1.0,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        )
                      ],
                    ),
                    SizedBox(
                      height: ScreenUtil.getInstance().setHeight(60),
                    ),
                    Container(
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          Text(
                            "Don't have any Account ? ",
                            style: TextStyle(
                              fontFamily: "Poppins-Medium",
                              fontSize: 16,
                              fontWeight: FontWeight.normal,
                              color: Colors.black,
                            ),
                          ),
                          InkWell(
                            onTap: () {
                              Navigator.of(context).pushReplacement(
                                MaterialPageRoute(
                                    builder: (context) => SignUpPage()),
                              );
                            },
                            child: Container(
                              decoration: new BoxDecoration(
                                  color: Colors.deepOrange[700],
                                  borderRadius: new BorderRadius.circular(5)),
                              padding:
                                  const EdgeInsets.only(left: 14, right: 14),
                              child: Text("Sign Up",
                                  style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 15,
                                      fontWeight: FontWeight.bold,
                                      fontFamily: "Poppins-Bold")),
                            ),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(
                      height: ScreenUtil.getInstance().setHeight(60),
                    ),
                    Container(
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          InkWell(
                            onTap: () => launch("tel://9740547920"),
                            child: Container(
                              decoration: new BoxDecoration(
                                  color: Colors.greenAccent[700],
                                  borderRadius: new BorderRadius.circular(5)),
                              padding: const EdgeInsets.only(
                                  left: 8, right: 8, top: 8, bottom: 8),
                              child: Text("Call Us / हमें कॉल करें",
                                  style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                      fontFamily: "Poppins-Bold")),
                            ),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(
                      height: ScreenUtil.getInstance().setHeight(140),
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

  Future<bool> _onWillPop() async {
    return (await showDialog(
          context: _context,
          builder: (context) => new AlertDialog(
            title: new Text('Do you want to go back?'),
            content: new Text(''),
            actions: <Widget>[
              new FlatButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: new Text('No'),
              ),
              new FlatButton(
                onPressed: () => Navigator.of(context).pop(true),
                child: new Text('Yes'),
              ),
            ],
          ),
        )) ??
        false;
  }
}
