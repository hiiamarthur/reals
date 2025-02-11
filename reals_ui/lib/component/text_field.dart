import 'package:flutter/material.dart';

class CustomTextField extends StatelessWidget {
  final String hintText;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final ValueChanged<String>? onChanged;
  final TextEditingController? controller;
  final TextStyle? textStyle;
  final bool isPassword;
  final OutlineInputBorder? borderStyle;
  final Color? backgroundColor;

  const CustomTextField({
    Key? key,
    this.hintText = '',
    this.prefixIcon,
    this.suffixIcon,
    this.onChanged,
    this.controller,
    this.textStyle,
    this.borderStyle,
    this.backgroundColor,
    this.isPassword = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: backgroundColor ?? Colors.white,
        borderRadius: borderStyle?.borderRadius ?? BorderRadius.circular(8.0),
      ),
      child: TextField(
        controller: controller,
        style: textStyle ?? TextStyle(fontSize: 16.0),
        obscureText: isPassword ?? false,
        decoration: InputDecoration(
          prefixIcon: prefixIcon,
          suffixIcon: !isPassword ? suffixIcon : Image.asset("assets/images/eye.png"),
          hintText: hintText,
          hintStyle: textStyle?.copyWith(color: Colors.grey) ?? TextStyle(color: Colors.grey),
          border: borderStyle ??
              OutlineInputBorder(
                borderRadius: BorderRadius.circular(8.0),
                borderSide: BorderSide(color: Colors.grey),
              ),
          enabledBorder: borderStyle ??
              OutlineInputBorder(
                borderRadius: BorderRadius.circular(8.0),
                borderSide: BorderSide(color: Colors.grey),
              ),
          focusedBorder: borderStyle ??
              OutlineInputBorder(
                borderRadius: BorderRadius.circular(8.0),
                borderSide: BorderSide(color: Colors.blue),
              ),
        ),
        onChanged: onChanged,
      ),
    );
  }
}
