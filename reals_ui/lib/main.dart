import 'package:reals_ui/app.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:reals_ui/config/config.dart';
import 'package:reals_ui/config/route.dart';
import 'package:reals_ui/services/dio_web_server_manager.dart';
import 'package:sp_util/sp_util.dart';
import 'package:equatable/equatable.dart';
import 'helper/helper_management.dart';
import 'package:easy_localization/easy_localization.dart';

Future<void> startup(String env) async {
  debugPrint("start Up call $env");
  WidgetsFlutterBinding.ensureInitialized();

  await dotenv.load(fileName: env);
  await SpUtil.getInstance();

  if (SpHelper.isFirstOpen()) {
    SpHelper.putObject(Config.isFirstOpen, true);
    SpHelper.putObject(Config.initLang, 'en-US');
  }

  // Get.updateLocale(getLocale());
  DioWebServerManager().init(true, dotenv.env['API_HOST'].toString());

  FluroRouterApplication.setupRouter();

  EquatableConfig.stringify = kDebugMode;

  // await Get.putAsync(() => AppService().init());
  debugPrint = (String? message, {int? wrapWidth}) =>
      debugPrintSynchronouslyWithText(message);
  WidgetsFlutterBinding.ensureInitialized();
  await EasyLocalization.ensureInitialized();
  runApp(
    EasyLocalization(
        supportedLocales: [Locale('en', 'US'), Locale('zh', 'HK')],
        path:
            'assets/translations', // <-- change the path of the translation files
        fallbackLocale: Locale('en', 'US'),
        child: MyApp()),
  );
}

void debugPrintSynchronouslyWithText(String? message) {
  message = "[${DateTime.now()}]: $message";
  debugPrintSynchronously(message);
}


void main() {
  // runApp(const MyApp());
   const env = String.fromEnvironment('ENV', defaultValue: 'assets/.env.dev');
  startup(env);
}