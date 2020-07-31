import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:loading/indicator/ball_pulse_indicator.dart';
import 'package:loading/loading.dart';
import 'package:ohzasProvider/util/log_util.dart';

class BoatManWebView extends StatefulWidget {
  String pageUrl;
  BoatManWebView({this.pageUrl});

  @override
  State<StatefulWidget> createState() {
    return _BoatManWebView(this.pageUrl);
  }
}

class _BoatManWebView extends State<BoatManWebView> {
  var _url;
  final _key = UniqueKey();
  bool pageLoaded = false;
  int loadCount = 0;
  BuildContext _context;

  InAppWebViewController webView;
  String url = "";
  double loadProgress = 0;

  _BoatManWebView(this._url) {
    Log.i('COVID-19 URL', _url);
    url = _url;
  }
  // final flutterWebViewPlugin = FlutterWebviewPlugin();

  @override
  Widget build(BuildContext context) {
    if (_context == null) {
      _context = context;
    }

    return WillPopScope(
      onWillPop: _onWillPop,
      child: Scaffold(
        appBar: AppBar(
          title: Text('Account Form'),
        ),
        body: Stack(
          children: [
            InAppWebView(
              initialUrl: _url,
              initialHeaders: {},
              initialOptions: InAppWebViewGroupOptions(
                  crossPlatform: InAppWebViewOptions(
                debuggingEnabled: true,
              )),
              onWebViewCreated: (InAppWebViewController controller) {
                webView = controller;
              },
              onLoadStart: (InAppWebViewController controller, String url) {
                Log.i('onLoadStart');
                if (pageLoaded) {
                  Navigator.of(context).pop(true);
                }
//            setState(() {
//              this.url = url;
//            });
              },
              onLoadStop:
                  (InAppWebViewController controller, String url) async {
                // loadCount++;
                // if (loadCount > 1) {
                //   Navigator.of(context).pop(true);
                // }
                Log.i('onLoadStop');

//            setState(() {
//              this.url = url;
//            });
              },
              onProgressChanged:
                  (InAppWebViewController controller, int progress) {
                Log.i('onProgressChanged', progress);
                // if (pageLoaded) {
                //   Navigator.of(context).pop(true);
                // }
                loadProgress = progress.roundToDouble();
                if (loadProgress == 100) {
                  setState(() {
                    pageLoaded = true;
                  });
                }
//            setState(() {
//              this.progress = progress / 100;
//            });
              },
              onLoadResource:
                  (InAppWebViewController controller, LoadedResource resource) {
                Log.i('onLoadResource');
              },
            ),
            Visibility(
              visible: !pageLoaded,
              child: Container(
                width: MediaQuery.of(context).size.width,
                height: MediaQuery.of(context).size.height,
                alignment: Alignment.center,
                color: Colors.white,
                child: Loading(
                  indicator: BallPulseIndicator(),
                  color: Colors.indigo[800],
                  size: 60.0,
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
            title: new Text('If you have made any change, it will be lost.'),
            content: Text('Do you want to go back?'),
            actions: <Widget>[
              new FlatButton(
                onPressed: () {
                  Navigator.of(context).pop(false);
                },
                child: new Text('No'),
              ),
              new FlatButton(
                onPressed: () {
                  Navigator.of(context).pop(true);
//              onSubmitServiceAccountInfo1();
                },
                child: new Text('Yes'),
              ),
            ],
          ),
        )) ??
        false;
  }
}
