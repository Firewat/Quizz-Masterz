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

## System Overview

Quiz Masterz is built using a Flask-based architecture with SQLAlchemy ORM for database management. The system is designed around role-based access control (RBAC) with two primary user types: Teachers and Students.

## Core Components

### Authentication System
- User registration and login using Flask-Login
- Role-based access control for teachers and students
- Session management and secure routing

### Database Layer
- SQLite database with SQLAlchemy ORM
- Relational models for Users, Classrooms, Quizzes, Questions, and Answers
- Association tables for many-to-many relationships
- Transaction management for quiz submissions and shop purchases

### Quiz Management System
- Draft and published quiz states
- Multiple-choice questions with multiple correct answers
- Learning Points (LP) scoring system
- Quiz attempt tracking to prevent retakes
- Automated grading, scoring and LP distribution

### Classroom Management
- Join codes for classroom access
- Student management
- Quiz assignment
- Classroom-specific leaderboards
- Student performance analytics

### Shop System
- LP-based "virtual currency"
- Avatar purchasing
- Avatar selection

## Security Features

### Access Control
- Route protection using Flask-Login
- Role verification
- Session security measures

### Data Protection
- Password hashing with salt
- SQL injection prevention through SQLAlchemy
- Secure quiz submission handling

## Technical Implementation

### Route Structure
```
/auth/
  ├─ /login
  ├─ /logout
  └─ /sign-up

/teacher/
  ├─ /classrooms
  ├─ /create_classroom
  ├─ /edit_classroom/<id>
  ├─ /quiz/<id>/manage_questions
  ├─ /quiz/<id>/review/<classroom_id>
  └─ /quiz/<id>/upload_to_classroom/<classroom_id>

/student/
  ├─ /join_classroom
  ├─ /my_classrooms
  ├─ /classroom/<id>
  ├─ /quizzes
  └─ /take-quiz/<quiz_id>/<classroom_id>

/shop/
  ├─ /
  ├─ /buy/<item_id>
  └─ /select-avatar/<avatar_icon>
```

### Database Architecture
- Normalized database design with foreign and primary key relationships
- Efficient indexing on frequently queried fields
- Cascade delete behavior for entries
- Transaction integrity for critical operations

### Frontend Architecture
- Bootstrap-based responsive design
- Dynamic form handling with Flask-WTF
- Client-side validation

## Performance Considerations

### Database Optimization
- Lazy loading for related entries
- Query patterns
- Indexing

### Caching Strategy
- Session caching for user data
- Query result caching
- Static asset caching

### Scalability
- Modular codebase design
- Extensible data models
- Maintainable route structure

## Error Handling

### User Feedback
- Flash messages for user actions
- Clear error messages
- Success confirmations
- Input validation feedback

### System Errors
- Graceful error handling
- 404 and 500 error pages
- Database error

## Future Considerations

### Planned Enhancements
- Advanced analytics and Administrator dashboard
- Performance optimization

### Scalability Plans
- API endpoint development
- Quiz History implementation