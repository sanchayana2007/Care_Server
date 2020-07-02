import 'dart:convert';

import 'package:datetime_picker_formfield/datetime_picker_formfield.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:intl/intl.dart';
import 'package:ohzas/app-state/about_page.dart';
import 'package:ohzas/authorization/signIn.dart';
import 'package:ohzas/app-state/default/app_home_page.dart';
import 'package:ohzas/handler/http_request_handler.dart';
import 'package:ohzas/handler/network_handler.dart';
import 'package:ohzas/handler/shared_pref_handler.dart';
import 'package:ohzas/util/log_util.dart';
import 'package:ohzas/util/time_util.dart';
import 'package:ohzas/util/toast_util.dart';

TextEditingController dateAndTime = new TextEditingController();

class ServiceBookPage extends StatefulWidget {
  final Map service;
  ServiceBookPage(this.service);

  @override
  State<StatefulWidget> createState() {
    return _ServiceBookPage();
  }
}



class _ServiceBookPage extends State<ServiceBookPage> {
  SharedPrefHandler sharedPrefHandler;
  HttpRequestHandler httpRequestHandler;
  String newValue = 'One-time-session';
  String selected;
  String cancelFee = '0';

  // getAllData() async {
  // var resp1 = await httpRequestHandler.getServiceList();
  //     try {
  //       //Log.i(resp1);
  //       Log.i("Me");
  //       if (resp1['status']) {
  //         Log.i("Okay");
  //       } 
  //       else {
  //         cancelFee = '0';
  //       }
  //     } catch (e) {
  //       Log.i(e);
  //       Toaster.e(_context, message: 'Invalid Server Response.');
  //     }
  // }

  

  

  TextEditingController serviceName = new TextEditingController();
  TextEditingController serviceCharge = new TextEditingController();
  TextEditingController serviceTADA = new TextEditingController();
  TextEditingController serviceTotal = new TextEditingController();
  TextEditingController comment = new TextEditingController();
  TextEditingController session = new TextEditingController();

  _ServiceBookPage() {
    sharedPrefHandler = new SharedPrefHandler();
    dateAndTime.text = '';
    comment.text = '';
  }

  BuildContext _context;
  String TAG = "Servce Book Page";

  

  onSubmitBooking() async {
    if (dateAndTime.text.isEmpty) {
      Toaster.e(_context, message: 'Please Enter date and Time / कृपया दिनांक और समय दर्ज करें');
      return;
    }
    goBack();
    String mainTimeString = '';
    List<String> timeInString = dateAndTime.text.split(' ');
    mainTimeString = timeInString[0];
    mainTimeString = mainTimeString +
        ' ' +
        TimeUtil.convert12StringTo24String(
            timeIn12Hour: timeInString[1] + ' ' + timeInString[2],
            inputFormat: 'hh:mm a',
            outputFormat: 'HH:mm');
    int sessionValue = 0;
    if (newValue == sessionList[0]) {
      sessionValue = 1;
    } else {
      sessionValue = int.parse(newValue);
    }
    Object body = {
      "serviceId": widget.service['_id'],
      "time": TimeUtil.getIntTimeFromStringTime(timeInString: mainTimeString),
      "comment": comment.text.toString(),
      "session": sessionValue,
    };
    var resp = await httpRequestHandler.postSubmitBooking(body);
    try {
      Log.i(resp);
      if (resp['status']) {
        Toaster.s(_context, message: resp['message']);
        Navigator.of(_context).pop(true);
      } else {
        Toaster.e(_context, message: resp['message']);
      }
    } catch (e) {
      Log.i(e);
      Toaster.e(_context, message: 'Invalid Server Response.');
    }
  }

  String srvTotal = '';

  List<String> sessionList = [
    'One-time-session',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '19',
    '20'
  ];

  bool disclaimerView = true;

  @override
  Widget build(BuildContext context) {
    if (_context == null) {
      //getAllData();
      _context = context;
      httpRequestHandler = new HttpRequestHandler(context);
      serviceName.text = widget.service['serNameEnglish'].toString();
      serviceCharge.text = widget.service['serCharges'].toString();
      serviceTADA.text = widget.service['serTA'].toString();
      srvTotal = widget.service['serTATotal'].toString();
      //cancelFee.text = widget.service['cancelFee'].toString();
    }
    return WillPopScope(
      onWillPop: null,
      child: Scaffold(
        appBar: AppBar(
          title: Text('Book your service'),
        ),
        body: Container(
          width: MediaQuery.of(context).size.width,
          height: MediaQuery.of(context).size.height,
          color: Colors.white,
          child: SingleChildScrollView(
            child: Stack(
              children: <Widget>[
                Visibility(
                  visible: !disclaimerView,
                  child: Container(
                    color: Colors.white,
                    padding: EdgeInsets.only(top: 40, left: 20, right: 20),
                    child: Theme(
                      data: ThemeData(
                        primaryColor: Colors.black,
                        cursorColor: Colors.black,
                        accentColor: Colors.black,
                        fontFamily: "Poppins-Regular",
                      ),
                      child: new Column(
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                          TextField(
                            decoration: InputDecoration(
                              hintStyle:
                                  TextStyle(color: Colors.grey, fontSize: 12.0),
                              border: OutlineInputBorder(
                                borderSide: BorderSide(
                                  color: Colors.black,
                                ),
                              ),
                              labelText: "Service / सेवा",
                              labelStyle:
                                  TextStyle(color: Colors.black, fontSize: 18),
                            ),
                            enabled: false,
                            controller: serviceName,
                            keyboardType: TextInputType.phone,
                            style: TextStyle(fontSize: 20),
                          ),
                          SizedBox(
                            height: 20,
                          ),
                          TextField(
                            decoration: InputDecoration(
                              hintStyle:
                                  TextStyle(color: Colors.grey, fontSize: 12.0),
                              border: OutlineInputBorder(
                                borderSide: BorderSide(
                                  color: Colors.black,
                                ),
                              ),
                              labelText: "Service Charge / सेवा शुल्क",
                              labelStyle:
                                  TextStyle(color: Colors.black, fontSize: 18),
                            ),
                            enabled: false,
                            controller: serviceCharge,
                            keyboardType: TextInputType.phone,
                            style: TextStyle(fontSize: 20),
                          ),
                          // SizedBox(
                          //   height: 20,
                          // ),
                          // Text('Cancellation Fee'),
                          // Container(
                          //   width: MediaQuery.of(context).size.width,
                          //   padding:
                          //       EdgeInsets.only(left: 10, top: 15, bottom: 15),
                          //   decoration: BoxDecoration(
                          //       border: Border.all(color: Colors.grey),
                          //       borderRadius: BorderRadius.circular(5)),
                          //   child: Text(
                          //     cancelFee,
                          //     style: TextStyle(fontSize: 20),
                          //   ),
                          // ),
                          SizedBox(
                            height: 20,
                          ),
                          Text(
                            // '\t\t\tInside city limits/outside city limits',
                            '\t\t\tSelect session / सत्र का चयन करें',
                            style: TextStyle(fontSize: 14),
                          ),
                          Row(children: <Widget>[
                            new DropdownButton<String>(
                              value: newValue,
                              hint: Text("Please select the number of session"),
                              onChanged: (String changedValue) {
                                srvTotal = widget.service['serTATotal'].toString();
                                double subTot = 0;
                                newValue = changedValue;
                                try {
                                  subTot = double.parse(srvTotal);
                                } catch (e) {
                                  Log.i(e);
                                }
                                Log.i(newValue);
                                // double subTot = 0;
                                // try {
                                //   subTot = double.parse(serviceTotal.text);
                                // } catch (e) {
                                //   Log.i(e);
                                // }
                                double discount = 0;
                                if (newValue == '5' ||
                                    newValue == '6' ||
                                    newValue == '7' ||
                                    newValue == '8' ||
                                    newValue == '9' ||
                                    newValue == '10') {
                                  discount = 0.1;
                                }
                                if (newValue == '11' ||
                                    newValue == '12' ||
                                    newValue == '13' ||
                                    newValue == '14' ||
                                    newValue == '15') {
                                  discount = 0.15;
                                }
                                if (newValue == '16' ||
                                    newValue == '17' ||
                                    newValue == '18' ||
                                    newValue == '19' ||
                                    newValue == '20') {
                                  discount = 0.2;
                                }
                                Log.i(discount);
                                subTot = subTot - (subTot * discount);
                                Log.i(subTot);
                                setState(() {
                                  newValue = changedValue;
                                  srvTotal = subTot.toString();
                                });
                              },
                              items: sessionList.map((String value) {
                                return new DropdownMenuItem<String>(
                                  value: value,
                                  child: new Text(value),
                                );
                              }).toList(),
                            ),
                          ]),
                          SizedBox(
                            height: 30,
                          ),
                          TextField(
                            decoration: InputDecoration(
                              hintStyle:
                                  TextStyle(color: Colors.grey, fontSize: 12.0),
                              border: OutlineInputBorder(
                                borderSide: BorderSide(
                                  color: Colors.black,
                                ),
                              ),
                              labelText: 'Travelling Allowance / यात्रा भत्ता',
                              labelStyle:
                                  TextStyle(color: Colors.black, fontSize: 18),
                            ),
                            enabled: false,
                            controller: serviceTADA,
                            keyboardType: TextInputType.phone,
                            style: TextStyle(fontSize: 20),
                          ),
                          SizedBox(
                            height: 20,
                          ),
                          Text('Total Charge(per session) / कुल शुल्क(प्रति सत्र)'),
                          Container(
                            width: MediaQuery.of(context).size.width,
                            padding:
                                EdgeInsets.only(left: 10, top: 15, bottom: 15),
                            decoration: BoxDecoration(
                                border: Border.all(color: Colors.grey),
                                borderRadius: BorderRadius.circular(5)),
                            child: Text(
                              srvTotal,
                              style: TextStyle(fontSize: 20),
                            ),
                          ),
                          SizedBox(
                            height: 20,
                          ),
                          BasicDateTimeField(),
                          SizedBox(
                            height: 20,
                          ),
                          TextField(
                            decoration: InputDecoration(
                              hintStyle:
                                  TextStyle(color: Colors.grey, fontSize: 12.0),
                              border: OutlineInputBorder(
                                borderSide: BorderSide(
                                  color: Colors.black,
                                ),
                              ),
                              labelText: "Comment(optional)/टिप्पणी (वैकल्पिक)",
                              labelStyle:
                                  TextStyle(color: Colors.black, fontSize: 12),
                            ),
//                controller: signInMobileNumber,
                            maxLength: 320,
                            maxLines: 5,
                            keyboardType: TextInputType.text,
                            style: TextStyle(fontSize: 20),
                          ),
                          SizedBox(
                            height: 10,
                          ),
                          Text(
                            'Note*  Payment method ( Cash on delivery ).',
                            style: TextStyle(fontStyle: FontStyle.italic),
                          ),
                          SizedBox(
                            height: 5,
                          ),
                          Text(
                            'ध्यान दें* भुगतान विधि (डिलवरी पर नकदी).',
                            style: TextStyle(fontStyle: FontStyle.italic),
                          ),
                          SizedBox(
                            height: 30,
                          ),
                          Container(
                            padding: EdgeInsets.only(bottom: 20),
                            alignment: Alignment.bottomCenter,
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: <Widget>[
                                Row(
                                  children: <Widget>[
                                    FlatButton(
                                      padding: EdgeInsets.only(
                                        left: 30,
                                        right: 40,
                                        top: 10,
                                        bottom: 10,
                                      ),
                                      splashColor: Colors.white.withAlpha(80),
                                      color: Colors.black,
                                      shape: RoundedRectangleBorder(
                                        borderRadius:
                                            new BorderRadius.circular(30.0),
                                      ),
                                      onPressed: () {
                                        confirmPop();
                                      },
                                      child: Container(
                                        child: Row(
                                          mainAxisAlignment:
                                              MainAxisAlignment.center,
                                          children: <Widget>[
                                            Icon(
                                              Icons.assignment,
                                              color: Colors.white,
                                              size: 25,
                                            ),
                                            SizedBox(
                                              width: 20,
                                            ),
                                            Text(
                                              'Submit / निवेदन',
                                              style: TextStyle(
                                                fontSize: 20,
                                                color: Colors.white,
                                              ),
                                            )
                                          ],
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          )
                        ],
                      ),
                    ),
                  ),
                ),
                Visibility(
                  visible: disclaimerView,
                  child: Container(
                    width: MediaQuery.of(context).size.width,
                    padding: EdgeInsets.all(20),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: <Widget>[
                        Text(
                          'Consent/Disclaimer',
                          style: TextStyle(
                              fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        SizedBox(
                          height: 10,
                        ),
                        Text(
                          '\t\t\t\tI hereby willingly authorize the qualified personnel as assigned from “Ohzas” the mobile app, the minor procedure that I am required to undergo per my physician’s advice.',
                          style: TextStyle(fontSize: 14),
                          textAlign: TextAlign.justify,
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        Text(
                          '\t\t\t\tThe designated personnel has explained to me in my language, and I understand fully the nature, need and purpose of the treatment, possible alternatives, methods of treatment, the risks involved in whole procedure and possible complications. It has been explained to me that during the course of the operation(s) / treatment, unforeseen conditions may be revealed / or encountered which necessitates surgical or other procedures in extension of or in addition to the complications already explained to me. The designated personnel will not be held responsible for any eventuality if occurs during the treatment.',
                          style: TextStyle(fontSize: 14),
                          textAlign: TextAlign.justify,
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        Text(
                          '\t\t\t\t मैं यहाँ "ओजस" से सौंपे गए योग्य कर्मियों को स्वेच्छा से अधिकृत करता हूँ, जो मुझे अपने चिकित्सक की सलाह के अनुसार करने की आवश्यक मामूली प्रक्रिया आवश्यक मामूली प्रक्रिया है ।',
                          style: TextStyle(fontSize: 14),
                          textAlign: TextAlign.justify,
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        Text(
                          '\t\t\t\tनामित कर्मियों ने मुझे अपनी भाषा में समझाया है, और मैं उपचार की प्रकृति, आवश्यकता और उद्देश्य, संभावित विकल्प, उपचार के तरीके पूर्ण प्रक्रिया में शामिल जोखिम और संभावित जटिलताओं को पूरी तरह से समजता हूँ । यह मुझे समझाया है की ऑपरे शन (ओं ) / उपचार के दौरान, अप्रत्याशित परिस्तिथियों का खुलासा किया जा सकता है जो पहले से ही मुझे बताई गयी जटिलताओं के अलावा शल्य  चिकित्सा या अन्य प्रक्रियाओं के विस्तार की आवश्यकता है । उपचार के दौरान होने वाली किसी बी स्तिथि के लिए नामित कर्मियों को ज़िम्मेदार नहीं ठहराया जायेगा । ',
                          style: TextStyle(fontSize: 14),
                          textAlign: TextAlign.justify,
                        ),
                        Container(
                          margin: EdgeInsets.only(top: 30, bottom: 20),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceAround,
                            children: <Widget>[
                              Flexible(
                                flex: 1,
                                child: Card(
                                  color: Colors.grey,
                                  child: InkWell(
                                    onTap: () {
                                      Navigator.of(context).pop(true);
                                    },
                                    splashColor: Colors.white,
                                    child: Container(
                                      padding: EdgeInsets.only(
                                          top: 5,
                                          left: 20,
                                          right: 20,
                                          bottom: 5),
                                      child: Column(
                                        children: <Widget>[
                                          Text(
                                            'Decline',
                                            style: TextStyle(
                                                fontSize: 16,
                                                color: Colors.white),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              Flexible(
                                flex: 1,
                                child: Card(
                                  color: Colors.blue[400],
                                  child: InkWell(
                                    onTap: () {
                                      setState(() {
                                        disclaimerView = false;
                                      });
                                    },
                                    splashColor: Colors.white,
                                    child: Container(
                                      padding: EdgeInsets.only(
                                          top: 5,
                                          left: 20,
                                          right: 20,
                                          bottom: 5),
                                      child: Column(
                                        children: <Widget>[
                                          Text(
                                            'Accept',
                                            style: TextStyle(
                                                fontSize: 16,
                                                color: Colors.white),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                ),
                              )
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  goBack() {
    Navigator.of(_context).pushReplacement(
      MaterialPageRoute(builder: (context) => AppHomePage()),
    );
  }

 

  Future<bool> confirmPop() async {
    return (await showDialog(
          context: context,
          builder: (context) => new AlertDialog(
            title: new Text('Are you sure? \n\nCancellation after 30 minutes chargeable and will be added to your next invoice'),
            content: new Text(''),
            actions: <Widget>[
              new FlatButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: new Text('No'),
              ),
              new FlatButton(
                onPressed: () => [onSubmitBooking()],
                //},
                child: new Text('Yes'),
              ),
            ],
          ),
        )) ??
        false;
  }
}

class BasicDateTimeField extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _BasicDateTimeField();
  }
}

class _BasicDateTimeField extends State<BasicDateTimeField> {
  // 2012-02-27 13:27:00
  final format = DateFormat("yyyy-MM-dd hh:mm a");
  String labelText = 'Date and time/दिनांक और समय';
  _BasicDateTimeField();
  @override
  Widget build(BuildContext context) {
    return Column(children: <Widget>[
      Theme(
        data: ThemeData(
          primaryColor: Colors.black,
          cursorColor: Colors.black,
          accentColor: Colors.black,
          fontFamily: "Poppins-Regular",
        ),
        child: DateTimeField(
          format: format,
          controller: dateAndTime,
          decoration: InputDecoration(
              border: OutlineInputBorder(
                borderSide: BorderSide(
                  color: Colors.black,
                ),
              ),
              labelText: labelText,
              labelStyle: TextStyle(fontSize: 18, color: Colors.black)),
          style: TextStyle(fontSize: 18, color: Colors.black),
          onShowPicker: (context, currentValue) async {
            final date = await showDatePicker(
              context: context,
              firstDate: DateTime.now(),
              initialDate: currentValue ?? DateTime.now(),
              lastDate: DateTime(DateTime.now().year + 1),
            );
            if (date != null) {
              final time = await showTimePicker(
                context: context,
                initialTime:
                    TimeOfDay.fromDateTime(currentValue ?? DateTime.now()),
              );
              setState(() {
                labelText = 'Date and Time';
              });
              return DateTimeField.combine(date, time);
            } else {
              setState(() {
                labelText = 'Date and time/दिनांक और समय';
              });
              return currentValue;
            }
          },
          onChanged: (value) {
            if (value == null) {
              setState(() {
                labelText = 'Enter Date and Time';
              });
            }
          },
        ),
      ),
    ]);
  }
}
