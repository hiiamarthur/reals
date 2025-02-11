import 'dart:math';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:reals_ui/config/style/index.dart';
import 'package:reals_ui/controllers/prompt_controller.dart';
import 'package:reals_ui/data/prompt.dart';
import 'package:reals_ui/helper/helper_management.dart';
import 'package:reals_ui/widgets/app_button.dart';
import 'package:reals_ui/widgets/app_spacer.dart';

class QuestionsPage extends StatefulWidget {
  @override
  _QuestionsPageState createState() => _QuestionsPageState();
}

class _QuestionsPageState extends State<QuestionsPage> {
  int _currentStage = 0; // Current Questions stage (0 to 7)
  final PromptController _controller = Get.find();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        // appBar: AppBar(
        //   title: Text('Questions Bar - 8 Stages'),
        //   centerTitle: true,
        // ),
        body: GetBuilder<PromptController>(
            init: _controller,
            builder: (_) {
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Flex(
                      direction: Axis.horizontal,
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Container(
                          // decoration: BoxDecoration(
                          //   border: Border.all(color: Colors.red),
                          // ),
                          child: // Adjust the value as needed
                              IconButton(
                            icon: Icon(Icons.arrow_back_rounded),
                            padding: EdgeInsets.fromLTRB(0, 0, 0, 0),
                            alignment: Alignment.centerLeft,
                            onPressed: () {
                              Get.back();
                              // Your onPressed action here
                            },
                          ),
                          // child: AppButton.icon(Icons.arrow_back_rounded,
                          //   onPressed: () => Get.back()),
                        ),
                        Text(
                          "$_currentStage" + "/8 completed",
                          style: TextStyle(fontFamily: 'Quicksand'),
                        ),
                      ],
                    ),
                    // Questions bar
                    // Row(
                    //   children: List.generate(8, (index) {
                    //     return Expanded(
                    //       child: Container(
                    //         margin: EdgeInsets.symmetric(horizontal: 2),
                    //         height: 10,
                    //         color: _currentStage >= index ? Colors.blue : Colors.grey[300],
                    //       ),
                    //     );
                    //   }),
                    // ),
                    SizedBox(height: 20),
                    LinearProgressIndicator(
                      minHeight: 8,
                      color: AppColors.appGrey,
                      backgroundColor: AppColors.bgGrey,
                      value: _currentStage.toDouble() / 8,
                      semanticsLabel: 'Linear progress indicator',
                    ),
                    SizedBox(height: 20),

                    // Questions stages
                    Expanded(
                        child: ListView(children: [
                      // Loop through each stage and display a question only if it's the current stage
                      ...List.generate(8, (index) {
                        if (_currentStage != index)
                          return const SizedBox.shrink();

                        return Column(
                          children: [
                            // Text(
                            //   'Question for Stage ${index + 1}',
                            //   style: TextStyle(
                            //       fontSize: 18, fontWeight: FontWeight.bold),
                            // ),
                            const SizedBox(height: 10),
                            _buildQuestion(index, _),
                            const SizedBox(height: 20),
                          ],
                        );
                      }),
                    ])),
                    SizedBox(height: 20),

                    // Navigation buttons
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Padding(
                              padding: EdgeInsets.all(4.0),
                              child: AppButton.outlined(
                                title: "Decided for Me",

                                onPressed: _currentStage > 0
                                    ? () {
                                        setState(() {
                                          _currentStage--;
                                        });
                                      }
                                    : null,
                                // child: Text('Previous'),
                              )),
                        ),
                        Expanded(
                          child: Padding(
                              padding: EdgeInsets.all(4.0),
                              child: AppButton.main(
                                "Next Question",
                                onPressed: _currentStage < 7
                                    ? () {
                                        setState(() {
                                          _currentStage++;
                                        });
                                      }
                                    : null,
                                // child: Text('Next'),
                              )),
                        )
                      ],
                    ),
                  ],
                ),
              );
            }));
  }

  Widget _buildQuestion(int index, PromptController _) {
    final localization = MaterialLocalizations.of(context);
    switch (index) {
      case 0:
        return Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Text(
              'When are you planning the date for?',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontFamily: 'Quicksand',
              ),
            ),
            const SizedBox(height: 20),
            AppSpacer.h20(),
            GestureDetector(
              onTap: () async {
                _.dateDay.value = await pickDate(context);
              },
              child: Card(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10.0),
                ),
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Obx(() {
                    return Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              _.dateDay != null
                                  ? "${_.dateDay.value.month} / ${_.dateDay.value.year}"
                                  : "Select Date",
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const Icon(Icons.calendar_today),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          "${_.dateDay!.value.day} ${_.dateDay!.value.month} ${_.dateDay!.value.year}",
                          style: const TextStyle(
                            fontSize: 16,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    );
                  }),
                ),
              ),
            )
          ],
        );
      case 1:
        return Column(
          children: [
            Text(
              "What time of date would you prefer for the date?",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontFamily: 'Quicksand',
              ),
            ),
            AppSpacer.h20(),
            Row(
              children: [
                Text("Start:"),
                Expanded(
                    child: GestureDetector(
                        onTap: () async {
                          _.dateTimeStart.value = await pickTime(context);
                        },
                        child: Card(
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(40.0),
                          ),
                          elevation: 4,
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Obx(() {
                              return Column(
                                children: [
                                  const SizedBox(height: 8),
                                  Text(
                                    localization.formatTimeOfDay(
                                        _.dateTimeStart.value,
                                        alwaysUse24HourFormat: false),
                                    style: const TextStyle(
                                      fontSize: 16,
                                      color: Colors.grey,
                                    ),
                                  ),
                                ],
                              );
                            }),
                          ),
                        )))
              ],
            ),
            Row(
              children: [
                Text("End:"),
                Expanded(
                    child: GestureDetector(
                        onTap: () async {
                          _.dateTimeStart.value = await pickTime(context);
                        },
                        child: Card(
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(40.0),
                          ),
                          elevation: 4,
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Obx(() {
                              return Column(
                                children: [
                                  const SizedBox(height: 8),
                                  Text(
                                    localization.formatTimeOfDay(
                                        _.dateTimeStart.value,
                                        alwaysUse24HourFormat: false),
                                    style: const TextStyle(
                                      fontSize: 16,
                                      color: Colors.grey,
                                    ),
                                  ),
                                ],
                              );
                            }),
                          ),
                        )))
              ],
            )
          ],
        );
        break;
      case 2:
        return Column(
          children: [
            Text(
              "What kind of date would you like to plan?",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontFamily: 'Quicksand',
              ),
            ),
            SizedBox(height: 20),
            _buildGrid(DateType.allTypes, _),
          ],
        );
      case 3:
        return Column(
          children: [
            Text(
              "Do you have preferred cuisine?",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontFamily: 'Quicksand',
              ),
            ),
            SizedBox(height: 60),
            // Expanded(
            //     child:
            SizedBox(
                width: double.infinity,
                child: GestureDetector(onTap: () async {
                  _controller.isHavingCuisine.value = true;
                }, child: Obx(() {
                  return Card(
                    color: _controller.isHavingCuisine.value
                        ? Colors.red
                        : Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(40.0),
                    ),
                    elevation: 4,
                    child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          children: [
                            const SizedBox(height: 8),
                            Text(
                              "Yes",
                              style: const TextStyle(
                                fontSize: 16,
                                color: Colors.grey,
                              ),
                            ),
                          ],
                        )),
                  );
                }))),
            SizedBox(
                width: double.infinity,
                child: GestureDetector(onTap: () async {
                  _controller.isHavingCuisine.value = false;
                }, child: Obx(() {
                  return Card(
                    color: !_controller.isHavingCuisine.value
                        ? Colors.red
                        : Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(40.0),
                    ),
                    elevation: 4,
                    child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          children: [
                            const SizedBox(height: 8),
                            Text(
                              "No",
                              style: const TextStyle(
                                fontSize: 16,
                                color: Colors.grey,
                              ),
                            ),
                          ],
                        )),
                  );
                })))
            // )
            ,
          ],
        );
      case 4:
        return Column(
          children: [
            Text(
              "How would you like to get around?",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontFamily: 'Quicksand',
              ),
            ),
            SizedBox(height: 60),
            // Expanded(
            //     child:
            SizedBox(
                width: double.infinity,
                child: GestureDetector(onTap: () async {
                  _controller.isHavingCuisine.value = true;
                }, child: Obx(() {
                  return Card(
                    color: _controller.isHavingCuisine.value
                        ? Colors.red
                        : Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(40.0),
                    ),
                    elevation: 4,
                    child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          children: [
                            const SizedBox(height: 8),
                            Text(
                              "Public Transportation",
                              style: const TextStyle(
                                fontSize: 16,
                                color: Colors.grey,
                              ),
                            ),
                          ],
                        )),
                  );
                }))),
            SizedBox(
                width: double.infinity,
                child: GestureDetector(onTap: () async {
                  _controller.isHavingCuisine.value = false;
                }, child: Obx(() {
                  return Card(
                    color: !_controller.isHavingCuisine.value
                        ? Colors.red
                        : Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(40.0),
                    ),
                    elevation: 4,
                    child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          children: [
                            const SizedBox(height: 8),
                            Text(
                              "Driving",
                              style: const TextStyle(
                                fontSize: 16,
                                color: Colors.grey,
                              ),
                            ),
                          ],
                        )),
                  );
                })))
            // )
            ,
          ],
        );
      case 5:
        return Column(children: [
          Text(
            "What is your budget for the date? (HKD per person)",
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              fontFamily: 'Quicksand',
            ),
          ),
          SizedBox(height: 60),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [Text("0%"), Text("100%")],
          ),
          Obx(() {
            return Slider(
                value: _controller.budget.value,
                onChanged: (value) {
                  _controller.budget.value = value;
                });
          })
        ]);
        break;
      case 6:
        return Column(children: [
          Text(
            "How intense would you like the date to be?",
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              fontFamily: 'Quicksand',
            ),
          ),
          SizedBox(height: 60),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [Text("Chill"), Text("Intense")],
          ),
          Obx(() {
            return Slider(
                value: _controller.intensityLevel.value,
                onChanged: (value) {
                  _controller.intensityLevel.value = value;
                });
          })
        ]);
        break;
      case 7:
        return Column(
          children: [
            Text(
              "Do you have a preferred location for the date?",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontFamily: 'Quicksand',
              ),
            ),
            Text("(you can choose more than one)"),
            SizedBox(height: 60),
            ...LocationType.allTypes.map((location) {
              return SizedBox(
                  width: double.infinity,
                  child: GestureDetector(onTap: () async {
                    _controller.locations.contains(location)
                        ? _controller.locations.remove(location)
                        : _controller.locations.add(location);
                  }, child: Obx(() {
                    return Card(
                      color: _controller.locations.contains(location)
                          ? Colors.red
                          : Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(40.0),
                      ),
                      elevation: 4,
                      child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            children: [
                              const SizedBox(height: 8),
                              Text(
                                location,
                                style: const TextStyle(
                                  fontSize: 16,
                                  color: Colors.grey,
                                ),
                              ),
                            ],
                          )),
                    );
                  })));
            })
          ],
        );

        break;
      default:
        return Container();
        break;
    }
    // if (index % 2 == 0) {
    //   // Yes/No question
    //   return Column(
    //     children: [
    //       Text('Do you like Flutter?'),
    //       const SizedBox(height: 10),
    //       Row(
    //         mainAxisAlignment: MainAxisAlignment.center,
    //         children: [
    //           ElevatedButton(
    //             onPressed: () {
    //               // Handle Yes answer
    //             },
    //             child: const Text('Yes'),
    //           ),
    //           const SizedBox(width: 10),
    //           ElevatedButton(
    //             onPressed: () {
    //               // Handle No answer
    //             },
    //             child: const Text('No'),
    //           ),
    //         ],
    //       ),
    //     ],
    //   );
    // } else {
    //   // Multiple choice question
    //   return Column(
    //     children: [
    //       Text('What is your favorite Flutter widget?'),
    //       const SizedBox(height: 10),
    //       Column(
    //         children: [
    //           RadioListTile<int>(
    //             value: 1,
    //             groupValue: index,
    //             onChanged: (value) {
    //               // Handle choice selection
    //             },
    //             title: const Text('Container'),
    //           ),
    //           RadioListTile<int>(
    //             value: 2,
    //             groupValue: index,
    //             onChanged: (value) {
    //               // Handle choice selection
    //             },
    //             title: const Text('Row'),
    //           ),
    //           RadioListTile<int>(
    //             value: 3,
    //             groupValue: index,
    //             onChanged: (value) {
    //               // Handle choice selection
    //             },
    //             title: const Text('Column'),
    //           ),
    //           RadioListTile<int>(
    //             value: 4,
    //             groupValue: index,
    //             onChanged: (value) {
    //               // Handle choice selection
    //             },
    //             title: const Text('ListView'),
    //           ),
    //         ],
    //       ),
    //     ],
    //   );
    // }
  }

  Widget _buildGrid(List<String> items, PromptController _) {
    // Split the list into pairs
    List<String> tempItems = List.from(items);
    List<List<String>> pairs = [];
    int i = 0;
    while (tempItems.isNotEmpty) {
      int endingIndex = 0;
      if (i % 2 == 1) {
        endingIndex = min(tempItems.length, 2);
      } else {
        endingIndex = min(tempItems.length, 3);
      }
      debugPrint("tempItems ${tempItems}");
      pairs.add(tempItems.sublist(0, endingIndex));
      tempItems.removeRange(0, endingIndex);
      i += 1;
    }

    return Column(
      mainAxisAlignment: MainAxisAlignment.start,
      children: pairs.map((pair) {
        return Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: pair.map((category) {
            return Expanded(
              child: Padding(
                padding: const EdgeInsets.all(2.0),
                child: Obx(() {
                  return ChoiceChip(
                    label: Text(category),
                    labelStyle: TextStyle(
                      color: _.dateType.contains(category)
                          ? Colors.black
                          : Colors.white,
                      fontSize: 16,
                    ),
                    selected: _.dateType.contains(category),
                    selectedColor: Colors.white,
                    backgroundColor: Colors.redAccent,
                    onSelected: (bool isSelected) {
                      debugPrint("_.dateType.value ${_.dateType.value}");
                      if (!isSelected) {
                        _.dateType.remove(category);
                      } else {
                        _.dateType.add(category);
                      }
                    },
                    shape: RoundedRectangleBorder(
                      side: BorderSide.none,
                      borderRadius: BorderRadius.circular(30.0),
                    ),
                  );
                }),
              ),
            );
            ;
          }).toList(),
        );
      }).toList(),
    );
    ;
  }
}
