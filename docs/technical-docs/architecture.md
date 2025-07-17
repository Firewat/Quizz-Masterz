---
title: Architecture
parent: Technical Docs
nav_order: 1
layout: default
---

{: .no_toc }
# Architecture

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview 

For Teachers:
Classroom Management & Creation: Create and manage multiple classrooms.
Quiz Creation: Build quizzes with multiple-choice questions supporting multiple correct answers.
Student Monitoring: View student performance and quiz results.
Set Learning Points: Set multiple correct answers with flexible scoring for Students to earn Learning Points (LP).

For Students:
Classroom Participation: Join classrooms using unique classroom codes.
Quiz Taking: Take quizzes with multiple answer selection capability.
(TODO) Performance Tracking: View quiz results with detailed scoring breakdown and earn LPs for your right answers.
(TODO) Shop: Level up and earn Skins for your Profile.

System Features:
Multiple Answer Support: Students can select multiple answers per question.
Partial Credit Scoring: Scoring system with partial credit for partially correct answers and penalties for incorrect selections.
User Authentication: Secure login and registration system with role-based access (Teacher/Student).

## Codemap

- **Entry Point:**
  - `main.py` starts the application and initializes the web server.

- **Website Package:**
  - `auth.py`: Handles user authentication, registration, and session management.
  - `models.py`: Defines database models for users, classrooms, quizzes, questions, and answers.
  - `views.py`: Contains the main route handlers for both teacher and student features.
  - `forms.py`: Manages form validation and processing for user input.
  - `static/` and `templates/`: Contain static assets (CSS) and HTML templates for rendering the UI.

- **Database:**
  - `instance/database.db` stores all persistent data (users, classrooms, quizzes, results).

**Main Flow:**
1. Users register and log in (role: Teacher or Student).
2. Teachers create/manage classrooms and quizzes.
3. Students join classrooms and take quizzes.
4. Results and progress are tracked and displayed.

For a visual overview, refer to the [UML use case diagram](../assets/images/FullStack_Quizz_Masterz_UML_Use_Case_Diagramm_simplified.jpg).

## Cross-cutting concerns

Three cross-cutting concerns in Quizz-Masterz are:

**1. Authentication & Authorization:**
All users must register and log in to access the system. The application enforces role-based access control, ensuring that Teachers and Students can only access features appropriate to their roles. Sensitive actions (like quiz creation or classroom management) are protected so only authorized users can perform them.

**2. Data Validation:**
Every user input—such as registration details, quiz answers, and classroom codes—is validated both on the client and server sides. This prevents invalid or malicious data from entering the system and ensures data integrity throughout the application.

**3. Error Handling:**
The application provides clear, user-friendly error messages for common issues (e.g., failed login, invalid classroom code). 