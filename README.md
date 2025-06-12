# Quiz Masterz

Flask-based web application for creating, managing, and taking educational quizzes. Quiz Masters provides a platform for teachers to create and manage classrooms, create quizzes, and for students to join classrooms and take quizzes with multiple answer support and partial credit scoring.

## Features

### For Teachers
- **Classroom Management & Creation**: Create and manage multiple classrooms.
- **Quiz Creation**: Build quizzes with multiple-choice questions supporting multiple correct answers.
- **Student Monitoring**: View student performance and quiz results.
- **Set Learning Points**: Set multiple correct answers with flexible scoring for Students to earn Learning Points (LP).

### For Students
- **Classroom Participation**: Join classrooms using unique classroom codes.
- **Quiz Taking**: Take quizzes with multiple answer selection capability.
- **Performance Tracking**: View quiz results with detailed scoring breakdown and earn LPs for your right answers.
- **Shop**: Level up and earn Skins for your Profile.

### System Features
- **Multiple Answer Support**: Students can select multiple answers per question.
- **Partial Credit Scoring**: Scoring system with partial credit for partially correct answers and penalties for incorrect selections.
- **User Authentication**: Secure login and registration system with role-based access (Teacher/Student).

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip

### Installation

1.  **Clone the repository**
    ```bash
    git clone (https://github.com/Firewat/Quizz-Masterz)
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the database**
    The application uses Flask-Migrate for database migrations.
    ```bash
    # flask db init  (only if never done before)
    # flask db migrate -m "init"
    flask db upgrade
    ```

4.  **Run the application**
    ```bash
    python main.py
    ```
    

5.  **Access the application**
    Open your browser and navigate to `http://127.0.0.1:5000`

## Project Structure
```
Full_Stack_Quizz_Masterz/
├── main.py                      # Application entry point (Furkan)
├── requirements.txt             # Python dependencies (All)
├── README.md                   # Project documentation (All)
├── .gitignore                  # Git ignore configuration (All)
├── instance/                   # Flask instance folder
│   └── database.db            # SQLite database file
├── migrations/                 # Database migration files 
├── website/                    # Main application package
│   ├── __init__.py            # Flask app factory (Furkan)
│   ├── models.py              # Database models (Lasse )
│   ├── views.py               # Main routes and views (Lasse )
│   ├── auth.py                # Authentication routes (Lasse)
│   ├── forms.py               # WTForms form definitions (Lasse)
│   ├── components.py          # UI component helpers (David)
│   ├── static/                # Static assets (CSS, JS, images)
│   └── templates/             # Jinja2 HTML templates (David
│       ├── base.html          # Base template with navigation
│       ├── home.html          # Role-based home page
│       ├── login.html         # User login form
│       ├── sign_up.html       # User registration form
│       ├── test_quiz.html     # Student test quiz interface
│       ├── test_quiz_results.html # Test quiz results display
│       ├── teacher_classrooms.html # Teacher classroom management
│       ├── teacher_quizzes.html    # Teacher quiz management
│       ├── student_quizzes.html    # Student quiz dashboard
│       ├── take_quiz.html          # Quiz taking interface
│       ├── quiz_results.html       # Quiz results page
│       ├── manage_questions.html   # Question management
│       ├── manage_answers.html     # Answer management
│       ├── edit_classroom.html     # Classroom editing
│       ├── edit_quiz.html          # Quiz editing
│       ├── edit_question.html      # Question editing
│       ├── add_quiz_to_classroom.html # Quiz assignment to classroom
│       ├── join_quiz.html          # Quiz joining interface
│       ├── profile.html            # User profile page
│       ├── quiz_history.html       # Quiz history view
│       ├── review_submissions.html # Submission review
└── __pycache__/               # Python bytecode cache
```

## 🏗️ Architecture Overview

### Backend Architecture (Lasses Responsibility)

#### Core Components
- **Flask Application** (`__init__.py`)
  - Creates and configures Flask app
  - Initializes database and login manager
  - Registers blueprints

- **Database Models** (`models.py`)
  - `User`: User accounts with role-based access (student/teacher)
  - `Classroom`: Teacher-managde classrooms
  - `Quiz`: Quiz definitions with questions
  - `Question`: Individual quiz questions
  - `Answer`: Multiple Answer choices for questions
  - `QuizSubmission`: Student quiz attempts
  - `UserAnswer`: Individual question responses

- **Authentication System** (`auth.py`)
  - User registration and login
  - Password hashing 
  - Session management with Flask-Login
  - Role-based access control

- **Forms** (`forms.py`)
  - WTForms-based form validation
  - `LoginForm`: User authentication
  - `SignUpForm`: User registration
  - Additional forms for quiz/classroom management

- **Views and Routes** (`views.py`)
  - Main application routes
  - Quiz management endpoints
  - Classroom administration
  - Test quiz functionality
  - Student and teacher dashboards

#### Database Schema
```sql
-- Users table with role-based access
User(id, email, password, first_name, role)

-- Classroom management
Classroom(id, name, code, teacher_id)

-- Quiz structure
Quiz(id, title, description, teacher_id)
Question(id, text, quiz_id)
Answer(id, text, is_correct, question_id)

-- Student submissions
QuizSubmission(id, user_id, quiz_id, score, submitted_at)
UserAnswer(id, submission_id, question_id, selected_answers)
```

### Frontend Architecture (David's Responsibility)

#### Template Structure
- **Base Template** (`base.html`)
  - Common HTML structure
  - Navigation bar with role-based links
  - Bootstrap integration

- **Authentication Templates**
  - `login.html`: Simple login form
  - `sign_up.html`: User registration
  - Role-based welcome pages

- **Student Interface**
  - `home.html`: Student dashboard with test quiz access
  - `test_quiz.html`: 3-question Python code quiz
  - `test_quiz_results.html`: Quiz results with scoring
  - `student_quizzes.html`: Available quizzes
  - `take_quiz.html`: Quiz-taking interface

- **Teacher Interface**
  - `teacher_classrooms.html`: Classroom management
  - `teacher_quizzes.html`: Quiz administration
  - Management forms for questions, answers, and classrooms

- **UI Components** (`components.py`)
  - Form helpers and macros
  - Template utility functions
 
### DevOps and Configuration (Furkans Responsibility)

#### Application Configuration
- **Entry Point** (`main.py`)
  - Flask development server configuration
  - Environment-specific settings
  - Database initialization

- **Dependencies** (`requirements.txt`)
  ```
  Flask==2.3.3
  Flask-SQLAlchemy==3.0.5
  Flask-Login==0.6.3
  Flask-WTF==1.1.1
  WTForms==3.0.1
  Werkzeug==2.3.7
  ```

- **Git Configuration** (`.gitignore`)
  - Python cache files
  - Virtual environment exclusions
  - Database and instance files
  - IDE-specific files

#### Deployment Considerations
- **Database**: SQLite for development, PostgreSQL recommended for production
- **Environment Variables**: Secret key, database URL configuration
- **Static Assets**: Served by Flask in development, CDN in production
- **Session Management**: Secure session configuration required

## Test Quiz Feature

### Implementation Details
The test quiz feature provides a quick assessment tool for students and a Test for us:

- **Question Set**: 3 Python code questions sourced from the application codebase
- **Format**: Multiple choice with single correct answers
- **Scoring**: Simple pass/fail with percentage calculation
- **Session Management**: Quiz state maintained in Flask sessions

### Quiz Questions
1. **Flask Routes**: Identifying correct route decorator syntax
2. **Database Models**: Understanding SQLAlchemy relationship definitions
3. **Template Syntax**: Recognizing proper Jinja2 template syntax

### Completed Features 
- Basic authentication system with role-based access
- Simple login and registration forms
- Test quiz functionality with 3 Python questions
- Role-based home pages (student/teacher views)
- Team responsibility assignments
- Project structure documentation

### In Development 
- Advanced quiz management features
- Classroom creation and management
- Comprehensive student/teacher interfaces
- Enhanced UI styling and responsiveness

### Planned 
- Full quiz creation and management system
- Student performance analytics
- Advanced question types
- Shop for Students
- Notes Creation
