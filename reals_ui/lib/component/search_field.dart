import 'package:flutter/material.dart';

class SearchField extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return TextField(
      decoration: InputDecoration(
        prefixIcon: Icon(Icons.search), // Search Icon
        hintText: 'Search...', // Placeholder text
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0), // Rounded corners
          borderSide: BorderSide(color: Colors.grey), // Border style
        ),
      ),
      onChanged: (value) {
        // Handle search input
        print('Search: $value');
      },
    );
  }
}
