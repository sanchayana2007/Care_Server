import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:ohzasProvider/app-state/default/app_home_page.dart';
import 'package:ohzasProvider/authorization/signIn.dart';
import 'package:ohzasProvider/handler/build_config.dart';
import 'package:ohzasProvider/handler/shared_pref_handler.dart';
import 'package:ohzasProvider/util/log_util.dart';

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

  @override
  Widget build(BuildContext context) {
    _context = context;
    intTimer();
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
}
