import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Trans;
import 'package:reals_ui/component/text_field.dart';
import 'package:reals_ui/config/style/index.dart';
import 'package:reals_ui/controllers/login_controller.dart';
import 'package:reals_ui/widgets/app_button.dart';

class ForgetPasswordPage extends StatefulWidget {
  const ForgetPasswordPage({Key? key}) : super(key: key);

  @override
  createState() => _ForgetPasswordPageState();
}

class _ForgetPasswordPageState extends State<ForgetPasswordPage> {
  @override
  void initState() {
    super.initState();
  }

  LoginController _controller = Get.find();
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
        // appBar: AppBar(
        //   title: Text('Questions Bar - 8 Stages'),
        //   centerTitle: true,
        // ),
        body: GetBuilder<LoginController>(
            init: _controller,
            builder: (_) {
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Text(
                      "Forget Password",
                      style: TextStyle(
                        fontSize: 60,
                        fontWeight: FontWeight.w600,
                        fontFamily: 'Montserrat',
                      ),
                    ),
                    SizedBox(height: 20),
                    CustomTextField(
                      backgroundColor: AppColors.bgBorderGrey,
                      borderStyle: OutlineInputBorder(
                          borderSide: BorderSide(
                              color: Color.fromARGB(255, 232, 216, 220)),
                          borderRadius: BorderRadius.all(Radius.circular(20))),
                      hintText: "Enter Email Address",
                      prefixIcon: Image.asset("assets/images/username.png"),
                    ),
                    SizedBox(height: 20),
                    Text(
                        "We will send you a message to set or reset your new password"),
                    SizedBox(height: 40),
                    SizedBox(
                        width: double.infinity,
                        child: AppButton.main("Submit",
                            style: ButtonStyle(
                              padding: WidgetStateProperty.all<EdgeInsets>(
                                  Paddings.s20),
                              elevation: WidgetStateProperty.all<double>(0.0),
                              shape: WidgetStateProperty.all<
                                      RoundedRectangleBorder>(
                                  RoundedRectangleBorder(
                                      borderRadius:
                                          BorderRadius.circular(5.0))),
                            ))),
                    SizedBox(height: 50),
                  ],
                ),
              );
            }));
  }
}

class ForgetPasswordPageBody extends StatefulWidget {
  const ForgetPasswordPageBody({Key? key}) : super(key: key);
  @override
  createState() => _ForgetPasswordPageBodyState();
}

class _ForgetPasswordPageBodyState extends State<ForgetPasswordPageBody> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [AppButton(child: Text("test"))],
    );
  }
}
