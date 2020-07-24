import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:percent_indicator/linear_percent_indicator.dart';
import 'package:sprintf/sprintf.dart';
import 'package:ohzasProvider/app-state/default/service_provider_web_view.dart';
import 'package:ohzasProvider/app-state/default/app_home_page.dart';
import 'package:ohzasProvider/handler/shared_pref_handler.dart';
import 'package:ohzasProvider/handler/build_config.dart';
import 'package:ohzasProvider/handler/http_request_handler.dart';
import 'package:ohzasProvider/handler/network_handler.dart';
import 'package:ohzasProvider/util/log_util.dart';
import 'package:ohzasProvider/util/toast_util.dart';

class ServiceProviderHome extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _ServiceProviderHome();
  }
}

class _ServiceProviderHome extends State<ServiceProviderHome> {
  //var _url;
  final _key = UniqueKey();
  bool pageLoaded = false;
  int loadCount = 0;
  BuildContext _context;
  HttpRequestHandler httpRequestHandler;
  SharedPrefHandler sharedPreferencesHandler;
  String serviceId = '';

  _ServiceProviderHome() {
    //_url = BuildConfig.serverUrl + '/tour_operator/registration/';
  }

  @override
  Widget build(BuildContext context) {
    if (_context == null) {
      final id = ModalRoute.of(context).settings.arguments;
      Log.i(id);
      serviceId = id;
      _context = context;
      httpRequestHandler = new HttpRequestHandler(context);
      sharedPreferencesHandler = new SharedPrefHandler();
      getServiceAccount();
    }

    return WillPopScope(
      onWillPop: _onWillPop,
      child: Scaffold(
        appBar: AppBar(
          title: Text(
            'Service Provider',
            style: TextStyle(
              color: Colors.black,
            ),
          ),
          iconTheme: IconThemeData(color: Colors.black),
          backgroundColor: Colors.white,
          actions: <Widget>[
            IconButton(
              icon: Icon(
                Icons.refresh,
                color: Colors.black,
              ),
              onPressed: () {
                getServiceAccount();
              },
            )
          ],
        ),
        body: SingleChildScrollView(
          child: Container(
            padding: EdgeInsets.only(
              top: 10,
              left: 10,
              right: 10,
              bottom: 10,
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                Container(
                  padding: EdgeInsets.all(10),
                  width: MediaQuery.of(context).size.width,
                  alignment: Alignment.center,
                  child: !srvVerified
                      ? Text(
                          'Account activation is Pending',
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.orange[700],
                            fontWeight: FontWeight.bold,
                          ),
                          textAlign: TextAlign.center,
                        )
                      : Text(
                          'Account is Verified',
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.green,
                            fontWeight: FontWeight.bold,
                          ),
                          textAlign: TextAlign.center,
                        ),
                ),
                SizedBox(
                  height: 10,
                ),
                Container(
                  child: Column(
                    children: <Widget>[
                      LinearPercentIndicator(
                        width: MediaQuery.of(context).size.width - 25,
                        lineHeight: 10,
                        percent: tPercentage / 100,
                        progressColor: Colors.blue[700],
                      ),
                      Text(
                        sprintf('Overall Progress %s%', [tPercentage]),
                        style: TextStyle(
                          fontSize: 18,
                          fontStyle: FontStyle.italic,
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(
                  height: 10,
                ),
                Column(
                  children: <Widget>[
                    // Card(
                    //   elevation: 10,
                    //   child: InkWell(
                    //     onTap: () {
                    //       Log.i(httpRequestHandler.xAuthorizationKey);
                    //       Log.i(httpRequestHandler.xOriginKey);
                    //       Log.i(httpRequestHandler.xApiKey);
                    //       Log.i(covid19State);
                    //       int covid19Status = 0;
                    //       if (covid19State) {
                    //         covid19Status = 1;
                    //       }
                    //       String covid19Form = BuildConfig.serverUrl +
                    //           '/reg_contact_form/?' +
                    //           sprintf(
                    //               'Authorization=%s&x-Origin-Key=%s&x-Api-Key=%s&status=%s&serviceType=%s',
                    //               [
                    //                 httpRequestHandler.xAuthorizationKey,
                    //                 httpRequestHandler.xOriginKey,
                    //                 httpRequestHandler.xApiKey,
                    //                 covid19Status,
                    //                 5
                    //               ]);
                    //       Log.i(covid19Form);
                    //       Navigator.of(context).push(
                    //         MaterialPageRoute(
                    //           builder: (context) => BoatManWebView(
                    //             pageUrl: covid19Form,
                    //           ),
                    //         ),
                    //       );
                    //     },
                    //     child: Container(
                    //       padding: EdgeInsets.all(10),
                    //       child: Row(
                    //         mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    //         children: <Widget>[
                    //           Flexible(
                    //             flex: 6,
                    //             child: Text(
                    //               'Contact Information',
                    //               style: TextStyle(
                    //                 fontSize: 14,
                    //               ),
                    //             ),
                    //           ),
                    //           Flexible(
                    //             flex: 1,
                    //             child: formComplt[0]
                    //                 ? Icon(
                    //                     Icons.check_circle,
                    //                     size: 30,
                    //                     color: Colors.green[700],
                    //                   )
                    //                 : Icon(
                    //                     CupertinoIcons.clear_thick_circled,
                    //                     size: 30,
                    //                     color: Colors.redAccent,
                    //                   ),
                    //           ),
                    //         ],
                    //       ),
                    //     ),
                    //   ),
                    // ),
                    Card(
                      elevation: 10,
                      child: InkWell(
                        onTap: () {
                          Log.i(httpRequestHandler.xAuthorizationKey);
                          Log.i(httpRequestHandler.xOriginKey);
                          Log.i(httpRequestHandler.xApiKey);
                          Log.i(covid19State);
                          int covid19Status = 0;
                          if (covid19State) {
                            covid19Status = 1;
                          }
                          Log.i("Service Id for form below");
                          Log.i(serviceId);
                          String covid19Form = BuildConfig.serverUrl +
                              '/provider/?' +
                              sprintf(
                                  'Authorization=%s&x-Origin-Key=%s&x-Api-Key=%s&id=%s',
                                  [
                                    httpRequestHandler.xAuthorizationKey,
                                    httpRequestHandler.xOriginKey,
                                    httpRequestHandler.xApiKey,
                                    serviceId,
                                  ]);
                          Log.i(covid19Form);
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (context) => BoatManWebView(
                                pageUrl: covid19Form,
                              ),
                            ),
                          );
                        },
                        child: Container(
                          padding: EdgeInsets.all(10),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: <Widget>[
                              Flexible(
                                flex: 6,
                                child: Text(
                                  'Service Information',
                                  style: TextStyle(
                                    fontSize: 14,
                                  ),
                                ),
                              ),
                              Flexible(
                                flex: 1,
                                child: formComplt[1]
                                    ? Icon(
                                        Icons.check_circle,
                                        size: 30,
                                        color: Colors.green[700],
                                      )
                                    : Icon(
                                        CupertinoIcons.clear_thick_circled,
                                        size: 30,
                                        color: Colors.redAccent,
                                      ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                SizedBox(
                  height: 20,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  double tPercentage = 0.0;
  List<bool> formComplt = [
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
  ];
  Map srvAccountDt;
  List<int> formSubmitted = [0, 13];

  @override
  void deactivate() {
    super.deactivate();
    try {
      Log.i('SERVICE PROVIDER MY ACCOUNT', mounted);
      getServiceAccount();
    } catch (e) {
      Log.e(e);
    }
  }

  bool srvVerified = false;
  getServiceAccount() async {
    if (!await NetworkHandler.isOnlineWithToast(
      _context,
    )) {
      return null;
    }
    Log.i('TSRT BOOK');
    var value = await httpRequestHandler.getServiceAccountOvw(serviceId);
    // Log.i('SRC ACC', value);
    tPercentage = 0;
    try {
      Log.i(value);
      if (value['status']) {
        srvAccountDt = value['result'][0];
        formSubmitted[0] = 0;
        Log.i(srvAccountDt);
        if (srvAccountDt['serviceProvider']) {
          tPercentage = 100;
          formComplt[1] = true;
        }
        // if (srvAccountDt['document']) {
        //   tPercentage += 25;
        //   formComplt[2] = true;
        // }
        // if (srvAccountDt['declaration']) {
        //   tPercentage += 25;
        // }
        if (srvAccountDt['verified'] != null && srvAccountDt['verified']) {
          srvVerified = true;
        }
      } else {
        formSubmitted[0] = 0;
        tPercentage = 0;
        srvVerified = false;
        for (int i = 0; i < formComplt.length; i++) {
          formComplt[i] = false;
        }
      }
    } catch (e) {
      Log.i(e);
      Toaster.w(_context, message: 'Invalid Server Reponsse.');
    }
    if (!mounted) {
      return;
    }
    setState(() {
      formComplt = formComplt;
    });
  }

  bool covid19State = false;

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
                onPressed: () => goBack(),
                child: new Text('Yes'),
              ),
            ],
          ),
        )) ??
        false;
  }

  goBack() {
    Navigator.of(_context).pushReplacement(
      MaterialPageRoute(builder: (context) => AppHomePage()),
    );
  }
}
