import 'package:flutter/material.dart';
import 'package:reals_ui/config/style/index.dart';
import 'package:reals_ui/widgets/app_button.dart';
import 'package:reals_ui/widgets/app_scaffold.dart';

class BeginPage extends StatefulWidget {
  const BeginPage({Key? key}) : super(key: key);

  @override
  createState() => _BeginPageState();
}

class _BeginPageState extends State<BeginPage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return AppScaffold(
        backgroundColor: AppColors.appWhite,
        body: SingleChildScrollView(
          child: DefaultTextStyle.merge(
            style: TextStyles.h14w500.copyWith(color: AppColors.appBlack),
            child: BeginPageBody(),
          ),
        ));
  }
}

class BeginPageBody extends StatefulWidget {
  const BeginPageBody({Key? key}) : super(key: key);
  @override
  createState() => _BeginPageBodyState();
}

class _BeginPageBodyState extends State<BeginPageBody> {
@override
  Widget build(BuildContext context) {
    return Column(
      children: [
        AppButton(child: Text("test"))
      ],
    );
  }
}