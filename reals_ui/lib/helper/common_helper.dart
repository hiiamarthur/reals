
import 'package:flutter/material.dart';
import 'package:reals_ui/config/style/index.dart';

 Future<DateTime> pickDate(BuildContext context) async {
    DateTime? selectedDate = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(20),
      lastDate: DateTime(2100),
      confirmText: "OK",
      cancelText: "Cancel",
      builder: (context, child) => Theme(
        data: ThemeData.light().copyWith(
          datePickerTheme: AppTheme.lightTheme.datePickerTheme
        ),
        child: child!,
      ),
      // builder:(BuildContext context,Widget? child){
      //   return Date
      // }
    );

    return selectedDate!;
  }
  
Future<TimeOfDay> pickTime(BuildContext context) async {
    TimeOfDay? selectedTime = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
      confirmText: "OK",
      cancelText: "Cancel",
      builder: (context, child) => Theme(
        data: ThemeData.light().copyWith(
          timePickerTheme: AppTheme.lightTheme.timePickerTheme
        ),
        child: child!,
      ),
    );

    return selectedTime!;
  }
