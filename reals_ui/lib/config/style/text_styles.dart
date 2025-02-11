import 'package:flutter/material.dart';

import 'index.dart';

class TextStyles {
// button
  static TextStyle buttonText = h14w500.copyWith(color: AppColors.mainRed);

  static TextStyle h10 =
      const TextStyle(fontSize: Dimens.h10, color: AppColors.textColor);
  static TextStyle h12 =
      const TextStyle(fontSize: Dimens.h12, color: AppColors.textColor);
  static TextStyle h14 =
      const TextStyle(fontSize: Dimens.h14, color: AppColors.textColor);
  static TextStyle h16 =
      const TextStyle(fontSize: Dimens.h16, color: AppColors.textColor);
  static TextStyle h18 =
      const TextStyle(fontSize: Dimens.h18, color: AppColors.textColor);
  static TextStyle h20 =
      const TextStyle(fontSize: Dimens.h20, color: AppColors.textColor);
  static TextStyle h21 =
      const TextStyle(fontSize: Dimens.h21, color: AppColors.textColor);
  static TextStyle h30 =
      const TextStyle(fontSize: Dimens.h30, color: AppColors.textColor);

  /// 10
  static TextStyle h10w300 = h10.copyWith(fontWeight: FontWeight.w300);

  /// 12
  static TextStyle h12w400 = h12.copyWith(fontWeight: FontWeight.w400);
  static TextStyle h12w500 = h12.copyWith(fontWeight: FontWeight.w500);

  /// 14
  static TextStyle h14w400 = h14.copyWith(fontWeight: FontWeight.w400);
  static TextStyle h14w500 = h14.copyWith(fontWeight: FontWeight.w500);

  /// 16
  static TextStyle h16w500 = h16.copyWith(fontWeight: FontWeight.w500);

  /// 18
  static TextStyle h18w500 = h18.copyWith(fontWeight: FontWeight.w500);
  static TextStyle h18w600 = h18.copyWith(fontWeight: FontWeight.w600);
  static TextStyle h18w900 = h18.copyWith(fontWeight: FontWeight.w900);

  /// 20
  static TextStyle h20w700 = h20.copyWith(fontWeight: FontWeight.w700);

  /// 21
  static TextStyle h21w700 = h21.copyWith(fontWeight: FontWeight.w700);
  static TextStyle h22w600 =
      h21.copyWith(fontWeight: FontWeight.w600, letterSpacing: -1.41);

  /// 30
  static TextStyle h30w900 = h30.copyWith(fontWeight: FontWeight.w900);

  static TextStyle headline1 = h20w700;
  static TextStyle headline2 = h18w600;
  static TextStyle headline3 = h16w500;
  static TextStyle headline4 = h14w500;
  static TextStyle headline5 = h12w400;
  static TextStyle headline6 = h10w300;
  static TextStyle subtitle1 = h14w400;
  static TextStyle subtitle2 = h12w500;
  static TextStyle bodyText1 = h14w500;
  static TextStyle bodyText2 = h14w400;
}
