---
title: Contributions
parent: Team Evaluation
nav_order: 4
---

{: .no_toc }
# Summary of individual contributions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Lasse Schulz

Backend Architecture 

Core Components

    Flask Application (__init__.py)

        Creates and configures Flask app

        Initializes database and login manager

        Registers blueprints

    Database Models (models.py)

        User: User accounts with role-based access (student/teacher)

        Classroom: Teacher-managde classrooms

        Quiz: Quiz definitions with questions

        Question: Individual quiz questions

        Answer: Multiple Answer choices for questions

        QuizSubmission: Student quiz attempts

        UserAnswer: Individual question responses

    Authentication System (auth.py)

        User registration and login

        Password hashing

        Session management with Flask-Login

        Role-based access control

    Forms (forms.py)

        WTForms-based form validation

        LoginForm: User authentication

        SignUpForm: User registration

        Additional forms for quiz/classroom management

    Views and Routes (views.py)

        Main application routes

        Quiz management endpoints

        Classroom administration

        Test quiz functionality

        Student and teacher dashboards

## Furkan Dinc

DevOps and Configuration 

Application Configuration

    Entry Point (main.py)

        Flask development server configuration

        Environment-specific settings

        Database initialization

    Dependencies (requirements.txt)

        Flask==2.3.3

        Flask-SQLAlchemy==3.0.5

        Flask-Login==0.6.3

        Flask-WTF==1.1.1

        WTForms==3.0.1

        Werkzeug==2.3.7

    Git Configuration (.gitignore)

        Python cache files

        Virtual environment exclusions

        Database and instance files

        IDE-specific files

Deployment Considerations

    Database: SQLite for development, PostgreSQL recommended for production

    Environment Variables: Secret key, database URL configuration

    Static Assets: Served by Flask in development, CDN in production

    Session Management: Secure session configuration required

## David Levi

Frontend Architecture

Template Structure

    Base Template (base.html)

        Common HTML structure

        Navigation bar with role-based links

        Bootstrap integration

    Authentication Templates

        login.html: Simple login form

        sign_up.html: User registration

        Role-based welcome pages

    Student Interface

        home.html: Student dashboard with test quiz access

        test_quiz.html: 3-question Python code quiz

        test_quiz_results.html: Quiz results with scoring

        student_quizzes.html: Available quizzes

        take_quiz.html: Quiz-taking interface

    Teacher Interface

        teacher_classrooms.html: Classroom management

        teacher_quizzes.html: Quiz administration

        Management forms for questions, answers, and classrooms

    UI Components (components.py)

        Form helpers and macros

        Template utility functions
