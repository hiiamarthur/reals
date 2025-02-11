import 'package:google_sign_in/google_sign_in.dart';

final GoogleSignIn googleSignIn = GoogleSignIn(
  scopes: ['email'],
);

Future<void> handleGoogleSignIn() async {
  try {
    final account = await googleSignIn.signIn();
    if (account != null) {
      final authentication = await account.authentication;
      final idToken = authentication.idToken;
      
      // Send idToken to your FastAPI server for validation
    }
  } catch (error) {
    print(error);
  }
}