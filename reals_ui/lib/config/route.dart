import 'package:fluro/fluro.dart';
import 'package:flutter/material.dart';
import 'package:reals_ui/pages/forget_password_page.dart';
import 'package:reals_ui/pages/login_page.dart';
import 'package:reals_ui/pages/main_page.dart';
import 'package:reals_ui/pages/question_page.dart';
import 'package:reals_ui/pages/sign_up_page.dart';

class FluroRouterApplication {
  static FluroRouter router = FluroRouter();

  static void setupRouter() {
    router.define('/', handler: Handler(
      handlerFunc: (BuildContext? context, Map<String, dynamic> params) {
        debugPrint('routeHere /admin');
        return MainPage();
      },
    ), transitionType: TransitionType.fadeIn);
  router.define('/login',handler: Handler(
      handlerFunc: (BuildContext? context, Map<String, dynamic> params) {
        debugPrint('routeHere /admin');
        return LoginPage();
      },
    ), transitionType: TransitionType.fadeIn);
     router.define('/signUp',handler: Handler(
      handlerFunc: (BuildContext? context, Map<String, dynamic> params) {
        debugPrint('routeHere /admin');
        return SignUpPage();
      },
    ), transitionType: TransitionType.fadeIn);
    router.define('/forgetPassword',handler: Handler(
      handlerFunc: (BuildContext? context, Map<String, dynamic> params) {
        debugPrint('routeHere /admin');
        return ForgetPasswordPage();
      },
    ), transitionType: TransitionType.fadeIn);
  router.define('/question',handler: Handler(
      handlerFunc: (BuildContext? context, Map<String, dynamic> params) {
        debugPrint('routeHere /admin');
        return QuestionsPage();
      },
    ), transitionType: TransitionType.fadeIn);
    // initIntergrationIntance(router);
  }
}
