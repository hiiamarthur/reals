import 'dart:developer';

import 'package:flutter/cupertino.dart';
import 'package:sp_util/sp_util.dart';
import 'package:get/get.dart';
import '../config/config.dart';
import '../helper/helper_management.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

AndroidOptions _getAndroidOptions() => const AndroidOptions(
      encryptedSharedPreferences: true,
    );
IOSOptions _getIOSOptions() => const IOSOptions(
  
);

class AppService extends GetxService {
  late String _unConfirmedToken;
  String get unConfirmedToken => _unConfirmedToken;

  late String _unConfirmedJwtToken;
  String get unConfirmedJwtToken => _unConfirmedJwtToken;
  late String _token;
  String get token => _token;
  late String _jwt;
  String get jwt => _jwt;

  // CustomUser? _user;
  // CustomUser? get user => _user;
  // UserCredential? _userCredential;
  // UserCredential? get userCredential => _userCredential;
  late bool _authenticated = false;
  bool get authenticated => _authenticated;
  String appleLatestVersion = '1.0.0';
  String androidLatestVersion = '1.0.0';
  bool appleForceUpdate = false;
  bool androidForceUpdate = false;

  // Create storage
  // final storage = const FlutterSecureStorage();
  final storage = FlutterSecureStorage(aOptions: _getAndroidOptions(),iOptions: _getIOSOptions());

  Future<AppService> init() async {
    _token = SpHelper.authToken();

    await status();
    debugPrint('$runtimeType ready!');

    return this;
  }

  @override
  void onReady() async {
    super.onReady();
    debugPrint('App onReady');
    await storage.readAll().then((value) {
      debugPrint("storage:" + inspect(value).toString());
    });
  }

  Future<String> readyToGoHome() async {
    await 1.delay();
    if (authenticated) {
      return '/home';
    }
    return '/welcome';
  }

  Future checkUserSession() async {
    debugPrint("Calling app_sserive.Print");
    var body = {
      "token": SpUtil.getString(Config.keyAuthToken),
    };

    // await firebase.verifyCredential(body).then((value) async {
    //   if(value is ErrorResponse){
    //     debugPrint("errorResponse:"+inspect(value.error).toString());
    //     if(value.error['code'] == FirebaseAuthError.idTokenExpired){
    //       body = {
    //         "token": SpUtil.getString(Config.refreshToken),
    //       };
    //       await firebase.updateIdToken(body);
    //       debugPrint("errorResponse:"+inspect(SpUtil.getString(Config.refreshToken)).toString());
    //     }
    //   }else if (value is SuccessResponse){
    //     debugPrint("value:" + inspect(firebase.auth.currentUser).toString());
    //     SpUtil.putObject(Config.userCredential,value.results['user']);
    //
    //     setAuthenticated(true);
    //   }
    // });
  }

  Future status() async {
    // await GunKulAPI.status(jwt: _token).then((value) {
    //   if (value is SuccessResponse) {
    //     if (value.results['authenticated']) {
    //       _setAuthenticatedData(
    //         authenticated: true,
    //         user: value.results['user'],
    //         token: value.results['token'],
    //       );
    //     } else {
    //       _setAuthenticatedData(
    //         authenticated: false,
    //         user: null,
    //         token: '',
    //       );
    //     }
    //     appleLatestVersion = value.results['appleLatestVersion'];
    //     androidLatestVersion = value.results['androidLatestVersion'];
    //     appleForceUpdate = value.results['appleForceUpdate'];
    //     androidForceUpdate = value.results['androidForceUpdate'];

    //     return value.results;
    //   } else if (value is ErrorResponse) {}

    //   return <String, dynamic>{};
    // });
  }

  _setAuthenticatedData({
    required bool authenticated,
    required String token,
    // required User? user
  }) {
    // setUser(user);
    _token = token;
    SpUtil.putString(Config.keyAuthToken, _token);
    setAuthenticated(authenticated);
  }

  // login({required String token, required User user}) {
  //   if (!(user.confirmed ?? false)) {
  //     _unConfirmedToken = token;
  //     setUnConfirmedUser(user);
  //     setAuthenticated(false);
  //   } else {
  //     _unConfirmedToken = '';
  //     setUnConfirmedUser(null);
  //     setUser(user);
  //     _token = token;
  //     SpUtil.putString(Config.keyAuthToken, _token);
  //     setAuthenticated(true);
  //   }
  // }

  login(
      {required String authToken,
      required String jwtToken,
      required dynamic userCredential,
      required String refreshToken}) {
    debugPrint('call AppService Login...');
    // if (!(userCredential.user.confirmed ?? false)) {
    //   _unConfirmedJwtToken = jwtToken;
    //   setUnConfirmedUser(user);
    //   setAuthenticated(false);
    // } else {
    _unConfirmedJwtToken = '';
    // setUnConfirmedUser(null);
    // setUser(user);
    _token = authToken;
    SpUtil.putString(Config.keyAuthToken, authToken);
    storage.write(key: Config.keyAuthToken, value: authToken);
    _jwt = jwtToken;
    SpUtil.putString(Config.jwt, jwtToken);
    SpUtil.putObject(Config.userCredential, userCredential);
    SpUtil.putString(Config.refreshToken, refreshToken);
    setAuthenticated(true);
    storage.write(key: Config.jwt, value: jwtToken); // }
  }

  logout() {
    debugPrint('call logout...');
    // setUser(null);
    _token = '';
    SpUtil.putString(Config.jwt, _token);
    SpUtil.putString(Config.keyAuthToken, _token);
    setAuthenticated(false);
  }

  // setUser(User? user) {
  //   if (user is User) {
  //     _user = user;
  //   } else {
  //     _user = null;
  //   }
  // }

  // setUnConfirmedUser(User? user) {
  //   if (user is User) {
  //     _unConfirmedUser = user;
  //   } else {
  //     _unConfirmedUser = null;
  //   }
  // }

  setAuthenticated(bool? authenticated) {
    _authenticated = authenticated ?? false;
  }

  Future testApiFunc() async {
    return await Future.delayed(const Duration(milliseconds: 30));
  }
}
