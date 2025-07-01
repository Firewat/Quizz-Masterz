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



3.  **Run the application**

    ```bash

    python main.py

    ```





4.  **Access the application**

    Open your browser and navigate to `http://127.0.0.1:5000` or localhost website



## Project Structure

```

Quizz-Masterz/

├── main.py                      # Application entry point (Furkan)

├── requirements.txt             # Python dependencies (All)

├── README.md                   # Project documentation (All)

├── .gitignore                  # Git ignore configuration (All)

├── add_test_students.py        # Script to add test students to database

├── database_diagram.dbml       # Database diagram definition

├── venv/                       # Virtual environment folder

├── instance/                   # Flask instance folder

│   └── database.db            # SQLite database file

├── docs/                       # Project documentation

│   ├── _config.yml            # Documentation configuration

│   ├── index.md               # Documentation index

│   ├── README.md              # Documentation README

│   ├── design-decisions.md    # Design decision documentation

│   ├── ui-components.md       # UI components documentation

│   ├── user-eval.md           # User evaluation documentation

│   ├── value-proposition.md   # Value proposition documentation

│   ├── assets/                # Documentation assets

│   │   ├── images/            # Documentation images

│   │   └── pdfs/              # Documentation PDFs

│   ├── design-decisions/      # Design decision details

│   ├── team-eval/             # Team evaluation documentation

│   └── technical-docs/        # Technical documentation

├── website/                    # Main application package

│   ├── __init__.py            # Flask app factory (Furkan)

│   ├── models.py              # Database models (Lasse)

│   ├── views.py               # Main routes and views (Lasse)

│   ├── auth.py                # Authentication routes (Lasse)

│   ├── forms.py               # WTForms form definitions (Lasse)

│   ├── static/                # Static assets (CSS, JS, images)

│   │   └── css/

│   │       └── style.css      # Main stylesheet

│   ├── templates/             # Jinja2 HTML templates (David)

│   │   ├── base.html          # Base template with navigation

│   │   ├── home.html          # Role-based home page

│   │   ├── login.html         # User login form

│   │   ├── sign_up.html       # User registration form

│   │   ├── profile.html       # User profile page

│   │   ├── shop.html          # Student shop interface

│   │   ├── create_classroom.html # Teacher classroom creation

│   │   ├── edit_classroom.html # Classroom editing

│   │   ├── teacher_classrooms.html # Teacher classroom management

│   │   ├── teacher_create_quiz.html # Quiz creation interface

│   │   ├── teacher_manage_questions.html # Question management

│   │   ├── teacher_manage_answers.html # Answer management

│   │   ├── student_join_classroom.html # Student classroom joining

│   │   ├── student_my_classrooms.html # Student classroom dashboard

│   │   ├── student_quizzes.html # Student quiz dashboard

│   │   ├── student_view_classroom_details.html # Classroom details view

│   │   ├── take_quiz.html     # Quiz taking interface

│   │   └── quiz_review_details.html # Quiz review interface

│   └── __pycache__/           # Python bytecode cache

└── .git/                      # Git repository metadata

```




## Architecture Overview


## Architecture Overview



### Backend Architecture



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




### Frontend Architecture



#### Template Structure

- **Base Template** (`base.html`)

  - Common HTML structure

  - Navigation bar with role-based links

  - Bootstrap integration



- **Authentication Templates**

  - `login.html`: Simple login form

  - `sign_up.html`: User registration

  - Role-based home pages



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
  flask
  Flask-SQLAlchemy
  flask-login
  Flask-Migrate
  Flask-WTF
  WTForms
  email-validator
  ```



- **Git Configuration** (`.gitignore`)

  ```
  .vscode
  __pycache__
  instance/database.db
  /myenv/
  ```



## Completed Features 

**Authentication & User Management:**
- User registration and login system with role-based access (Student/Teacher)
- User profiles with learning points and level progression system
- Secure password hashing and session management

**Teacher Features:**
- Classroom creation and management with unique join codes
- Quiz creation with multiple-choice questions and answers
- Student management and quiz result monitoring
- Quiz publishing workflow (draft → published)

**Student Features:**
- Classroom joining using unique join codes
- Quiz taking with multiple answer selection
- Automatic scoring with learning points reward system
- Level progression based on accumulated learning points

**Core System Features:**
- Learning points system with exponential level progression
- Quiz scoring with partial credit support
- Role-based navigation and access control
- Quiz attempt prevention for completed quizzes



## In Development 

- Advanced quiz management features
- Shop
- Quiz History for Students

## Planned Features

- Student performance analytics
- Advanced question types
- Shop for Students
- Notes Creation


### AI Disclaimer

This Readme was partially created with the help of AI
