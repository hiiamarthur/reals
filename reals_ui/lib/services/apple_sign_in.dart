import 'package:sign_in_with_apple/sign_in_with_apple.dart';

Future<void> handleAppleSignIn() async {
  try {
    final credential = await SignInWithApple.getAppleIDCredential(
      scopes: [
        AppleIDAuthorizationScopes.email,
        AppleIDAuthorizationScopes.fullName,
      ],
    );

    final idToken = credential.identityToken;
    // Send idToken to your FastAPI server for validation
  } catch (error) {
    print(error);
  }
}
