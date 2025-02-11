import 'package:flutter/material.dart';

class AppSpacer extends StatelessWidget {
  final double w, h;

  const AppSpacer({Key? key, this.w = 0, this.h = 0}) : super(key: key);

  factory AppSpacer.w5() => AppSpacer(w: 5);
  factory AppSpacer.w7() => AppSpacer(w: 7);
  factory AppSpacer.w10() => AppSpacer(w: 10);
  factory AppSpacer.w15() => AppSpacer(w: 15);
  factory AppSpacer.w20() => AppSpacer(w: 20);
  factory AppSpacer.w26() => AppSpacer(w: 26);
  factory AppSpacer.w30() => AppSpacer(w: 30);
  factory AppSpacer.w40() => AppSpacer(w: 40);



  factory AppSpacer.h5() => AppSpacer(h: 5);
  factory AppSpacer.h10() => AppSpacer(h: 10);
  factory AppSpacer.h15() => AppSpacer(h: 15);
  factory AppSpacer.h18() => AppSpacer(h: 18);
  factory AppSpacer.h20() => AppSpacer(h: 20);
  factory AppSpacer.h24() => AppSpacer(h: 24);
  factory AppSpacer.h30() => AppSpacer(h: 30);
  factory AppSpacer.h35() => AppSpacer(h: 35);
  factory AppSpacer.h40() => AppSpacer(h: 40);
  factory AppSpacer.h50() => AppSpacer(h: 40);
  factory AppSpacer.h48() => AppSpacer(h: 48);
  factory AppSpacer.h60() => AppSpacer(h: 60);
  factory AppSpacer.h78() => AppSpacer(h: 78);
  factory AppSpacer.h100() => AppSpacer(h: 100);
  factory AppSpacer.h120() => AppSpacer(h: 120);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: w,
      height: h,
    );
  }
}
