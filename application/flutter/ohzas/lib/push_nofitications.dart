import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:fluttertoast/fluttertoast.dart';

class PushNotificationsManager {
  PushNotificationsManager._();

  factory PushNotificationsManager() => _instance;

  static final PushNotificationsManager _instance =
      PushNotificationsManager._();

  final FirebaseMessaging _firebaseMessaging = FirebaseMessaging();

  bool _initialized = false;

  Future<void> init() async {
    if (!_initialized) {
      // For iOS request permission first.
      //_firebaseMessaging.subscribeToTopic('Test');
      _firebaseMessaging.requestNotificationPermissions();
      _firebaseMessaging.configure(
        onMessage: (Map<String, dynamic> message) async {
          print("onMessage: $message");
        },
        onLaunch: (Map<String, dynamic> message) async {
          print("onLaunch: $message");
          Fluttertoast.showToast(msg: "onResume $message");
        },
        onResume: (Map<String, dynamic> message) async {
          print("onResume: $message");
          Fluttertoast.showToast(msg: "onResume $message");
        },
      );

      // For testing purposes print the Firebase Messaging token
      String token = await _firebaseMessaging.getToken();
      print("FirebaseMessaging token: $token");

      _initialized = true;
    }
  }
}
