---
title: UI Components
nav_order: 99
---

# QuizMasterz UI Components

The QuizMasterz application features a modern, user-friendly interface with various UI components designed for both students and teachers. Here's an overview of our main UI components and their usage.

## Key Interfaces

### Student Interface

```markdown
![Student Dashboard](assets/images/Dashboard WF.PNG)
```

![Student Dashboard](assets/images/Dashboard WF.PNG)

### Authentication Screens

```markdown
![Login Screen](assets/images/Login Screen.PNG)
```

![Login Screen](assets/images/Login Screen.PNG)

```markdown
![Sign Up Form](assets/images/Sign up form.PNG)
```

![Sign Up Form](assets/images/Sign up form.PNG)

## Student Features

### Classroom Management
{: .info }
> Students can join classrooms and view their enrolled classes through an intuitive interface.

![Join Classroom](assets/images/join classroom student.PNG)
![My Classrooms](assets/images/My classrooms Student.PNG)

### Quiz Taking Interface
{: .tip }
> Students can access available quizzes and take them in an interactive environment.

![Available Quizzes](assets/images/Available Quizzes Student.PNG)
![Take Quiz](assets/images/Take Quiz Student.PNG)

### Student Profile & Shop
{: .attention }
> Students can manage their profile and use the shop feature to enhance their learning experience.

![Student Profile](assets/images/Student Profile Student.PNG)
![Student Shop](assets/images/Student Shop student.PNG)

## System Architecture

### UML Diagrams

```mermaid
graph TD;
    Student-->Authentication;
    Student-->Classrooms;
    Student-->Quizzes;
    Teacher-->QuizManagement;
    Teacher-->ClassroomManagement;
    ClassroomManagement-->Students;
```

For a complete understanding of our system architecture, refer to our detailed UML diagrams:

![Simplified UML](assets/images/FullStack_Quizz_Masterz_UML_Use_Case_Diagramm_simplified.jpg)

{: .download }
> For more detailed technical documentation, check our [architecture documentation](technical-docs/architecture.md) section.