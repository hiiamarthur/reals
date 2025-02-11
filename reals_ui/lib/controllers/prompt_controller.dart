import 'package:get/get.dart';
import 'package:flutter/material.dart';



class PromptController extends GetxController {
  var dateDay = DateTime.now().obs;

  // Start time of the date (could be DateTime or just a time string in HH:mm format)
  var dateTimeStart = TimeOfDay.now().obs; // or DateTime

  // End time of the date (could be DateTime or just a time string in HH:mm format)
  var dateTimeEnd = TimeOfDay.now().obs; // or DateTime

  // Type of the date (using the DateType class created earlier)
  var dateType = <String>[].obs; // Expecting values like "outdoor", "indoor", etc.

  // Boolean to check if cuisine is involved
  var isHavingCuisine = false.obs;

  // Type of cuisine (using the CuisineType class created earlier)
  var cuisineType = ''.obs; // Expecting values like "chinese", "japanese", etc.

  // Transport type (could be a string or an enum if you have predefined transport modes)
  var transportType = ''.obs; // Example: "car", "public transport", "bike", etc.

  // Budget for the date (could be a string or a numeric range)
  var budget = 0.0.obs; // Example: budget in numbers

  // Intensity level of the date (could be low, medium, high)
  var intensityLevel = 0.0.obs; // Example: "low", "medium", "high"

  // Location for the date (could be a text input or coordinates)
  var locations = <String>[].obs; // Example: city or specific location
  
  @override
  void onInit() async {
    super.onInit();
    debugPrint('is init');
  }

  @override
  void onReady() async {
    super.onReady();
    debugPrint('onReady');
  }

 

  
}
