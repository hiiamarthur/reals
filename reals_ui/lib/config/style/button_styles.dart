import 'package:flutter/material.dart';
import 'index.dart';

class ButtonStyles {
  static ButtonStyle general = ButtonStyle(
    elevation: WidgetStateProperty.all<double>(0.0),
    textStyle: WidgetStateProperty.all<TextStyle>(
        const TextStyle(color: AppColors.mainRed)),
  );

  static ButtonStyle main = ButtonStyle(
    padding: WidgetStateProperty.all<EdgeInsets>(Paddings.s10),
    elevation: WidgetStateProperty.all<double>(0.0),
    shape: WidgetStateProperty.all<RoundedRectangleBorder>(
        RoundedRectangleBorder(borderRadius: BorderRadius.circular(20.0))),
    backgroundColor: WidgetStateProperty.all<Color>(AppColors.mainRed),
    textStyle: WidgetStateProperty.all<TextStyle>(
        const TextStyle(color: AppColors.appWhite)),
  );

  static ButtonStyle blockButton = ButtonStyle(
    backgroundColor: WidgetStateProperty.resolveWith<Color>(
      (_) {
        if (_.isNotEmpty) return AppColors.mainRed.withOpacity(.5);

        return AppColors.mainRed;
      },
    ),
    foregroundColor: WidgetStateProperty.all<Color>(AppColors.appWhite),
  );

  static ButtonStyle outlinedButton = ButtonStyle(
    backgroundColor: WidgetStateProperty.all<Color>(AppColors.appWhite),
    // shape: WidgetStateProperty.all<OutlinedBorder>(
    //   RoundedRectangleBorder(
    //     borderRadius: BorderRadius.circular(Dimens.borderRadius),
    //     side: const BorderSide(width: 1.0, color: AppColors.btnOutlinedBorder),
    //   ),
    // ),
     shape: WidgetStateProperty.all<RoundedRectangleBorder>(
        RoundedRectangleBorder(borderRadius: BorderRadius.circular(20.0))),
    shadowColor:
        WidgetStateProperty.all<Color>(AppColors.appBlack.withOpacity(0.1)),
    elevation: WidgetStateProperty.all<double>(17.0),
  );

  static ButtonStyle mergeStyles(ButtonStyle defaultStyle, ButtonStyle? overrideStyle) {
    return defaultStyle.copyWith(
      padding: overrideStyle?.padding ?? defaultStyle.padding,
      elevation: overrideStyle?.elevation ?? defaultStyle.elevation,
      shape: overrideStyle?.shape ?? defaultStyle.shape,
      backgroundColor: overrideStyle?.backgroundColor ?? defaultStyle.backgroundColor,
      textStyle: overrideStyle?.textStyle ?? defaultStyle.textStyle,
    );
  }
}
