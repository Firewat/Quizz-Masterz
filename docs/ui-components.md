---
title: UI Components
nav_order: 99
---

# QuizMasterz UI Components

The QuizMasterz application features a student and teacher-friendly interface with various UI components designed for both Users. Here's an overview:

## Key Interfaces

### Student Interface

![Student Dashboard](assets/images/Student_Dashboard.png)

### Authentication Screens

![Login Screen](assets/images/Login.png)

![Sign Up Form](assets/images/Sign_Up.png)

## Student Features

### Classroom Management
![Join Classroom](assets/images/join_Classroom_student.PNG)
![My Classrooms](assets/images/my_classrooms_student.PNG)

### Quiz Taking Interface

![Available Quizzes](assets/images/quiz_in_classroom_student.PNG)
![Take Quiz](assets/images/quiz_taking_student.PNG)

### Student Profile & Shop
![Student Profile](assets/images/student_profile.PNG)
![Student Shop](assets/images/shop_student.PNG)

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