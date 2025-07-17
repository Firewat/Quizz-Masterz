---
title: UI Components
nav_order: 99
---

# QuizMasterz UI Components

The QuizMasterz application features a student and teacher-friendly interface with various UI components designed for both Users. Here's an overview:

## Key Interfaces

### Student Interface

![Student Dashboard](Quizz-Masterz/docs/assets/images/Student_Dashboard.png)

### Authentication Screens

![Login Screen](Quizz-Masterz/docs/assets/images/Login.png)

![Sign Up Form](Quizz-Masterz/docs/assets/images/Sign_Up.png)

## Student Features

### Classroom Management
![Join Classroom](Quizz-Masterz/docs/assets/images/join_Classroom_student.PNG)
![My Classrooms](Quizz-Masterz/docs/assets/images/my_classrooms_student.PNG)

### Quiz Taking Interface

![Available Quizzes](Quizz-Masterz/docs/assets/images/quiz_in_classroom_student.PNG)
![Take Quiz](Quizz-Masterz/docs/assets/images/quiz_taking_student.PNG)

### Student Profile & Shop
![Student Profile](Quizz-Masterz/docs/assets/images/student_profile.PNG)
![Student Shop](Quizz-Masterz/docs/assets/images/shop_student.PNG)

## System Architecture

### UML Diagrams

```mermaid
graph TD;
    Student-->Authentication;
    Student-->Classrooms;
    Student-->Quizzes;
    Student-->Shop;
    Teacher-->QuizManagement;
    Teacher-->ClassroomManagement;
    ClassroomManagement-->StudentManagement;
```

For a complete understanding of our system architecture, refer to our detailed UML diagrams:

![Simplified UML](assets/images/FullStack_Quizz_Masterz_UML_Use_Case_Diagramm_simplified.jpg)

{: .download }
> For more detailed technical documentation, check our [architecture documentation](technical-docs/architecture.md) section.