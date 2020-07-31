import 'dart:developer';

// Log Utils class
class Log {
//  For Information py_log
  static i([var tag = '', var message = '']) {
    log('[I] ' + tag.toString() + ' ' + message.toString());
  }

//  For error py_log
  static e([var tag = '', var message = '']) {
    log('[E] ' + tag.toString() + ' ' + message.toString());
  }

//  For debug py_log
  static d([var tag = '', var message = '']) {
    log('[D] ' + tag.toString() + ' ' + message.toString());
  }

//  For warning py_log
  static w([var tag = '', var message = '']) {
    log('[W] ' + tag.toString() + ' ' + message.toString());
  }

//  Showing results py_log
  static r([var tag = '', var message = '']) {
    log('[R] ' + tag.toString() + ' ' + message.toString());
  }
}
