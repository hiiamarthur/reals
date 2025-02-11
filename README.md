# Reals Server

A modern FastAPI-based server application for managing GPT conversations with SQLAlchemy and PostgreSQL.

## Features

- 🚀 FastAPI for high-performance async API
- 🔐 User authentication and session management
- 🤖 GPT integration with conversation tracking
- 📊 API usage monitoring and logging
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 🔄 Async database operations
- 📝 Comprehensive API documentation (Swagger/OpenAPI)

## Environment Setup

The application supports multiple environments:

- Development (Local)
- Test (Render.com)
- Production

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd reals-server
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Local development
cp .env.example .env

# Test environment
cp .env.test.example .env.test
```

### Database Configuration

#### Local Development
```bash
# Start PostgreSQL service
# Create local database
createdb reals
```

#### Test Environment (Render.com)
1. Create a PostgreSQL database on Render.com
2. Update `.env.test` with Render.com credentials

### Running Migrations

```bash
# Initialize migrations (first time only)
alembic init alembic

# Create new migration
alembic revision --autogenerate -m "migration message"

# Apply migrations
alembic upgrade head
```

### Running the Application

```bash
# Development
uvicorn app.main:app --reload

# Test
ENV=test uvicorn app.main:app
```

## API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
reals-server/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   └── services/
├── alembic/
├── tests/
├── .env
├── .env.test
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Your chosen license]

## Contact

[Your contact information]

# Reals UI

A modern Flutter application serving as the frontend for the Reals project, featuring GPT conversation capabilities and a clean, responsive UI.

## Features

- 🎯 Flutter-powered cross-platform application
- 💬 Real-time GPT chat interface
- 🔐 User authentication and session management
- 🎨 Modern and responsive UI design
- 🌓 Dark/Light theme support
- 💾 Local session persistence
- 🔄 Automatic state management
- 📱 Cross-platform support (iOS, Android, Web)

## Getting Started

### Prerequisites

- Flutter SDK (latest stable version)
- Dart SDK
- Android Studio / VS Code with Flutter extensions
- iOS development tools (for iOS development)
- Git

### Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd reals_ui
```

2. Install dependencies:
```bash
flutter pub get
```

3. Set up environment configuration:
```bash
# Copy example environment file
cp .env.example .env
```

### Environment Configuration

Configure the following environment variables:
```env
API_BASE_URL=http://localhost:8000  # Development
# API_BASE_URL=https://your-api.render.com  # Test
```

### Project Structure
```
reals_ui/
├── lib/
│   ├── api/              # API service layer
│   ├── models/           # Data models
│   ├── screens/          # UI screens
│   │   ├── auth/        # Authentication screens
│   │   ├── chat/        # Chat interface
│   │   └── settings/    # App settings
│   ├── widgets/         # Reusable widgets
│   ├── utils/           # Utility functions
│   ├── providers/       # State management
│   └── themes/          # App themes
├── assets/              # Images, fonts, etc.
├── test/               # Unit and widget tests
└── pubspec.yaml        # Project configuration
```

### Running the Application

#### Development
```bash
# Run with development configuration
flutter run -t lib/main_development.dart

# Run with specific device
flutter run -d [device-id] -t lib/main_development.dart
```

#### Test Environment
```bash
# Run with test configuration
flutter run -t lib/main_test.dart
```

### Building for Production

#### Android
```bash
flutter build apk --release
# or
flutter build appbundle --release
```

#### iOS
```bash
flutter build ios --release
```

#### Web
```bash
flutter build web --release
```

## Features and Screens

### Authentication
- Login
- Registration
- Password Reset
- Profile Management

### Chat Interface
- Real-time GPT conversations
- Message history
- Conversation management
- File attachments (if applicable)

### Settings
- Theme customization
- Language preferences
- Notification settings
- Profile management

## State Management

This project uses [state management solution] for handling application state. Key features include:
- Session management
- Chat state
- User preferences
- API integration

## Testing

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/widget_test.dart
```

## Development Guidelines

### Code Style
- Follow official Flutter style guide
- Use meaningful variable and function names
- Comment complex logic
- Keep files focused and manageable

### Git Workflow
1. Create feature branch from development
2. Implement changes
3. Write/update tests
4. Create pull request
5. Code review
6. Merge to development

## Troubleshooting

Common issues and solutions:
1. Build errors
   - Run `flutter clean`
   - Delete build folder
   - Run `flutter pub get`

2. API connection issues
   - Verify API_BASE_URL in .env
   - Check backend server status
   - Verify network connectivity

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Your chosen license]

## Contact

[Your contact information]
```

This README provides:
1. Project overview and features
2. Setup instructions
3. Environment configuration
4. Project structure
5. Running and building instructions
6. Feature descriptions
7. Development guidelines
8. Testing instructions
9. Troubleshooting guide