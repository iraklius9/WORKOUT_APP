# Workout Plan API

A RESTful API for a Personalized Workout Plan system that allows users to create and manage customized workout plans and track their fitness goals.

## Features

### Core Features
1. **User Authentication**
   - Secure user registration, login, and logout
   - JWT-based authentication
   - Profile management

2. **Exercise Database**
   - 20+ predefined exercises
   - Detailed descriptions and instructions
   - Various exercise types and difficulty levels

3. **Workout Plans**
   - Create personalized workout plans
   - Customize sets, reps, and duration
   - Schedule workouts

4. **Progress Tracking**
   - Track weight and measurements
   - Set and monitor fitness goals
   - Exercise-specific achievements

5. **API Documentation**
   - Swagger UI for testing endpoints
   - Detailed endpoint documentation

### Bonus Features
6. **Real-time Workout Mode**
   - Guided workout sessions
   - Exercise completion tracking
   - Rest period timers

7. **Docker Support**
   - Easy deployment with Docker
   - PostgreSQL database integration

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Database**: PostgreSQL (Docker) / SQLite (Development)
- **Authentication**: JWT (JSON Web Tokens)
- **Documentation**: Swagger/OpenAPI
- **Deployment**: Docker & Docker Compose

## Project Structure
```
WORKOUT_APP/
├── exercises/           # Exercise database and management
├── progress/           # Progress tracking functionality
├── security/          # Authentication and security features
├── users/             # User profile management
├── workout_plans/     # Workout plan creation and management
├── workouts/          # Active workout session handling
├── templates/         # HTML templates
└── WORKOUT_APP/       # Main project settings
```

## Enhanced Security Features
- Two-Factor Authentication (2FA)
- Rate limiting protection
- Strong password validation
- Phone number validation for 2FA

## Setup Instructions

### Local Development

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd WORKOUT_APP
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the root directory:
   ```
   DEBUG=1
   SECRET_KEY=your-secret-key-here
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py seed_exercises  # Populate exercise database
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Docker Deployment

1. **Build and Run**
   ```bash
   docker-compose up --build
   ```

2. **Initialize Database**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py seed_exercises
   docker-compose exec web python manage.py createsuperuser
   ```

## API Documentation

### Authentication Endpoints

#### Register New User
```http
POST /api/users/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password",
    "password2": "secure_password"
}

Response (201 Created):
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
}
```

#### Login
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password"
}

Response (200 OK):
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Exercise Endpoints

#### List Exercises
```http
GET /api/exercises/
Authorization: Bearer <your_token>

Response (200 OK):
{
    "count": 20,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Push-ups",
            "description": "A classic bodyweight exercise...",
            "instructions": "1. Start in plank position...",
            "target_muscles": "Chest, Shoulders, Triceps",
            "difficulty_level": "beginner",
            "exercise_type": "strength"
        },
        ...
    ]
}
```

### Workout Plan Endpoints

#### Create Workout Plan
```http
POST /api/workout-plans/plans/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "title": "Full Body Workout",
    "description": "3-day full body workout plan",
    "frequency": 3,
    "duration": 60,
    "difficulty": "intermediate"
}

Response (201 Created):
{
    "id": 1,
    "title": "Full Body Workout",
    "description": "3-day full body workout plan",
    "frequency": 3,
    "duration": 60,
    "difficulty": "intermediate",
    "created_at": "2025-02-02T12:00:00Z",
    "sessions": []
}
```

#### Add Workout Session
```http
POST /api/workout-plans/plans/1/add_session/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "name": "Day 1 - Upper Body",
    "day_of_week": 1,
    "notes": "Focus on form"
}

Response (201 Created):
{
    "id": 1,
    "name": "Day 1 - Upper Body",
    "day_of_week": 1,
    "notes": "Focus on form",
    "exercises": []
}
```

#### Add Exercise to Session
```http
POST /api/workout-plans/sessions/1/add_exercise/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "exercise": 1,
    "order": 1,
    "sets": 3,
    "reps": 12,
    "rest_period": 60
}

Response (201 Created):
{
    "id": 1,
    "exercise": 1,
    "exercise_detail": {
        "name": "Push-ups",
        "description": "A classic bodyweight exercise..."
    },
    "order": 1,
    "sets": 3,
    "reps": 12,
    "rest_period": 60
}
```

### Progress Tracking Endpoints

#### Log Progress
```http
POST /api/progress/tracking/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "date": "2025-02-02",
    "weight": 75.5,
    "notes": "Feeling stronger",
    "workout_duration": 45,
    "mood": "great"
}

Response (201 Created):
{
    "id": 1,
    "date": "2025-02-02",
    "weight": 75.5,
    "notes": "Feeling stronger",
    "workout_duration": 45,
    "mood": "great",
    "created_at": "2025-02-02T12:00:00Z"
}
```

#### Create Goal
```http
POST /api/progress/goals/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "title": "Weight Loss Goal",
    "description": "Lose 5kg in 2 months",
    "target_date": "2025-04-02",
    "goal_type": "weight",
    "target_value": 70.0
}

Response (201 Created):
{
    "id": 1,
    "title": "Weight Loss Goal",
    "description": "Lose 5kg in 2 months",
    "target_date": "2025-04-02",
    "goal_type": "weight",
    "target_value": 70.0,
    "is_completed": false
}
```

### Real-time Workout Endpoints

#### Start Workout
```http
POST /api/workout-plans/active/start_workout/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "session": 1
}

Response (201 Created):
{
    "id": 1,
    "session_detail": {
        "name": "Day 1 - Upper Body",
        "exercises": [...]
    },
    "started_at": "2025-02-02T12:00:00Z",
    "status": "in_progress"
}
```

#### Complete Exercise
```http
POST /api/workout-plans/active/1/complete_exercise/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "workout_exercise_id": 1,
    "completed_sets": 3,
    "completed_reps": 12,
    "weight_used": 50
}

Response (200 OK):
{
    "id": 1,
    "exercise_name": "Push-ups",
    "completed_sets": 3,
    "completed_reps": 12,
    "weight_used": 50,
    "completed_at": "2025-02-02T12:15:00Z"
}
```

## WebSocket Connection

For real-time workout updates, connect to:
```
ws://localhost:8000/ws/workout/<workout_id>/
```

Example messages:
```json
// Exercise completion
{
    "type": "exercise_complete",
    "exercise_id": 1,
    "completed_sets": 3,
    "completed_reps": 12
}

// Server response
{
    "type": "workout_update",
    "message": {
        "exercise_id": 1,
        "completed_sets": 3,
        "completed_reps": 12
    }
}
```

## Additional Features to Consider

1. **Social Features**:
   - Friend system
   - Share workout plans
   - Community challenges
   - Social feed of workouts
   - Comments and likes on workouts

2. **Advanced Analytics**:
   - Visual progress charts
   - Body measurements tracking
   - Workout performance analytics
   - Personal records tracking
   - AI-powered workout recommendations

3. **Nutrition Integration**:
   - Meal planning
   - Calorie tracking
   - Macro tracking
   - Recipe database
   - Integration with nutrition APIs

4. **Gamification**:
   - Achievement system
   - Workout streaks
   - Points and levels
   - Badges for milestones
   - Monthly challenges

5. **Mobile Features**:
   - Mobile app (React Native/Flutter)
   - Offline mode
   - Push notifications
   - Exercise form videos
   - Voice commands

6. **Health Integration**:
   - Connect with fitness wearables
   - Heart rate monitoring
   - Sleep tracking
   - Step counting
   - Integration with Apple Health/Google Fit

7. **AI and Machine Learning**:
   - Personalized workout recommendations
   - Form checking using computer vision
   - Progress prediction
   - Workout difficulty adjustment
   - Smart rest period suggestions

8. **Enhanced Security**:
   - Two-factor authentication
   - OAuth social login
   - Rate limiting
   - Advanced password policies
   - Session management

9. **Premium Features**:
   - Subscription system
   - Premium workout plans
   - Personal trainer access
   - Advanced analytics
   - Priority support

10. **Content Management**:
    - Blog system
    - Exercise tutorials
    - Nutrition articles
    - Success stories
    - Expert advice section

## Security Notes

- All endpoints require JWT authentication except registration and login
- Tokens expire after 24 hours
- Refresh tokens are valid for 7 days
- Use HTTPS in production
- Keep your SECRET_KEY secure
- Update dependencies regularly
