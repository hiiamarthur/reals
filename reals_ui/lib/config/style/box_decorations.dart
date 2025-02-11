import 'package:flutter/material.dart';
import 'index.dart';

class BoxDecorations {
  static BoxDecoration card = const BoxDecoration(
    color: AppColors.appGrey,
    borderRadius: BorderRadius.all(Radius.circular(12)),
  );

  static BoxDecoration outlinedTag = BoxDecoration(
    border: Border.all(color: AppColors.appRed.withOpacity(.2), width: 1.0),
    borderRadius: const BorderRadius.all(Radius.circular(3)),
  );

  static BoxDecoration infoTag = const BoxDecoration(
    color: AppColors.appGrey,
    borderRadius: BorderRadius.all(Radius.circular(5)),
  );

}
