//import 'package:clipboard_manager/clipboard_manager.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get_version/get_version.dart';
import 'package:ohzasProvider/util/toast_util.dart';
import 'package:package_info/package_info.dart';

class AboutPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _AboutPage();
  }
}

class _AboutPage extends State<AboutPage> {
  String _platformVersion = 'Unknown';
  String _projectVersion = '';
  String _projectCode = '';
  String _projectAppID = '';
  String _projectName = '';

  @override
  initState() {
    super.initState();
    initPlatformState();
  }

  // Platform messages are asynchronous, so we initialize in an async method.
  initPlatformState() async {
    String platformVersion;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      platformVersion = await GetVersion.platformVersion;
    } catch (e) {
      platformVersion = 'Failed to get platform version.';
    }

    String projectVersion;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      projectVersion = await GetVersion.projectVersion;
    } catch (e) {
      projectVersion = 'Failed to get project version.';
    }

    String projectCode;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      projectCode = await GetVersion.projectCode;
    } catch (e) {
      projectCode = 'Failed to get build number.';
    }

    String projectAppID;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      projectAppID = await GetVersion.appID;
    } catch (e) {
      projectAppID = 'Failed to get app ID.';
    }

    String projectName;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      projectName = await GetVersion.appName;
    } catch (e) {
      projectName = 'Failed to get app name.';
    }

    // If the widget was removed from the tree while the asynchronous platform
    // message was in flight, we want to discard the reply rather than calling
    // setState to update our non-existent appearance.
    PackageInfo packageInfo = await PackageInfo.fromPlatform();

    String appName = packageInfo.appName;
    String packageName = packageInfo.packageName;
    String version = packageInfo.version;
    String buildNumber = packageInfo.buildNumber;

    if (!mounted) return;

    setState(() {
      _platformVersion = platformVersion;
      _projectVersion = projectVersion;
      _projectCode = projectCode;
      _projectAppID = projectAppID;
      _projectName = projectName;
    });
  }

  @override
  Widget build(BuildContext context) {
    return new WillPopScope(
      onWillPop: null,
      child: new Scaffold(
        appBar: new AppBar(
          title: new Text(
            'About',
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
                    onTap: () {
                      onClickCopy(copyText: _projectName);
                    },
                    child: new ListTile(
                      leading: new Icon(Icons.apps),
                      title: const Text('Name'),
                      subtitle: new Text(_projectName),
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
                    onTap: () {
                      onClickCopy(copyText: _platformVersion);
                    },
                    child: new ListTile(
                      leading: new Icon(Icons.computer),
                      title: const Text('Running On'),
                      subtitle: new Text(_platformVersion),
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
                    onTap: () {
                      onClickCopy(copyText: _projectVersion);
                    },
                    child: new ListTile(
                      leading: new Icon(Icons.assignment),
                      title: const Text('Version Name'),
                      subtitle: new Text(_projectVersion),
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
                    onTap: () {
                      onClickCopy(copyText: _projectCode);
                    },
                    child: new ListTile(
                      leading: new Icon(Icons.code),
                      title: const Text('Version Code'),
                      subtitle: new Text(_projectCode),
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

  onClickCopy({String copyText = ''}) async {
    await Clipboard.setData(ClipboardData(text: copyText));
    Toaster.i(context, message: 'Copied to Clipboard');
  }
}
