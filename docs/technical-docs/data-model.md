---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .no_toc }
# Data Model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Database Schema

 **UML Use Case Diagrams**

![UML Use Case Diagram - Simplified](../assets/images/FullStack_Quizz_Masterz_UML_Use_Case_Diagramm_simplified.jpg)
*Simplified UML Use Case Diagram showing the main system interactions.*

![UML Use Case Diagram - Complete](../assets/images/FullStack_Quizz_Mastzerz_Complete_UML_Use_Case_Diagram.jpg)
*Complete UML Use Case Diagram with detailed system architecture and relationships.*

- [UML Use Case Diagram - Simplified](../assets/pdfs/FullStack_Quizz_Masterz_UML_Use_Case_Diagramm_simplified.pdf)
- [UML Use Case Diagram - Complete](../assets/pdfs/FullStack_Quizz_Mastzerz_Complete_UML_Use_Case_Diagram.pdf)

...
### User
```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(50))  # 'teacher' or 'student'
    learning_points = db.Column(db.Integer, default=0)
    selected_avatar = db.Column(db.String(100), default=None)
    unlocked_avatars = db.Column(db.Text, default='')
```

Relationships:
- `classrooms_created`: One-to-many with Classroom (teacher's classrooms)
- `joined_classrooms`: Many-to-many with Classroom (student's joined classrooms)
- `quiz_attempts`: One-to-many with StudentQuizAttempt

### Classroom
```python
class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    join_code = db.Column(db.String(8), unique=True, nullable=False)
```

Relationships:
- `teacher`: Many-to-one with User
- `students`: Many-to-many with User
- `quizzes`: Many-to-many with Quiz
- `quiz_attempts`: One-to-many with StudentQuizAttempt

### Quiz
```python
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
```

Relationships:
- `teacher`: Many-to-one with User
- `questions`: One-to-many with Question
- `classrooms_assigned_to`: Many-to-many with Classroom

### Question
```python
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    learning_points = db.Column(db.Integer, nullable=False, default=1)
```

Relationships:
- `quiz`: Many-to-one with Quiz
- `answers`: One-to-many with Answer

### Answer
```python
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
```

Relationships:
- `question`: Many-to-one with Question

### StudentQuizAttempt
```python
class StudentQuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
```

Relationships:
- `student`: Many-to-one with User
- `quiz`: Many-to-one with Quiz
- `classroom`: Many-to-one with Classroom

## Association Tables

### classroom_members
Many-to-many relationship between students and classrooms:
```python
classroom_members = db.Table('classroom_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True)
)
```

### classroom_quizzes
Many-to-many relationship between classrooms and quizzes:
```python
classroom_quizzes = db.Table('classroom_quizzes',
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True),
    db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
)
```
...

## Quiz Flow

1. Teachers create quizzes with multiple-choice questions in their classrooms
2. Each question can have multiple correct answers and earns learning points (LP)
3. Students join classrooms using unique join codes
4. Students take quizzes and earn LP based on correct answers
5. LP can be used to purchase items from the shop
6. Teachers can review quiz results and student performance

## Student Progress

1. Students accumulate LP by completing quizzes correctly
2. LP can be spent in the shop for cosmetic items
3. Students can track their progress in each classroom's leaderboard
4. Quiz attempts are recorded to prevent retaking the same quiz

## Authentication & User Management

![Login Screen](../assets/images/Login%20Screen.PNG)
*User login interface with email and password authentication.*

![Sign Up Form](../assets/images/Sign%20up%20form.PNG)
*Registration form for new users to create accounts.*

![Student Logged In Successfully](../assets/images/Student%20logged%20in%20successfully.PNG)
*Confirmation screen after successful user authentication.*

![Student Profile Student](../assets/images/Student%20Profile%20Student.PNG)
*Student profile displaying learning points, level, and personal statistics.*

## Classroom Management

![My Classrooms Student](../assets/images/My%20classrooms%20Student.PNG)
*Overview of all classrooms a student has joined.*

![Join Classroom Student](../assets/images/join%20classroom%20student.PNG)
*Interface for students to join classrooms using unique codes.*

![Classroom Student](../assets/images/Classroom%20Student.PNG)
*Individual classroom view showing assigned quizzes and class information.*

## Quiz System

![Available Quizzes Student](../assets/images/Available%20Quizzes%20Student.PNG)
*List of quizzes available for students to take in their classrooms.*

![Take Quiz Student](../assets/images/Take%20Quiz%20Student.PNG)
*Quiz interface where students answer questions and earn learning points.*

## Gamification Features

![Student Shop student](../assets/images/Student%20Shop%20student.PNG)
*Shop system where students can purchase cosmetic skins using earned points.*

## System Architecture

![Dashboard WF](../assets/images/Dashboard%20WF.PNG)
*Overall dashboard wireframe showing the complete application structure.*
