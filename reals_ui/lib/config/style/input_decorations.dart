import 'package:flutter/material.dart';
import 'index.dart';

class InputDecorations {
  static double outlineRadius = 5.0;

  // outline input decoration
  static OutlineInputBorder outline = const OutlineInputBorder(
    borderRadius: BorderRadius.all(
      Radius.circular(Dimens.borderRadius),
    ),
    borderSide: BorderSide(width: 1.0, color: AppColors.inputBorder),
  );
  // outline input decoration

}
