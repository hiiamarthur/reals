// ignore_for_file: prefer_const_constructors

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'index.dart';

const double commonRadius = 5.0;

class AppTheme {
  AppTheme._();
  static const double baseScreenWidth = 1080.0;
  static const double baseScreenHeigh = 1920.0;
  static double _calculateTextSize(double baseSize) {
    double screenWidth =
        // ignore: deprecated_member_use
        MediaQueryData.fromView(WidgetsBinding.instance.window).size.width;
    double scaleFactor = screenWidth / baseScreenWidth;
    return baseSize * scaleFactor;
  }

  // Light Theme
  static final ThemeData lightTheme = ThemeData(
      // brightness: Brightness.light,
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.appBlack,
        elevation: 0.0,
        iconTheme:
            ThemeData.light().iconTheme.copyWith(color: AppColors.appBlack),
        titleTextStyle: TextTheme(
          headlineLarge: TextStyles.h18w500.copyWith(
            color: AppColors.textColor,
          ),
        ).headlineLarge,
      ),
      tabBarTheme: const TabBarTheme(
        labelColor: Colors.black, // Selected tab text color
        unselectedLabelColor: Colors.black54, // Unselected tab text color
        indicatorColor: Colors.black, // Color of the tab indicator
        labelStyle: TextStyle(
          fontWeight: FontWeight.bold, // Text style for selected tab
          fontSize: 18, // Increased font size for better visibility
        ),
        unselectedLabelStyle: TextStyle(
          fontWeight: FontWeight.normal, // Text style for unselected tab
          fontSize: 16, // Slightly smaller font size for unselected
        ),
      ),
      checkboxTheme: const CheckboxThemeData(
        side: BorderSide(width: 1.0),
      ),
      primaryColor: Colors.white,
      inputDecorationTheme: InputDecorationTheme(
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 20, vertical: 10.0),
        labelStyle: const TextStyle(),
        hintStyle: TextStyles.h14w500,
        errorMaxLines: 2,
        filled: true,
        fillColor: Colors.white, // Background color of the input
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0), // Rounded corners
          borderSide: BorderSide(
            color: Colors.grey, // Default border color
            width: 1.0,
          ),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0), // Rounded corners
          borderSide: BorderSide(
            color: Colors.black, // Color when focused
            width: 1.5,
          ),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0), // Rounded corners
          borderSide: BorderSide(
            color: Colors.red, // Color when there is an error
            width: 1.5,
          ),
        ),

        // hintStyle: TextStyle(
        //   color: Colors.grey, // Hint text color
        // ),
        // labelStyle: TextStyle(
        //   color: Colors.grey, // Label text color
        // ),
      ),
      buttonTheme: const ButtonThemeData(
        buttonColor: Colors.white, //  <-- light color
        textTheme:
            ButtonTextTheme.primary, //  <-- dark text for light background
      ),
      scaffoldBackgroundColor: AppColors.appWhite,
      textButtonTheme: TextButtonThemeData(style: ButtonStyles.general),
      elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10.0)),
              textStyle: TextStyle(
                color: Color(0xFF454545),
                fontSize: _calculateTextSize(52.5),
                fontFamily: 'Roboto',
                fontWeight: FontWeight.bold,
                height: 1.2,
                letterSpacing: _calculateTextSize(0.15),
              ))),
      iconButtonTheme: IconButtonThemeData(
        style: IconButton.styleFrom(
          padding: Paddings.h10
        )
      ),
      // outlinedButtonTheme: OutlinedButtonThemeData(
      //   style: ButtonStyle(
      //     shape: MaterialStateProperty.resolveWith<OutlinedBorder>((_) {
      //       return RoundedRectangleBorder(
      //           borderRadius: BorderRadius.circular(5));
      //     }),
      //   ),
      // ),
      sliderTheme: SliderThemeData(
          trackHeight: 4.0, // Height of the track
          trackShape: RoundedRectSliderTrackShape(), // Rounded track
          activeTrackColor: AppColors.appRed, // Active track color (red)
          inactiveTrackColor: Colors.black, // Inactive track color
          thumbColor: AppColors.appRed, // Thumb color
          thumbShape: RoundSliderThumbShape(enabledThumbRadius: 12.0), // Thumb shape
          overlayColor: AppColors.appRed.withOpacity(0.2), // Overlay color
          valueIndicatorColor: AppColors.appRed, // Value indicator color
          valueIndicatorShape: PaddleSliderValueIndicatorShape(), // Shape of value indicator
        ),
      colorScheme: const ColorScheme.highContrastLight(
        primary: AppColors.appMain,
        secondary: AppColors.appRed,
      ),
      dialogBackgroundColor: AppColors.appWhite,
      highlightColor: AppColors.transparent,
      splashColor: AppColors.transparent,
      dividerColor: AppColors.inputBorder,
      cupertinoOverrideTheme: const CupertinoThemeData(
          textTheme: CupertinoTextThemeData(
        dateTimePickerTextStyle: TextStyle(color: Colors.white, fontSize: 16),
        pickerTextStyle: TextStyle(color: Colors.white, fontSize: 12),
      )
      )
      ,datePickerTheme: DatePickerThemeData(
        todayForegroundColor: WidgetStateProperty.all<Color>(AppColors.textBlack),
        confirmButtonStyle: ButtonStyles.blockButton,
        cancelButtonStyle: ButtonStyles.blockButton,
        // actionForegroundColor: WidgetStateProperty.all<Color>(AppColors.appBlack)
      ),
      timePickerTheme: TimePickerThemeData(
        cancelButtonStyle: ButtonStyles.main,
        confirmButtonStyle: ButtonStyles.main
      ),
      chipTheme: ChipThemeData(
        side: BorderSide.none
      )
      );
      
}
