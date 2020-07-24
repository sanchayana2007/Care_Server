import 'package:flutter/material.dart';
import 'package:ohzasProvider/handler/http_request_handler.dart';
import 'package:ohzasProvider/util/log_util.dart';
import 'package:ohzasProvider/util/time_util.dart';
import 'package:ohzasProvider/util/toast_util.dart';

class ServiceBookHistoryPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _ServiceBookHistoryPage();
  }
}

class _ServiceBookHistoryPage extends State<ServiceBookHistoryPage> {
  BuildContext _context;
  HttpRequestHandler httpRequestHandler;

  var bookingHistory = [];

  _ServiceBookHistoryPage() {}
  bool buttonState = true;

  void _buttonChange() {
    setState(() {
      buttonState ? _buttonChange : null;
    });
  }

  cancelAppointment(context, bookingId) async {
    Log.i(bookingId);
    Object body = {
      "bookingId": bookingId,
    };
    var resp = await httpRequestHandler.putSubmitBooking(body);
    try {
      Log.i(resp);
      if (resp['status']) {
        Toaster.s(context, message: resp['message']);
        getAllBookings();
      } else {
        Toaster.e(context, message: resp['message']);
      }
    } catch (e) {
      Toaster.e(context, message: 'Internal Server Response');
    }
  }

  getAllBookings() async {
    var resp = await httpRequestHandler.getAppointmentBooking();
    try {
      Log.i(resp);
      if (resp['status']) {
        loadAllBookings(resp['result']);
      } else {
        Toaster.e(_context, message: resp['message']);
      }
    } catch (e) {
      Log.i(e);
      Toaster.e(_context, message: 'Invalid Server Response.');
    }
  }

  loadAllBookings(var data) async {
    for (int i = 0; i < data.length; i++) {
      try {
        Map index = data[i];
        index['stageColor'] = Colors.black;
        switch (index['stage']) {
          case 'new':
            index['stageColor'] = Colors.yellow[800];
            Log.i('default 0');
            break;
          case 'completed':
            index['stageColor'] = Colors.blue[500];
            Log.i('default 1');
            break;
          case 'accepted':
            index['stageColor'] = Colors.green[500];
            Log.i('default 2');
            break;
          case 'declined':
            index['stage'] = 'cancelled';
            index['stageColor'] = Colors.red[500];
            Log.i('default 2');
            break;
          case 'declined_fee':
            index['stage'] = 'cancelled(with fee)';
            index['stageColor'] = Colors.red[500];
            Log.i('default 2');
            break;
          default:
            Log.i('default');
            index['stageColor'] = Colors.black;
        }
        data[i] = index;
      } catch (e) {
        Log.i('INDEX', i);
        Log.i('DATA', data[i]);
        continue;
      }
    }
    setState(() {
      bookingHistory = data;
    });
  }

  bool historyLoaded = true;
  @override
  Widget build(BuildContext context) {
    _context = context;
    httpRequestHandler = new HttpRequestHandler(context);
    if (historyLoaded) {
      getAllBookings();
      historyLoaded = false;
    }
    return new WillPopScope(
      onWillPop: null,
      child: new Scaffold(
        appBar: AppBar(
          title: Text('Booking History'),
          actions: <Widget>[
            IconButton(
              icon: Icon(Icons.refresh),
              onPressed: () {
                getAllBookings();
              },
            )
          ],
        ),
        body: Container(
          color: Colors.blueGrey.withAlpha(50),
          alignment: Alignment.center,
          child: Column(
            children: <Widget>[
              Visibility(
                visible: bookingHistory.length > 0,
                child: Expanded(
                  child: ListView.builder(
                    itemBuilder: (context, position) {
                      return Card(
                        margin: EdgeInsets.only(
                            top: 10, bottom: 5, left: 10, right: 10),
                        child: InkWell(
                          onTap: () {},
                          child: Container(
                            padding: EdgeInsets.all(20),
                            width: MediaQuery.of(context).size.width,
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: <Widget>[
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: <Widget>[
                                    Text(
                                      bookingHistory[position]['stage']
                                          .toString()
                                          .toUpperCase(),
                                      style: TextStyle(
                                        fontSize: 16,
                                        color: bookingHistory[position]
                                            ['stageColor'],
                                      ),
                                    )
                                  ],
                                ),
                                SizedBox(
                                  height: 10,
                                ),
                                Row(
                                  children: <Widget>[
                                    Flexible(
                                      flex: 1,
                                      child: Text(
                                        bookingHistory[position]['serviceDetails']
                                                [0]['serNameEnglish']
                                            .toString()
                                            .toUpperCase(),
                                        style: TextStyle(
                                            fontSize: 16,
                                            color: Colors.blueGrey[600],
                                            fontWeight: FontWeight.bold),
                                      ),
                                    ),
                                    // Text(' / '),
                                    // Text(
                                    //   bookingHistory[position]['serviceDetails']
                                    //           [0]['serNameHindi']
                                    //       .toString()
                                    //       .toUpperCase(),
                                    //   style: TextStyle(
                                    //       fontSize: 16,
                                    //       color: Colors.blueGrey[600],
                                    //       fontWeight: FontWeight.bold),
                                    // ),
                                  ],
                                ),
                                SizedBox(
                                  height: 10,
                                ),
                                Row(
                                  children: <Widget>[
                                    Text(
                                      'Requested :',
                                      style: TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.bold),
                                    ),
                                    SizedBox(
                                      width: 10,
                                    ),
                                    Text(
                                      TimeUtil.getStringTimeFromIntTime(
                                          timeInMicroSeconds:
                                              bookingHistory[position]
                                                  ['requestedTime'],
                                          dateFormat: 'yyyy/MM/dd hh:mm a'),
                                      style: TextStyle(
                                        fontSize: 14,
                                      ),
                                    )
                                  ],
                                ),
                                SizedBox(
                                  height: 5,
                                ),
                                Row(
                                  children: <Widget>[
                                    Text(
                                      'Appointed :',
                                      style: TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.bold),
                                    ),
                                    SizedBox(
                                      width: 12,
                                    ),
                                    Text(
                                      TimeUtil.getStringTimeFromIntTime(
                                          timeInMicroSeconds:
                                              bookingHistory[position]
                                                  ['booktime'],
                                          dateFormat: 'yyyy/MM/dd hh:mm a'),
                                      style: TextStyle(
                                        fontSize: 14,
                                      ),
                                    )
                                  ],
                                ),
                                SizedBox(
                                  height: 5,
                                ),
                                Row(
                                  children: <Widget>[
                                    Text(
                                      'Session Booked :',
                                      style: TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.bold),
                                    ),
                                    SizedBox(
                                      width: 12,
                                    ),
                                    Text(
                                      bookingHistory[position]['session']
                                            .toString()
                                            .toUpperCase(),
                                      style: TextStyle(
                                        fontSize: 14,
                                      ),
                                    )
                                  ],
                                ),
                                SizedBox(
                                  height: 5,
                                ),
                                Row(
                                  children: <Widget>[
                                    Text(
                                      'Session Remaining :',
                                      style: TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.bold),
                                    ),
                                    SizedBox(
                                      width: 12,
                                    ),
                                    Text(
                                      bookingHistory[position]['session_remaining']
                                            .toString()
                                            .toUpperCase(),
                                      style: TextStyle(
                                        fontSize: 14,
                                      ),
                                    )
                                  ],
                                ),
                                SizedBox(height: 10),
                                Visibility(
                                  visible: (DateTime.now().microsecondsSinceEpoch - bookingHistory[position]['requestedTime']) < 300000000 * 6 && bookingHistory[position]['stage'] != 'declined' && bookingHistory[position]['stage'] != 'completed' && bookingHistory[position]['stage'] != 'cancelled' && bookingHistory[position]['stage'] != 'declined_fee',
                                  child: Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: <Widget>[
                                        RaisedButton(
                                          child: Text("Cancel Appointment / अपॉइंटमेंट रद्द करें"),
                                          onPressed: (){
                                            Log.i((DateTime.now().microsecondsSinceEpoch - bookingHistory[position]['requestedTime']));
                                            cancelAppointment(context, 
                                              bookingHistory[position]
                                                    ['_id']);
                                          },
                                          //onPressed:buttonState ? _buttonChange : null,
                                          color: Colors.orange,
                                          textColor: Colors.white,
                                          padding:
                                              EdgeInsets.fromLTRB(10, 10, 10, 10),
                                          splashColor: Colors.grey,
                                        )
                                      ],
                                  ),
                                )
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                    itemCount: bookingHistory.length,
                  ),
                ),
              ),
              Visibility(
                visible: bookingHistory.length == 0,
                child: Column(
                  children: <Widget>[
                    Container(
                      alignment: Alignment.center,
                      width: MediaQuery.of(context).size.width,
                      height: MediaQuery.of(context).size.width + 100,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: <Widget>[
                          Icon(
                            Icons.hourglass_empty,
                            size: 80,
                            color: Colors.blueGrey[600],
                          ),
                          SizedBox(
                            height: 20,
                          ),
                          Text(
                            'No Booking is available.',
                            style: TextStyle(
                              fontSize: 16,
                              fontStyle: FontStyle.italic,
                              color: Colors.blueGrey[600],
                            ),
                          )
                        ],
                      ),
                    ),
                  ],
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
