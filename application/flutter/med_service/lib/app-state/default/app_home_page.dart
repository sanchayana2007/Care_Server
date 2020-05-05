import 'dart:convert';
import 'dart:math';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:medservice/app-state/about_page.dart';
import 'package:medservice/app-state/default/service_book_history_page.dart';
import 'package:medservice/app-state/default/service_book_page.dart';
import 'package:medservice/authorization/signIn.dart';
import 'package:medservice/handler/http_request_handler.dart';
import 'package:medservice/handler/network_handler.dart';
import 'package:medservice/handler/shared_pref_handler.dart';
import 'package:medservice/util/log_util.dart';
import 'package:medservice/util/toast_util.dart';

class AppHomePage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _AppHomePage();
  }
}

class _AppHomePage extends State<AppHomePage> {
  SharedPrefHandler sharedPrefHandler;
  HttpRequestHandler httpRequestHandler;

  _AppHomePage() {
    sharedPrefHandler = new SharedPrefHandler();
    httpRequestHandler = new HttpRequestHandler();
  }

  List<dynamic> serviceList =  [];

  getAllData() async {
    if (!await NetworkHandler.isOnlineWithToast()) {
      var value = await sharedPrefHandler.getString('\$TrstProfile');
      Map<String, dynamic> respJson = jsonDecode(value);
      updateProfileDetails(respJson);
      Log.i('FROM LOCAL CACHE', value);

      var value2 = await sharedPrefHandler.getString('\$serviceList');
      Map<String, dynamic> respJson2 = jsonDecode(value);
      loadServiceList(respJson2);
      Log.i('FROM LOCAL CACHE', value);
    } else {
      httpRequestHandler.getProfile(null).then(
        (value) {
          updateProfileDetails(value);
        },
      );
      var resp = await httpRequestHandler.getServiceList();
      try {
        Log.i(resp);
        if (resp['status']) {
          loadServiceList(resp['result']);
        } else {
          Toaster.e(message: resp['message']);
        }
      } catch (e) {
        Log.i(e);
        Toaster.e(message: 'Invalid Server Response.');
      }
    }
    profileLoaded = false;
  }

  var colorList = [
    Colors.blue,
    Colors.redAccent,
    Colors.yellow[700],
    Colors.indigo,
    Colors.deepOrange,
    Colors.green[600],
    Colors.black,
    Colors.blueGrey[600],
    Colors.purple,
    Colors.deepOrangeAccent,
    Colors.teal[600],
    Colors.indigoAccent,
    Colors.lightGreen,
    Colors.black54
  ];

  loadServiceList(var data) async {
    for (int i = 0; i < data.length; i++) {
      try {
        Map index = data[i];
        if (index['name'] == null || index['name'] == '') {
          index['name'] = 'N/A';
        }
        data[i] = index;
      } catch (e) {
        Log.i('INDEX', i);
        Log.i('DATA', data[i]);
        continue;
      }
    }
    setState(() {
      serviceList = data;
    });
    if (data.length > 0) {
      await sharedPrefHandler.setString('\$serviceList', jsonEncode(data));
    }
  }

  BuildContext _context;
  String TAG = "APP HOME";
  String userName = 'Hi Guest';
  String userEmail = '';
  String userPhoneNumber = "N/A";
  Map profileDetails = {};
  bool profileLoaded = true;

  updateProfileDetails(Map<String, dynamic> value) async {
    try {
      Log.i(TAG, value);
      setState(
        () {
          try {
            profileDetails = value["result"][0];
            userName = value['result'][0]['firstName'] +
                ' ' +
                value['result'][0]['lastName'];
          } catch (e) {
            Log.e(e);
            userName = "N/A";
          }
          try {
            userPhoneNumber =
                value['result'][0]['contact'][0]['value'].toString();
          } catch (e) {
            Log.e('Phone Number', e);
            userPhoneNumber = "N/A";
          }
          try {
            userEmail = value['result'][0]['contact'][1]['value'];
          } catch (e) {
            userEmail = "N/A";
          }
        },
      );
      await sharedPrefHandler.setString('\$TrstProfile', jsonEncode(value));
    } catch (e) {
      Log.i(TAG, e);
    }
  }

  @override
  Widget build(BuildContext context) {
    _context = context;
    if (profileLoaded) {
      getAllData();
    }
    return WillPopScope(
      onWillPop: _onWillPop,
      child: Scaffold(
        appBar: AppBar(
          title: Text('Medix'),
          actions: <Widget>[
            IconButton(
              onPressed: () {
                getAllData();
              },
              icon: Icon(Icons.refresh),
            )
          ],
        ),
        drawer: Drawer(
          child: ListView(
            children: <Widget>[
              UserAccountsDrawerHeader(
                decoration: BoxDecoration(
                  color: Colors.blue[400],
                  image: new DecorationImage(
                    image: new AssetImage('assets/pf_back_1600x900.jpg'),
                    fit: BoxFit.fill,
                  ),
                ),
                accountName: Text(
                  userName,
                  style: TextStyle(
                      fontSize: 16,
                      color: Colors.white,
                      fontWeight: FontWeight.w500),
                ),
                accountEmail: Text(
                  userEmail,
                  style: TextStyle(
                      fontSize: 17,
                      color: Colors.white,
                      fontWeight: FontWeight.w500),
                ),
                currentAccountPicture: GestureDetector(
                  child: CircleAvatar(
                    backgroundColor: Colors.deepOrange[900],
                    child: Icon(
                      Icons.person,
                      color: Colors.white,
                      size: 45,
                    ),
                  ),
                ),
              ),
//              InkWell(
//                onTap: () {
//                  Fluttertoast.showToast(
//                      msg: "You are currently on this page.",
//                      toastLength: Toast.LENGTH_SHORT,
//                      gravity: ToastGravity.BOTTOM,
//                      timeInSecForIos: 1,
//                      backgroundColor: Colors.green[400],
//                      textColor: Colors.white,
//                      fontSize: 16.0);
//                },
//                child: ListTile(
//                  title: Text("My Account"),
//                  leading: Icon(
//                    Icons.account_circle,
//                    color: Colors.black,
//                  ),
//                ),
//              ),
              InkWell(
                onTap: () async {
                  if (await NetworkHandler.isOnlineWithToast()) {
                    Navigator.of(_context).push(MaterialPageRoute(
                        builder: (context) => ServiceBookHistoryPage()));
                  }
                },
                child: ListTile(
                  title: Text("Booking History"),
                  leading: Icon(
                    Icons.assignment,
                    color: Colors.black,
                  ),
                ),
              ),
              Divider(
                color: Colors.grey[600],
              ),
//              InkWell(
//                onTap: () {
//                  Fluttertoast.showToast(
//                      msg: "Coming Soon.",
//                      toastLength: Toast.LENGTH_SHORT,
//                      gravity: ToastGravity.BOTTOM,
//                      timeInSecForIos: 1,
//                      backgroundColor: Colors.yellow[400],
//                      textColor: Colors.red,
//                      fontSize: 16.0);
//                },
//                child: ListTile(
//                  title: Text("Settings"),
//                  leading: Icon(
//                    Icons.settings,
//                    color: Colors.grey[800],
//                  ),
//                ),
//              ),
              InkWell(
                onTap: () {
                  Navigator.of(_context).push(
                    MaterialPageRoute(
                      builder: (context) => AboutPage(),
                    ),
                  );
                },
                child: ListTile(
                  title: Text("About"),
                  leading: Icon(
                    Icons.help,
                    color: Colors.blue,
                  ),
                ),
              ),
              Divider(
                color: Colors.grey[600],
              ),
              InkWell(
                onTap: () async {
                  await sharedPrefHandler.clearData();
                  Toaster.e(message: 'Signing Out, Please Wait.');
                  Navigator.of(context).pushReplacement(MaterialPageRoute(
                    builder: (context) => SignInPage(),
                  ));
                },
                child: ListTile(
                  title: Text("Sign Out"),
                  leading: Icon(
                    Icons.power_settings_new,
                    color: Colors.grey[800],
                  ),
                ),
              ),
            ],
          ),
        ),
        body: Container(
          color: Colors.white,
          child: Column(
            children: <Widget>[
              Expanded(
                child: GridView.count(
                  crossAxisCount: 2,
                  children: List.generate(
                    serviceList.length,
                    (position) {
                      return Card(
                        margin: EdgeInsets.all(10),
                        elevation: 20,
                        color: colorList[Random().nextInt(colorList.length - 2)],
                        child: Container(
                          height: 100,
                          width: MediaQuery.of(context).size.width / 2,
                          child: InkWell(
                            splashColor: Colors.white.withAlpha(100),
                            onTap: () {
                              Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (context) {
                                    return ServiceBookPage(serviceList[position]);
                                  }
                                )
                              );
                            },
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: <Widget>[
                                Text(
                                  serviceList[position]['name'],
                                  style: TextStyle(
                                      fontSize: 18, color: Colors.white
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),
            ],
          ),
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
