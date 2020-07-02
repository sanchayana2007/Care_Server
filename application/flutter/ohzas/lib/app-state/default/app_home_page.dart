import 'dart:convert';
import 'dart:math';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:ohzas/app-state/about_page.dart';
import 'package:ohzas/app-state/contactus_page.dart';
import 'package:ohzas/app-state/default/service_book_history_page.dart';
import 'package:ohzas/app-state/default/service_book_page.dart';
import 'package:ohzas/authorization/signIn.dart';
import 'package:ohzas/handler/http_request_handler.dart';
import 'package:ohzas/handler/network_handler.dart';
import 'package:ohzas/handler/shared_pref_handler.dart';
import 'package:ohzas/util/log_util.dart';
import 'package:ohzas/util/toast_util.dart';
import 'package:share/share.dart';

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
  }

  List<dynamic> serviceList = [];

  getAllData() async {
    await httpRequestHandler.getHeaders();
    if (!await NetworkHandler.isOnlineWithToast(
      _context,
    )) {
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
          Toaster.e(_context, message: resp['message']);
        }
      } catch (e) {
        Log.i(e);
        Toaster.e(_context, message: 'Invalid Server Response.');
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
        if (index['serNameEnglish'] == null || index['serNameEnglish'] == '') {
          index['serNameEnglish'] = 'N/A';
        }
        if (index['serCharges'] == null || index['serCharges'] == '') {
          index['serCharges'] = 'N/A';
        }
        if (index['serTADA'] == null || index['serTADA'] == '') {
          index['serTADA'] = 'N/A';
        }
        if (index['serTotal'] == null || index['serTotal'] == '') {
          index['serTotal'] = 'N/A';
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
    } else {
      setState(() {
        srvMessage = 'No service is available.';
      });
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

  String srvMessage = 'Loading..';

  @override
  Widget build(BuildContext context) {
    var assetsImage = new AssetImage(
        'assets/discount.png'); //<- Creates an object that fetches an image.
    var image = new Image(image: assetsImage, fit: BoxFit.cover);
    _context = context;
    if (profileLoaded) {
      httpRequestHandler = new HttpRequestHandler(context);
      getAllData();
    }
    return WillPopScope(
      onWillPop: _onWillPop,
      child: Scaffold(
        appBar: AppBar(
          title: Text('Ohzas'),
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
                  if (await NetworkHandler.isOnlineWithToast(
                    context,
                  )) {
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
              InkWell(
                onTap: () async {
                  if (await NetworkHandler.isOnlineWithToast(
                    context,
                  )) {
                    Navigator.of(_context).push(MaterialPageRoute(
                        builder: (context) => ContactusPage()));
                  }
                },
                child: ListTile(
                  title: Text("Contact Us"),
                  leading: Icon(Icons.contact_phone, color: Colors.green),
                ),
              ),
              Divider(
                color: Colors.grey[600],
              ),
              InkWell(
                onTap: () => Share.share(
                    'Download the OHZAS app for the best online health service: https://play.google.com/store/apps/details?id=com.xlayer.med.ohzas'),
                child: ListTile(
                  title: Text("Share"),
                  leading: Icon(Icons.share, color: Colors.blue),
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
                  Toaster.e(context, message: 'Signing Out, Please Wait.');
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
          width: MediaQuery.of(context).size.width,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              new Row(
                children: <Widget>[
                  Expanded(
                    child: Image.network(
                        "https://medix.xlayer.in/uploads/default/discount_new.png"),
                  ),
                  // new Container(
                  //   padding: EdgeInsets.all(2),
                  //   child: new Image.asset(
                  //     'assets/discount_new.png',
                  //     height: 110.0,
                  //     width:350,
                  //     //fit: BoxFit.fitWidth,
                  //     //fit: BoxFit.cover,
                  //   ),
                  // ),
                ],
              ),
              Visibility(
                visible: serviceList.length > 0,
                child: Expanded(
                  child: GridView.count(
                    crossAxisCount: 2,
                    childAspectRatio: (2 / 3),
                    controller: new ScrollController(keepScrollOffset: false),
                    shrinkWrap: true,
                    children: List.generate(
                      serviceList.length,
                      (position) {
                        return Card(
                          margin: EdgeInsets.all(8),
                          elevation: 20,
                          child: Container(
                            padding: EdgeInsets.only(top: 15),
                            height: 500,
                            child: InkWell(
                              splashColor: Colors.white.withAlpha(100),
                              onTap: () {
                                Navigator.of(context).push(
                                  MaterialPageRoute(builder: (context) {
                                    return ServiceBookPage(
                                        serviceList[position]);
                                  }),
                                );
                              },
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.start,
                                crossAxisAlignment: CrossAxisAlignment.stretch,
                                children: <Widget>[
                                  FadeInImage.assetNetwork(
                                    height: (MediaQuery.of(context).size.width /
                                            100) *
                                        31,
                                    fit: BoxFit.contain,
                                    placeholder: 'assets/loading_wt.gif',
                                    image: serviceList[position]['media'][0]
                                        ['link'],
                                  ),
                                  SizedBox(
                                    height: 5,
                                  ),
                                  Container(
                                    padding:
                                        EdgeInsets.only(left: 10, right: 10),
                                    child: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: <Widget>[
                                        Flexible(
                                          flex: 1,
                                          child: Text(
                                            serviceList[position]
                                                ['serNameEnglish'],
                                            style: TextStyle(
                                              fontSize: 14,
                                              color: Colors.black,
                                            ),
                                            textAlign: TextAlign.center,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  Container(
                                    padding:
                                        EdgeInsets.only(left: 10, right: 10),
                                    child: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: <Widget>[
                                        Flexible(
                                          flex: 1,
                                          child: Text(
                                            serviceList[position]
                                                ['serNameHindi'],
                                            style: TextStyle(
                                              fontSize: 14,
                                              color: Colors.black,
                                            ),
                                            textAlign: TextAlign.center,
                                          ),
                                        ),
                                      ],
                                    ),
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
              ),
              Visibility(
                visible: serviceList.length == 0,
                child: Column(
                  children: <Widget>[
                    Text(srvMessage),
                  ],
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
