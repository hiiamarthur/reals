//
import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:dio/dio.dart';
import 'package:reals_ui/class/dio.dart';
import 'package:reals_ui/helper/helper_management.dart';

class DioWebServerManager {
  static final DioWebServerManager _instance = DioWebServerManager._internal();

  factory DioWebServerManager() {
    return _instance;
  }

  DioWebServerManager._internal();

  static const Duration _defaultConnectTimeout = Duration(days: 1);
  static const Duration _defaultReceiveTimeout = Duration(seconds: 10);

  late Dio _dio;

  Map<String, dynamic> get _baseHeaders => <String, dynamic>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
      };

  void init(bool isDebug, String baseUrl,
      {Duration connectTimeout = _defaultConnectTimeout,
      Duration receiveTimeout = _defaultReceiveTimeout}) {
    BaseOptions baseOptions = BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: connectTimeout,
        receiveTimeout: receiveTimeout,
        responseType: ResponseType.json,
        headers: _baseHeaders);
    _dio = Dio(baseOptions)..interceptors.add(LogInterceptor());
  }

  void _ensureInitialized() {
    
  }

  void _updateHeaders() {
    _ensureInitialized();
    String token = SpHelper.authToken();
    debugPrint("call api token = " + token);
    if (token.isNotEmpty) {
      _dio.options.headers["Authorization"] = "Bearer $token";
    }
  }

  Future<dynamic> get(String url, {data, options, authenticated = true}) async {
    _ensureInitialized();
    debugPrint('getRequest:==>path:$url   params:$data');
    _updateHeaders();
    try {
      var res = await _dio.get(url, queryParameters: data, options: options);
      debugPrint("res IS ${res}");
      var resData = res.data as Map<String, dynamic>;
      var formattedRes = DioResponse.fromJson(resData);
      debugPrint("res ${res.data} ${formattedRes}");
      return formattedRes.result;
    } catch (e) {
      debugPrint("DioWebServerManager.get() catch exception ====> $e");
      rethrow;
    }
  }

  Future<dynamic> post(String url, {parameters, data, options, authenticated = true}) async {
    _ensureInitialized();
    debugPrint('postRequest:==>path:$url   params:$data');
    if(authenticated)
      _updateHeaders();
    try {
      return await _dio.post(url,
          queryParameters: parameters, data: data, options: options);
    } catch (e) {
      debugPrint("DioWebServerManager.post() catch exception ====> $e");
      rethrow;
    }
  }
}
