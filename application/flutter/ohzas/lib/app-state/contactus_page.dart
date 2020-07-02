//import 'package:clipboard_manager/clipboard_manager.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get_version/get_version.dart';
import 'package:ohzas/util/toast_util.dart';
import 'package:package_info/package_info.dart';
import 'package:url_launcher/url_launcher.dart';

class ContactusPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _ContactusPage();
  }
}

class _ContactusPage extends State<ContactusPage> {


  @override
  initState() {
    super.initState();
    initPlatformState();
  }

  // Platform messages are asynchronous, so we initialize in an async method.
  initPlatformState() async {
   

    // If the widget was removed from the tree while the asynchronous platform
    // message was in flight, we want to discard the reply rather than calling
    // setState to update our non-existent appearance.
  }

  @override
  Widget build(BuildContext context) {
    return new WillPopScope(
      onWillPop: null,
      child: new Scaffold(
        appBar: new AppBar(
          title: new Text(
            'Contact Us',
            style: TextStyle(color: Colors.black),
          ),
          
          backgroundColor: Colors.white,
          iconTheme: IconThemeData(
            color: Colors.black,
          ),
          elevation: 5,
        ),
        body: Container(
          padding: EdgeInsets.only(left: 20, right: 20),
          color: Colors.grey.withAlpha(100),
          height: MediaQuery.of(context).size.height,
          child: new SingleChildScrollView(
            child: new ListBody(
              children: <Widget>[
                Divider(
                color: Colors.grey[1000],
              ),
                Card(
                  margin: EdgeInsets.only(
                    top: 10,
                    bottom: 10,
                    left: 10,
                    right: 10,
                  ),
                  elevation: 5,
                  child: InkWell(
                    splashColor: Colors.black.withAlpha(40),
                    onTap: () => launch("tel://9740547920"),
                    child: new ListTile(
                      leading: new Icon(Icons.phone),
                      title: const Text('Phone Number'),
                      subtitle: new Text('9740547920'),
                    ),
                  ),
                ),
                Card(
                  margin: EdgeInsets.only(
                    top: 10,
                    bottom: 10,
                    left: 10,
                    right: 10,
                  ),
                  elevation: 5,
                  child: InkWell(
                    splashColor: Colors.black.withAlpha(40),
                    onTap: () => launch("mailto:contact@ohzas.com?subject=Contact from Ohzas App"),
                    child: new ListTile(
                      leading: new Icon(Icons.email),
                      title: const Text('Email Address'),
                      subtitle: new Text('contact@ohzas.com'),
                    ),
                  ),
                ),
                Card(
                  margin: EdgeInsets.only(
                    top: 10,
                    bottom: 10,
                    left: 10,
                    right: 10,
                  ),
                  elevation: 5,
                  child: InkWell(
                    splashColor: Colors.black.withAlpha(40),
                    onTap: () => launch("https://www.ohzas.com"),
                    child: new ListTile(
                      leading: new Icon(Icons.web_asset),
                      title: const Text('Website'),
                      subtitle: new Text('www.ohzas.com'),
                    ),
                  ),
                ),
                Card(
                  margin: EdgeInsets.only(
                    top: 10,
                    bottom: 10,
                    left: 10,
                    right: 10,
                  ),
                  elevation: 5,
                  child: InkWell(
                    splashColor: Colors.black.withAlpha(40),
                    onTap: () => launch("https://www.ohzas.com"),
                    child: new ListTile(
                      leading: new Icon(Icons.code),
                      title: const Text('Service Registration'),
                      //subtitle: new Text(_projectCode),
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
}
