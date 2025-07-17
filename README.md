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

- **Shop**: Level up and earn Skins for your Profile.



### System Features

- **Multiple Answer Support**: Students can select multiple answers per question.

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
