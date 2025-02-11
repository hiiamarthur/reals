import 'package:flutter/material.dart';
import 'package:reals_ui/component/search_field.dart';
import 'package:reals_ui/config/style/index.dart';
import 'package:reals_ui/data/main.dart';
import 'package:reals_ui/widgets/app_button.dart';
import 'package:reals_ui/widgets/app_scaffold.dart';
import 'package:reals_ui/widgets/app_spacer.dart';

class MainPage extends StatefulWidget {
  const MainPage({Key? key}) : super(key: key);

  @override
  createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
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
            child: MainPageBody(),
          ),
        ));
  }
}

class MainPageBody extends StatefulWidget {
  const MainPageBody({Key? key}) : super(key: key);
  @override
  createState() => _MainPageBodyState();
}

class _MainPageBodyState extends State<MainPageBody> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // SearchField(),
        Row(
          children: [
            Expanded(child: SearchField()),
            AppSpacer.w10(),
            // Image.asset("assets/images/sort.png")
            AppButton.outlined(
                title: "sort",
                child: Row(
                  children: [
                    Text("sort"),
                    Image.asset("assets/images/sort.png")
                  ],
                ))
          ],
        ),
        AppSpacer.h10(),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: mainData.mainDataMap.sublist(0, 4).map((map) {
            return Flexible(
                flex: 1,
                child: Container(
                    width: 200,
                    child: Column(
                      children: [
                        Image.asset(map["asset"]!),
                        Text(
                          map["name"]!,
                          style: TextStyle(
                            // fontSize: 20,
                            fontWeight: FontWeight.bold,
                            fontFamily: 'Quicksand',
                          ),
                        )
                      ],
                      // ),
                    )));
          }).toList(),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: mainData.mainDataMap.sublist(4, 8).map((map) {
            return Flexible(
                flex: 1,
                child: Container(
                    width: 200,
                    child: Column(
                      children: [
                        Image.asset(map["asset"]!),
                        Text(
                          map["name"]!,
                          style: TextStyle(
                            // fontSize: 20,
                            fontWeight: FontWeight.bold,
                            fontFamily: 'Quicksand',
                          ),
                        )
                      ],
                      // ),
                    )));
          }).toList(),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              "Featured Reals",
              style: TextStyle(
                fontSize: 20,
                // fontWeight: FontWeight.bold,
                fontFamily: 'Roboto',
              ),
            ),
            AppButton.outlined(title: "View All"),
          ],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [realsBlock(), realsBlock()],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              "Trend Reals",
              style: TextStyle(
                fontSize: 20,
                // fontWeight: FontWeight.bold,
                fontFamily: 'Roboto',
              ),
            ),
            AppButton.outlined(title: "View All"),
          ],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [realsBlock(), realsBlock()],
        ),
        // Flexible(
        //   flex: 1,
        //   child: ListView(
        //     shrinkWrap: true,
        //   children: mainData.testlist.map((map) {
        //     return Container(
        //       // alignment: Alignment.center,
        //       // decoration: BoxDecoration(
        //       //     color: Colors.blueAccent,
        //       //     borderRadius: BorderRadius.circular(8.0),
        //       //     border: Border.all(color: Colors.red)),
        //       child:
        //       // Column(
        //       //   children: [
        //           // Image.asset(mainDataMap[index]["asset"]!),
        //           Text(
        //             "test",
        //             // mainDataMap[index]["name"]!,
        //             // style: TextStyle(color: Colors.black, fontSize: 16.0),
        //           )
        //         // ],
        //       // ),
        //     );
        //   }).toList(),
        // ))
        //   Expanded(
        //     child:
        //     GridView.count(
        //       crossAxisCount: 2,
        //       crossAxisSpacing: 10,
        //   mainAxisSpacing: 10,
        //   shrinkWrap: true,
        //       // gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        //       //   crossAxisCount: 2, // 2 columns
        //       //   crossAxisSpacing: 8.0, // Space between columns
        //       //   mainAxisSpacing: 8.0, // Space between rows
        //       //   childAspectRatio: 1.5, // Aspect ratio (width/height)
        //       // ),
        //       // itemCount: 8, // Total items: 2x4 grid = 8 items
        //       children: [
        //         Text("test"),
        //         Text("test"),
        //         Text("test"),
        //         Text("test"),
        //       //   ...mainDataMap.map((map) {
        //       //   return Container(
        //       //     alignment: Alignment.center,
        //       //     decoration: BoxDecoration(
        //       //       color: Colors.blueAccent,
        //       //       borderRadius: BorderRadius.circular(8.0),
        //       //       border: Border.all(color: Colors.red)
        //       //     ),
        //       //     child: Column(
        //       //       children: [
        //       //         // Image.asset(mainDataMap[index]["asset"]!),
        //       //         Text(
        //       //           "test",
        //       //           // mainDataMap[index]["name"]!,
        //       //           style: TextStyle(color: Colors.black, fontSize: 16.0),
        //       //         )
        //       //       ],
        //       //     ),
        //       //   );
        //       // }).toList()
        // ]),

        //   )
      ],
    );
  }
}

Widget realsBlock() {
  return Column(
    children: [
      Image.asset("assets/images/feature reals 1.png"),
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            // crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                "Match 60%",
                style: TextStyle(
                  fontSize: 9,
                  fontFamily: 'Roboto',
                ),
              ),
              Text(
                "Pottery",
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'Roboto',
                ),
              ),
            ],
          ),
          AppSpacer.w20(),
          AppButton.outlined(title: "Book")
        ],
      )
    ],
  );
}
