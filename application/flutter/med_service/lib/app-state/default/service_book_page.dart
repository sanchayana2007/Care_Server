import 'dart:convert';

import 'package:datetime_picker_formfield/datetime_picker_formfield.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:intl/intl.dart';
import 'package:medservice/app-state/about_page.dart';
import 'package:medservice/authorization/signIn.dart';
import 'package:medservice/handler/http_request_handler.dart';
import 'package:medservice/handler/network_handler.dart';
import 'package:medservice/handler/shared_pref_handler.dart';
import 'package:medservice/util/log_util.dart';
import 'package:medservice/util/time_util.dart';
import 'package:medservice/util/toast_util.dart';

TextEditingController serviceName = new TextEditingController();
TextEditingController dateAndTime = new TextEditingController();
TextEditingController comment = new TextEditingController();

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

  _ServiceBookPage() {
    sharedPrefHandler = new SharedPrefHandler();
    httpRequestHandler = new HttpRequestHandler();
    dateAndTime.text = '';
    comment.text = '';
  }

  BuildContext _context;
  String TAG = "Servce Book Page";

  onSubmitBooking() async {
    if (dateAndTime.text.isEmpty) {
      Toaster.e(message: 'Please Enter date and Time');
      return;
    }
    String mainTimeString = '';
    List<String> timeInString = dateAndTime.text.split(' ');
    mainTimeString = timeInString[0];
    mainTimeString = mainTimeString + ' ' + TimeUtil.convert12StringTo24String(
        timeIn12Hour: timeInString[1] + ' ' + timeInString[2],
        inputFormat: 'hh:mm a',
        outputFormat: 'HH:mm'
    );
    Object body = {
      "serviceId": widget.service['_id'],
      "time": TimeUtil.getIntTimeFromStringTime(
        timeInString: mainTimeString
      ),
      "comment": comment.text.toString()
    };
    var resp = await httpRequestHandler.postSubmitBooking(body);
    try {
      Log.i(resp);
      if (resp['status']) {
        Toaster.s(message: resp['message']);
        Navigator.of(_context).pop(true);
      } else {
        Toaster.e(message: resp['message']);
      }
    } catch (e) {
      Log.i(e);
      Toaster.e(message: 'Invalid Server Response.');
    }
  }

  @override
  Widget build(BuildContext context) {
    _context = context;
    serviceName.text = widget.service['name'];
    return WillPopScope(
      onWillPop: null,
      child: Scaffold(
        appBar: AppBar(
          title: Text('Book your service'),
        ),
        body: SingleChildScrollView(
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
                      hintStyle: TextStyle(
                          color: Colors.grey, fontSize: 12.0),
                      border: OutlineInputBorder(
                        borderSide: BorderSide(
                          color: Colors.black,
                        ),
                      ),
                      labelText: "Service",
                      labelStyle: TextStyle(
                          color: Colors.black,
                          fontSize: 18
                      ),
                    ),
                    enabled: false,
                    controller: serviceName,
                    keyboardType: TextInputType.phone,
                    style: TextStyle(fontSize: 20),
                  ),
                  SizedBox(
                    height: 30,
                  ),
                  BasicDateTimeField(),
                  SizedBox(
                    height: 30,
                  ),
                  TextField(
                    decoration: InputDecoration(
                      hintStyle: TextStyle(
                          color: Colors.grey, fontSize: 12.0),
                      border: OutlineInputBorder(
                        borderSide: BorderSide(
                          color: Colors.black,
                        ),
                      ),
                      labelText: "Comment ( Optional ) ",
                      labelStyle: TextStyle(
                          color: Colors.black,
                          fontSize: 18
                      ),
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
                    style: TextStyle(
                      fontStyle: FontStyle.italic
                    ),
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
                                borderRadius: new BorderRadius.circular(30.0),
                              ),
                              onPressed: () {
                                onSubmitBooking();
                              },
                              child: Container(
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
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
                                      'Submit',
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
      ),
    );
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
  String labelText = 'Enter Date and time';
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
            labelStyle: TextStyle(
              fontSize: 18,
              color: Colors.black
            )
          ),
          style: TextStyle(
            fontSize: 18,
            color: Colors.black
          ),
          onShowPicker: (context, currentValue) async {
            final date = await showDatePicker(
              context: context,
              firstDate: DateTime(DateTime.now().year),
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
                labelText = 'Enter Date and Time';
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
