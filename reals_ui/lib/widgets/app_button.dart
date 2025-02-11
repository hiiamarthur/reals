import 'package:flutter/material.dart';
import 'package:reals_ui/config/style/index.dart';
import 'package:reals_ui/widgets/app_spacer.dart';

class AppButton extends StatelessWidget {
  final Widget child;
  final VoidCallback? onPressed;
  final ButtonStyle? style;
  final EdgeInsets? padding;

  const AppButton({Key? key, required this.child, this.onPressed, this.style, this.padding}) : super(key: key);

  // factory AppButton.main(String title, {VoidCallback? onPressed, ButtonStyle? style, EdgeInsets? padding, TextStyle? textStyle}) => AppButton(
  //       onPressed: onPressed,
  //       style: style ??
  //           ButtonStyles.main.copyWith(
  //             padding: MaterialStateProperty.all<EdgeInsets>(padding ?? Paddings.s10),
  //           ),
  //       child: Text(
  //         title,
  //         style: textStyle ?? TextStyles.h14w500.copyWith(color: AppColors.appWhite),
  //       ),
  //     );
 factory AppButton.main(
    String title, {
    VoidCallback? onPressed,
    ButtonStyle? style, // Optional parameter for custom style
    EdgeInsets? padding, // Optional padding override
    TextStyle? textStyle, // Optional text style override
    // double? radius,
    // Color? borderColor
  }) {
    final ButtonStyle baseStyle = ButtonStyles.main.copyWith(
      // shape: MaterialStateProperty.all<OutlinedBorder>(
      //       RoundedRectangleBorder(
      //         borderRadius: BorderRadius.circular(radius ?? Dimens.borderRadius),
      //         side: BorderSide(color: borderColor ?? AppColors.btnOutlinedBorder),
      //       ),
      //     ),
      padding: WidgetStateProperty.all<EdgeInsets>(padding ?? Paddings.s10),
    );

    // Merge the provided style with the base style
    final ButtonStyle mergedStyle = style != null ? baseStyle.merge(style) : baseStyle;

    return AppButton(
      onPressed: onPressed,
      style: mergedStyle,
      child: Text(
        title,
        style: textStyle ?? TextStyles.h14w500.copyWith(color: AppColors.appWhite),
      ),
    );
  }
  

  factory AppButton.tag(String title, {VoidCallback? onPressed, Color? color}) => AppButton(
        onPressed: onPressed,
        child: Text(
          title,
          style: TextStyles.buttonText.copyWith(color: color),
        ),
      );

  factory AppButton.icon(
    IconData iconData, {
    Color? color,
    VoidCallback? onPressed,
    double size = 30.0,
    ButtonStyle? customStyle,
    EdgeInsets? padding,
  }) {
    // final mergedStyle = ButtonStyles.mergeStyles(
    //   ButtonStyles,
    //   customStyle,
    // );

    // // Further merge with `styleOverride` if provided
    // final finalStyle = ButtonStyles.mergeStyles(
    //   mergedStyle,
    //   styleOverride,
    // );

    return AppButton(
        
        padding: padding,
        onPressed: onPressed,
        style: ButtonStyles.mergeStyles(
            ButtonStyle(
              
              padding: WidgetStateProperty.all<EdgeInsets>(EdgeInsets.zero),
            ), customStyle),
        child: Icon(
          
          iconData,
          size: size,
          color: color ?? AppColors.appBlack,
        ),
      );
  }
      

  factory AppButton.label(
    String title, {
    IconData? leading,
    IconData? trailing,
    Color? leadingColor,
    Color? trailingColor,
    VoidCallback? onPressed,
    TextStyle? textStyle,
    ButtonStyle? style,
    EdgeInsets? padding,
  }) =>
      AppButton(
        onPressed: onPressed,
        style: style ??
            ButtonStyles.main.copyWith(
              padding: WidgetStateProperty.all<EdgeInsets>(padding ?? Paddings.buttonLabel),
            ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (leading != null) ...[
              Icon(
                leading,
                size: 20.0,
                color: leadingColor ?? AppColors.appWhite,
              ),
              AppSpacer.w10(),
            ],
            Text(
              title,
              style: textStyle ?? TextStyles.h14w500.copyWith(color: AppColors.appWhite),
            ),
            if (trailing != null) ...[
              AppSpacer.w5(),
              Icon(
                trailing,
                size: 20.0,
                color: trailingColor ?? AppColors.appWhite,
              ),
            ],
          ],
        ),
      );

  factory AppButton.outlined({
    String? title,
    Widget? icon,
    child,
    EdgeInsets? padding,
    VoidCallback? onPressed,
    Color? borderColor,
    Color? backgroundColor,
    Color? textColor,
    TextStyle? textStyle,
    double? radius,
  }) =>
      AppButton(
        onPressed: onPressed,
        style: ButtonStyles.outlinedButton.copyWith(
          padding: WidgetStateProperty.all<EdgeInsets>(padding ?? EdgeInsets.zero),
          backgroundColor: WidgetStateProperty.all<Color>(backgroundColor ?? AppColors.appWhite),
          // shape: MaterialStateProperty.all<OutlinedBorder>(
          //   RoundedRectangleBorder(
          //     borderRadius: BorderRadius.circular(radius ?? Dimens.borderRadius),
          //     side: BorderSide(color: borderColor ?? AppColors.btnOutlinedBorder),
          //   ),
          // ),
        ),
        child: icon != null
            ? Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  icon,
                  AppSpacer.w5(),
                  child ??
                      Flexible(
                        child: Container(
                          height: 50.0,
                          alignment: Alignment.center,
                          child: Text(
                            title ?? '',
                            style: textStyle ??
                                TextStyles.buttonText.copyWith(
                                  color: textColor ?? AppColors.textColor,
                                ),
                          ),
                        ),
                      ),
                  AppSpacer.w20(),
                ],
              )
            : child ??
                Text(
                  title ?? '',
                  style: textStyle ??
                      TextStyles.buttonText.copyWith(
                        color: textColor ?? AppColors.textColor,
                      ),
                ),
      );

  factory AppButton.withChild({
    String? title,
    String? content,
    Widget? icon,
    EdgeInsets? padding,
    VoidCallback? onPressed,
    Color? borderColor,
    Color? backgroundColor,
    Color? textColor,
    TextStyle? textStyle,
    double? radius,
  }) =>
      AppButton(
        onPressed: onPressed,
        style: ButtonStyles.outlinedButton.copyWith(
          padding: WidgetStateProperty.all<EdgeInsets>(padding ?? EdgeInsets.zero),
          backgroundColor: WidgetStateProperty.all<Color>(backgroundColor ?? AppColors.appWhite),
          shape: WidgetStateProperty.all<OutlinedBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(radius ?? Dimens.borderRadius),
              side: BorderSide(color: borderColor ?? AppColors.btnOutlinedBorder),
            ),
          ),
        ),
        child:
        Container(
          padding: const EdgeInsets.all(20),
          child:
            SizedBox(
            height: 100,
            width: 200,
            child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Container(
                      alignment: Alignment.topLeft,
                      child: Text(title ?? ''),
                    ),
                    AppSpacer.w5(),
                    Expanded(
                      child: Container(
                        height: 50.0,
                        alignment: Alignment.centerRight,
                        child: Row(
                          
                          children: [
                            Expanded(child: Text(content ?? '')),
                            // Text(content ?? ''),
                            const Expanded( 
                              child: Padding(
                              padding: EdgeInsets.only(left: 20),
                              child: Icon(Icons.arrow_right, size: 20.0, color: AppColors.textColor),
                            )),
                          ],
                          
                        ),
                        
                      ),
                    ),
                    AppSpacer.w20(),
                  ],
                )
            )
        )
          
            
      );

  @override
  Widget build(BuildContext context) {
    return TextButton(
      onPressed: onPressed,
      style: style,
      child: child,
    );
  }
}

class BlockButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final ButtonStyle? style;
  final Color? textColor;
  final double? height;
  final TextStyle? textStyle;

  const BlockButton(this.text, {Key? key, this.onPressed, this.style, this.textColor, this.height, this.textStyle}) : super(key: key);

  // factory BlockButton.main(String text, {VoidCallback? onPressed, Color? backgroundColor, Color? borderColor, Color? textColor}) => BlockButton(
  //       text,
  //       onPressed: onPressed,
  //       textColor: textColor ?? AppColors.appWhite,
  //       style: ButtonStyles.outlinedButton.copyWith(
  //         backgroundColor: MaterialStateProperty.all<Color>(backgroundColor ?? AppColors.mainRed),
  //         shape: MaterialStateProperty.all<OutlinedBorder>(
  //           RoundedRectangleBorder(
  //             borderRadius: BorderRadius.circular(Dimens.borderRadius),
  //             side: BorderSide(color: borderColor ?? AppColors.mainRed),
  //           ),
  //         ),
  //       ),
  //     );
   factory BlockButton.main(
    String text, {
    VoidCallback? onPressed,
    Color? backgroundColor,
    Color? borderColor,
    Color? textColor,
    ButtonStyle? styleOverride, // New parameter for optional style override
  }) {
    // Define the custom style if any parameters are provided
    final customStyle = ButtonStyle(
      backgroundColor: backgroundColor != null
          ? WidgetStateProperty.all<Color>(backgroundColor)
          : null,
      shape: borderColor != null
          ? WidgetStateProperty.all<OutlinedBorder>(
              RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(Dimens.borderRadius),
                side: BorderSide(color: borderColor),
              ),
            )
          : null,
      textStyle: textColor != null
          ? WidgetStateProperty.all<TextStyle>(
              TextStyle(color: textColor),
            )
          : null,
    );

    // Merge the default main style with any custom styles or overrides
    final mergedStyle = ButtonStyles.mergeStyles(
      ButtonStyles.main,
      customStyle,
    );

    // Further merge with `styleOverride` if provided
    final finalStyle = ButtonStyles.mergeStyles(
      mergedStyle,
      styleOverride,
    );

    return BlockButton(
      text,
      onPressed: onPressed,
      style: finalStyle,
    );
  }


  factory BlockButton.outlined(String text, {VoidCallback? onPressed, Color? borderColor, Color? textColor, double? height, TextStyle? textStyle}) =>
      BlockButton(
        text,
        onPressed: onPressed,
        height: height,
        textColor: textColor,
        textStyle: textStyle,
        style: ButtonStyles.outlinedButton.copyWith(
          shape: WidgetStateProperty.all<OutlinedBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(Dimens.borderRadius),
              side: BorderSide(color: borderColor ?? AppColors.btnOutlinedBorder),
            ),
          ),
        ),
      );

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: height ?? 45.0,
      width: double.infinity,
      child: AppButton.main(
        text,
        onPressed: onPressed,
        textStyle: textStyle ?? TextStyles.h18w500.copyWith(color: textColor),
        style: style ?? ButtonStyles.blockButton,
      ),
    );
  }
}

class AppBackButton extends StatelessWidget {
  /// Creates an [IconButton] with the appropriate "back" icon for the current
  /// target platform.
  const AppBackButton({Key? key, this.color, this.onPressed, this.iconData = Icons.keyboard_arrow_left_sharp}) : super(key: key);

  /// The color to use for the icon.
  ///
  /// Defaults to the [IconThemeData.color] specified in the ambient [IconTheme],
  /// which usually matches the ambient [Theme]'s [ThemeData.iconTheme].
  final Color? color;

  final IconData? iconData;

  /// An override callback to perform instead of the default behavior which is
  /// to pop the [Navigator].
  ///
  /// It can, for instance, be used to pop the platform's navigation stack
  /// via [SystemNavigator] instead of Flutter's [Navigator] in add-to-app
  /// situations.
  ///
  /// Defaults to null.
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    assert(debugCheckHasMaterialLocalizations(context));
    return IconButton(
      color: color,
      tooltip: MaterialLocalizations.of(context).backButtonTooltip,
      onPressed: () {
        if (onPressed != null) {
          onPressed!();
        } else {
          Navigator.maybePop(context);
        }
      },
      icon: const Icon(AppIcons.back),
    );
  }
}
