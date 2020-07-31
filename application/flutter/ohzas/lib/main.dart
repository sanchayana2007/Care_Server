import 'dart:async';
import 'package:flutter/services.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:ohzas/app-state/default/app_home_page.dart';
import 'package:ohzas/authorization/signIn.dart';
import 'package:ohzas/handler/build_config.dart';
import 'package:ohzas/handler/shared_pref_handler.dart';
import 'package:ohzas/util/log_util.dart';
import 'package:ohzas/handler/network_handler.dart';
import 'package:ohzas/handler/http_request_handler.dart';
import 'package:package_info/package_info.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:get_version/get_version.dart';
import 'package:firebase_analytics/firebase_analytics.dart';



Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  ThemeData themeData = new ThemeData(
    primaryColor: Colors.white,
    accentColor: Colors.deepOrangeAccent,
    cursorColor: Colors.black,
    hintColor: Colors.green,
    fontFamily: "Poppins-Regular",
  );
  runApp(
    MaterialApp(
      debugShowCheckedModeBanner: true,
      theme: themeData,
      home: SplashScreen(),
    ),
  );
}

class SplashScreen extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _SplashScreen();
  }
}

class _SplashScreen extends State<SplashScreen> {
  bool exit = true;
  BuildContext _context;
  HttpRequestHandler httpRequestHandler;

  intTimer() async {
    Timer.periodic(
      Duration(seconds: 3),
      (Timer t) {
        t.cancel();
        if (exit) {
          setState(() {
            exit = false;
          });
          onExit();
        }
      },
    );
  }

  onExit() async {
    String apiId = await getSignedInData();
    if (apiId == null || apiId.isEmpty) {
      Navigator.of(_context).pushReplacement(
        MaterialPageRoute(builder: (context) => SignInPage()),
      );
    } else {
      Navigator.of(_context).pushReplacement(
        MaterialPageRoute(builder: (context) => AppHomePage()),
      );
    }
  }

  Future<String> getSignedInData() async {
    SharedPrefHandler sharedPrefHandler = new SharedPrefHandler();
    // TODO: xOrigin Key is Hard Coded.
    BuildConfig.xOriginKey = BuildConfig.xOriginKey;
    BuildConfig.xApiKey =
        await sharedPrefHandler.getString(sharedPrefHandler.xApiKey);
    BuildConfig.xAuthorization =
        await sharedPrefHandler.getString(sharedPrefHandler.xAuthorizationKey);
    Log.i(BuildConfig.xAuthorization);
    return BuildConfig.xAuthorization;
  }

  checkForUpdate() async {
    int projectCode = -1;
    try {
      var _projectCode = await GetVersion.projectCode;
      projectCode = int.parse(_projectCode);
    } catch (e) {
      projectCode = -1;
    }
    if (await NetworkHandler.isOnlineWithToast(_context)) {
      var resp =
          await httpRequestHandler.getCheckForUpdate(BuildConfig.mainApiId);
      try {
        if (resp['status'] && resp['result'][0] > projectCode) {
          Log.i('Checking For Update');
          updateWindow();
          return;
        }
      } catch (e) {
        Log.e(e);
      }
      intTimer();
    } else {
      exitApp();
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_context == null) {
      _context = context;
      httpRequestHandler = new HttpRequestHandler(context);
      checkForUpdate();
    }

    //intTimer();
    return Scaffold(
      body: Stack(
        children: <Widget>[
          Container(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Image.asset(
                      'assets/logo.jpg',
                      height: 150,
                    ),
                  ],
                ),
                SizedBox(
                  height: 20,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Text(
                      "",
                      style: TextStyle(
                        fontSize: 22,
                        fontFamily: "Poppins-Bold",
                        letterSpacing: .6,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Container(
            width: MediaQuery.of(context).size.width,
            alignment: Alignment.bottomCenter,
            margin: EdgeInsets.only(bottom: 30),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                Text(
                  'Powered By',
                  style: TextStyle(
                      fontFamily: "Poppins-Regular",
                      fontSize: 14,
                      color: Colors.blueGrey),
                ),
                SizedBox(
                  width: 10,
                ),
                Container(
                  height: 30,
                  width: 1,
                  color: Colors.grey,
                ),
                Container(
                  child: Image.asset(
                    'assets/xlayer_logo_v2.png',
                    height: 48,
                  ),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }

  exitApp() {
    if (BuildConfig.isAndroid()) {
      SystemNavigator.pop();
    }
  }

  Future<bool> updateWindow() async {
    return (await showDialog(
          context: _context,
          builder: (context) => new AlertDialog(
            title: new Text("A new update is now available."),
            actions: <Widget>[
              new FlatButton(
                onPressed: () {
                  // initTimer();
                  exitApp();
                },
                child: new Text('Not Now'),
              ),
              new FlatButton(
                onPressed: () {
                  _launchURL();
                  exitApp();
                },
                child: new Text('Update'),
              ),
            ],
          ),
        )) ??
        false;
  }

  _launchURL() async {
    String appUrl = 'https://www.ohzas.com/';
    if (BuildConfig.isAndroid()) {
      appUrl =
          'https://play.google.com/store/apps/details?id=com.xlayer.med.ohzas';
    }
    if (await canLaunch(appUrl)) {
      await launch(appUrl);
    } else {
      throw 'Could not launch $appUrl';
    }
  }
}
