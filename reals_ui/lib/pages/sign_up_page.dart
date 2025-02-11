import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Trans;
import 'package:reals_ui/component/text_field.dart';
import 'package:reals_ui/config/style/index.dart';
import 'package:reals_ui/controllers/login_controller.dart';
import 'package:reals_ui/widgets/app_button.dart';
import 'package:reals_ui/widgets/app_spacer.dart';

class SignUpPage extends StatefulWidget {
  const SignUpPage({Key? key}) : super(key: key);

  @override
  createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  LoginController _controller = Get.find();
  @override
  void initState() {
    super.initState();
  }

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
                      "Create An Account",
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
                      hintText: "Username or email",
                      prefixIcon: Image.asset("assets/images/username.png"),
                    ),
                    SizedBox(height: 20),
                    CustomTextField(
                      backgroundColor: AppColors.appGrey,
                      borderStyle: OutlineInputBorder(
                          borderSide: BorderSide(
                              color: Color.fromARGB(255, 232, 216, 220)),
                          borderRadius: BorderRadius.all(Radius.circular(20))),
                      hintText: "Password",
                      prefixIcon: Image.asset("assets/images/lock.png"),
                      isPassword: true,
                    ),
                    SizedBox(height: 20),
                    CustomTextField(
                      backgroundColor: AppColors.appGrey,
                      borderStyle: OutlineInputBorder(
                          borderSide: BorderSide(
                              color: Color.fromARGB(255, 232, 216, 220)),
                          borderRadius: BorderRadius.all(Radius.circular(20))),
                      hintText: "Confirm Password",
                      prefixIcon: Image.asset("assets/images/lock.png"),
                      isPassword: true,
                    ),
                    SizedBox(height: 10),
                    Text("By clicking the Register button, you agree to the public offer"),
                    
                    SizedBox(height: 40),
                     SizedBox(
                        width: double.infinity,
                        child: AppButton.main(
                          "Create Account",
                          style: ButtonStyle(
                            padding: WidgetStateProperty.all<EdgeInsets>(
                                Paddings.s40),
                            elevation: WidgetStateProperty.all<double>(0.0),
                            shape:
                                WidgetStateProperty.all<RoundedRectangleBorder>(
                                    RoundedRectangleBorder(
                                        borderRadius:
                                            BorderRadius.circular(2.0))),
                          ),
                          textStyle: TextStyle(
                              fontSize: 20, color: AppColors.appWhite),
                        )),
                    SizedBox(height: 50),
                    Text(
                      "- Or Continue with -",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                        fontFamily: 'Montserrat',
                      ),
                    ),
                    SizedBox(height: 20),
                    Align(
                      alignment: Alignment.topCenter,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          GestureDetector(
                            onTap: () {
                              Get.toNamed("/google-SignUp");
                            },
                            child: Image.asset("assets/images/google.png"),
                          ),
                          GestureDetector(
                            onTap: () {
                              Get.toNamed("/apple-SignUp");
                            },
                            child: Image.asset("assets/images/apple.png"),
                          ),
                          GestureDetector(
                            onTap: () {
                              Get.toNamed("/facebook-SignUp");
                            },
                            child: Image.asset("assets/images/facebook.png"),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          "I Already have an account.",
                          style: TextStyle(
                            fontWeight: FontWeight.w100,
                            fontSize: 12,
                            fontFamily: 'Montserrat',
                          ),
                        ),
                        AppSpacer.w5(),
                        GestureDetector(
                          onTap: () {
                            Get.toNamed("/login");
                          },
                          child: Text(
                            "Login",
                            style: TextStyle(
                              color: Color.fromARGB(255, 228, 74, 92),
                              fontWeight: FontWeight.bold,
                              fontSize: 12,
                              fontFamily: 'Montserrat',
                            ),
                          ),
                        ),
                      ],
                    )
                  ],
                ),
              );
            }));
  }
}

class SignUpPageBody extends StatefulWidget {
  const SignUpPageBody({Key? key}) : super(key: key);
  @override
  createState() => _SignUpPageBodyState();
}

class _SignUpPageBodyState extends State<SignUpPageBody> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [AppButton(child: Text("test"))],
    );
  }
}
