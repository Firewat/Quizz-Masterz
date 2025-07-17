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
- Password hashing using Werkzeug security
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
- Automated scoring and LP distribution

### Classroom Management
- Unique join codes for classroom access
- Student roster management
- Quiz assignment and tracking
- Classroom-specific leaderboards
- Student performance analytics

### Shop System
- LP-based virtual currency
- Cosmetic item purchasing
- Avatar selection and management
- Inventory tracking

## Security Features

### Access Control
- Route protection using Flask-Login decorators
- Role verification for sensitive operations
- Cross-site request forgery (CSRF) protection
- Session security measures

### Data Protection
- Password hashing with salt
- SQL injection prevention through SQLAlchemy
- Input validation and sanitization
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
- Normalized database design with foreign key relationships
- Efficient indexing on frequently queried fields
- Cascade delete behavior for dependent records
- Transaction integrity for critical operations

### Frontend Architecture
- Bootstrap-based responsive design
- Dynamic form handling with Flask-WTF
- AJAX for real-time updates
- Client-side validation

## Performance Considerations

### Database Optimization
- Lazy loading for related records
- Efficient query patterns
- Appropriate indexing
- Connection pooling

### Caching Strategy
- Session caching for user data
- Query result caching
- Static asset caching

### Scalability
- Modular codebase design
- Separation of concerns
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
- Database error recovery
- Transaction rollbacks

## Future Considerations

### Planned Enhancements
- Advanced analytics dashboard
- Additional question types
- Enhanced shop features
- Performance optimization

### Scalability Plans
- Database sharding capability
- Caching improvements
- API endpoint development
- Load balancing preparation