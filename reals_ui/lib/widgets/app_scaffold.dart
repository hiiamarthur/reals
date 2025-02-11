import 'package:flutter/material.dart';
//import 'package:flutter_libserialport/flutter_libserialport.dart';
import 'package:get/get.dart';
import 'package:reals_ui/config/style/index.dart';
import 'package:reals_ui/config/style/paddings.dart';

// import 'package:loader_overlay/loader_overlay.dart';

class AppScaffold extends StatelessWidget {
  final PreferredSizeWidget? appBar;
  final Widget? body, bottomNavigationBar;
  final bool? top, bottom, resizeToAvoidBottomInset;
  final EdgeInsets? padding;
  final Color? backgroundColor;

  const AppScaffold({
    Key? key,
    this.appBar,
    this.backgroundColor,
    this.body,
    this.bottomNavigationBar,
    this.top,
    this.bottom,
    this.resizeToAvoidBottomInset,
    this.padding,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawerEdgeDragWidth: 0,
      backgroundColor: backgroundColor,
      // resizeToAvoidBottomInset: true,
      // appBar: appBar,
      body: PopScope(
        child: _Body(
          body: body ?? Container(),
          // bottomNavigationBar: bottomNavigationBar,
          // bottomNavigationBar: AppButton.main(
          //   "Back",
          //   onPressed: () => Navigator.pop(context),
          // ),
          padding: padding ?? EdgeInsets.zero,
          // messageController: Get.find(),
        ),
      ),
      appBar: AppBar(
        backgroundColor: AppColors.appWhite,
        title: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Image.asset("assets/images/Icon face 3.png"),
                Image.asset("assets/images/Icon face.png"),
              ],
            ),
            Text("REALS"),
            Image.asset("assets/images/Icon shopping cart.png")
          ],
        ),
      ),
      bottomNavigationBar: BottomAppBar(
          shape: CircularNotchedRectangle(),
          notchMargin: 6.0,
          child:
              Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
            // Left group of navigation items
            // Row(
            //   children: [
            Flexible(
              flex: 1,
              child: GestureDetector(
                  onTap: () {
                    Get.toNamed("/explore");
                  },
                  child: Container(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.home, color: Colors.black),
                        Text('Explore', style: TextStyle(fontSize: 12)),
                      ],
                    ),
                  )),
            ),
            Flexible(
              flex: 1,
              child: GestureDetector(
                onTap: () {
                  Get.toNamed("/wish");
                },
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.favorite_border, color: Colors.black),
                    Text('Wishlist', style: TextStyle(fontSize: 12)),
                  ],
                ),
              ),
            ),
            //   ],
            // ),

            // Expanded(
            //   child:
            Flexible(
              flex: 1,
              // decoration: BoxDecoration(
              //   border: Border.all(color: Colors.red),
              // ),
              // padding: EdgeInsets.zero,
              // Set the desired width
              child: MaterialButton(
                  shape: CircleBorder(
                    side: BorderSide(
                      color: Colors.red, // Border color
                      width: 2, // Border width
                    ),
                  ),
                  padding: EdgeInsets.all(0),
                  onPressed: () {
                    Get.toNamed("/question");
                  },
                  child: Image.asset(
                      'assets/images/addRed.png') // path to your image asset
                  // size: 40, // size of the icon
                  // color: Colors.blue, // optional color, if you need to tint it
                  ),
            ),
            // ),
            //  ),
            // Right group of navigation items
            // Row(
            //   children: [
            Flexible(
              flex: 1,
              child: GestureDetector(
                onTap: () {
                  Get.toNamed("/schedule");
                },
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.search, color: Colors.black),
                    Text('Schedule', style: TextStyle(fontSize: 12)),
                  ],
                ),
              ),
            ),
            Flexible(
              flex: 1,
              child: GestureDetector(
                onTap: () {
                  Get.toNamed("/setting");
                },
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.settings, color: Colors.black),
                    Text('Setting', style: TextStyle(fontSize: 12)),
                  ],
                ),
              ),
            ),
            //   ],
            // ),
          ])),
    );
  }
}

class _Body extends StatelessWidget {
  final Widget? body, bottomNavigationBar;
  final EdgeInsets? padding;

  //

  const _Body({
    this.body,
    this.padding, this.bottomNavigationBar,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("App scagfold build");
    // MessageController _messageController = Get.find();

    return Padding(
      padding: padding ?? Paddings.w20,
      child: Column(children: <Widget>[
        Padding(
          padding: Paddings.w15,
          child: Expanded(
            child: body ?? const SizedBox.shrink(),
          ),
        ),
        bottomNavigationBar ?? const SizedBox.shrink(),
      ]),
      // children: [

      // ],
    );
  }
}
