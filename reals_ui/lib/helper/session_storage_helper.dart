import 'dart:convert';
import 'package:easy_localization/easy_localization.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sp_util/sp_util.dart';

import '../config/config.dart';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
// class LanguageCode {
//   static const String en = 'en_US';
//   static const String zh = 'zh_CN';
//   static const String ja = 'ja_JP';
// }

enum LanguageCode {
  en_US, // English
  zh_HK, // Chinese
  ja_JP, // Japanese
}

extension LanguageCodeExtension on LanguageCode {
  Locale get value {
    switch (this) {
      case LanguageCode.en_US:
        return Locale('en', 'US');
      case LanguageCode.zh_HK:
        return Locale('zh', 'HK');
      case LanguageCode.ja_JP:
        return Locale('ja', 'JP');
      default:
        throw Exception('Unsupported language code');
    }
  }
}

class SpHelper {
  static String languageCode = SpUtil.getString(Config.initLang).toString();
  static void putObject<T>(String key, value) {
    switch (T) {
      case int:
        SpUtil.putInt(key, value);
        break;
      case double:
        SpUtil.putDouble(key, value);
        break;
      case bool:
        SpUtil.putBool(key, value);
        break;
      case String:
        SpUtil.putString(key, value);
        break;
      case List:
        if (value is List<String>) {
          SpUtil.putStringList(key, value);
        } else {
          SpUtil.putObjectList(key, value);
        }
        break;
      default:
        SpUtil.putString(key, value == null ? "" : json.encode(value));
        break;
    }
  }

  // static String getLanguage() {
  //   String? _appLanguage = SpUtil.getString(Config.currentLang);
  //   if (_appLanguage is String ) {
  //     return _appLanguage;
  //   }
  //
  //   return 'en';
  // }

  static String getLanguageCode(BuildContext context) {
    return context.locale.languageCode;
  }

  static void setLanguageCode(BuildContext context, LanguageCode code) {
    context.setLocale(code.value);
    Get.updateLocale(code.value);
  }

  static String authToken() {
    String? _authToken = SpUtil.getString(Config.keyAuthToken);
    if (_authToken is String) {
      return _authToken;
    }
    return '';
  }

  static bool isFirstOpen() {
    bool? _isFirstOpen = SpUtil.getBool(Config.isFirstOpen);
    if (_isFirstOpen is bool) {
      return _isFirstOpen;
    }
    return false;
  }
}

class FlutterSecureStorageHelper{
  var secureStorage = new FlutterSecureStorage();

  void writeString(String key, String value){
    secureStorage.write(key: key, value: value);
  }

  Future<String?> getString(String key) async {
    return await secureStorage.read(key: key);
  }
}