
import 'package:flutter/material.dart';
import 'package:ohzas/handler/http_request_handler.dart';
import 'package:ohzas/util/log_util.dart';
import 'package:ohzas/util/time_util.dart';
import 'package:ohzas/util/toast_util.dart';

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

  _ServiceBookHistoryPage() {
    
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
    for(int i=0; i < data.length; i++) {
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
              icon: Icon(
                Icons.refresh
              ),
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
                            top: 10,
                            bottom: 5,
                            left: 10,
                            right: 10
                        ),
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
                                      bookingHistory[position]['stage'].toString().toUpperCase(),
                                      style: TextStyle(
                                        fontSize: 16,
                                        color: bookingHistory[position]['stageColor'],
                                      ),
                                    )
                                  ],
                                ),
                                SizedBox(
                                  height: 10,
                                ),
                                Row(
                                  children: <Widget>[
                                    Text(
                                      bookingHistory[position]['serviceDetails'][0]['serNameEnglish'].toString().toUpperCase(),
                                      style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.blueGrey[600],
                                          fontWeight: FontWeight.bold
                                      ),
                                    ),
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
                                          fontWeight: FontWeight.bold
                                      ),
                                    ),
                                    SizedBox(
                                      width: 10,
                                    ),
                                    Text(
                                      TimeUtil.getStringTimeFromIntTime(
                                          timeInMicroSeconds: bookingHistory[position]['requestedTime'],
                                          dateFormat: 'yyyy/MM/dd hh:mm a'
                                      ),
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
                                          fontWeight: FontWeight.bold
                                      ),
                                    ),
                                    SizedBox(
                                      width: 12,
                                    ),
                                    Text(
                                      TimeUtil.getStringTimeFromIntTime(
                                          timeInMicroSeconds: bookingHistory[position]['booktime'],
                                          dateFormat: 'yyyy/MM/dd hh:mm a'
                                      ),
                                      style: TextStyle(
                                        fontSize: 14,
                                      ),
                                    )
                                  ],
                                ),
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
