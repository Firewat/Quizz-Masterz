---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .no_toc }
# Reference documentation 

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Authentication

### `login()`

**Route:** `/login`

**Methods:** `GET` `POST`

**Purpose:** Handle user login with email and password validation.

**Sample output:** Redirects to home page on success, shows error messages on failure.

---

### `logout()`

**Route:** `/logout`

**Methods:** `GET`

**Purpose:** Log out the current user and end their session.

**Sample output:** Redirects to login page.

---

### `sign_up()`

**Route:** `/sign-up`

**Methods:** `GET` `POST`

**Purpose:** Register new users with email, name, password, and role selection.

**Sample output:** Redirects to home page on successful registration.

---

## Teacher Functions

### `teacher_classrooms()`

**Route:** `/teacher/classrooms`

**Methods:** `GET`

**Purpose:** Display all classrooms created by the teacher.

**Sample output:** List of teacher's classrooms with management options.

---

### `create_classroom()`

**Route:** `/teacher/create_classroom`

**Methods:** `GET` `POST`

**Purpose:** Create a new classroom with a name and automatically generated join code.

**Sample output:** Creates classroom and redirects to teacher's classrooms page.

---

### `edit_classroom(classroom_id)`

**Route:** `/teacher/edit_classroom/<int:classroom_id>`

**Methods:** `GET` `POST`

**Purpose:** Edit classroom details, manage students and quizzes, view leaderboard.

**Sample output:** Classroom management interface with student list and quiz options.

---

### `create_quiz_for_classroom(classroom_id)`

**Route:** `/teacher/classroom/<int:classroom_id>/create_quiz`

**Methods:** `GET` `POST`

**Purpose:** Create a new quiz within a specific classroom context.

**Sample output:** Redirects to quiz question management on creation.

---

### `teacher_manage_quiz_questions(quiz_id)`

**Route:** `/teacher/quiz/<int:quiz_id>/manage_questions`

**Methods:** `GET` `POST`

**Purpose:** Add and manage questions for a quiz.

**Sample output:** Interface for adding/editing quiz questions.

---

### `teacher_manage_question_answers(question_id)`

**Route:** `/teacher/question/<int:question_id>/manage_answers`

**Methods:** `GET` `POST`

**Purpose:** Manage answers for a specific quiz question.

**Sample output:** Interface for adding/editing question answers.

---

### `quiz_review_details(quiz_id, classroom_id)`

**Route:** `/teacher/quiz/<int:quiz_id>/review/<int:classroom_id>`

**Methods:** `GET`

**Purpose:** View detailed quiz statistics and student performance.

**Sample output:** Quiz statistics including scores and participation rates.

---

## Student Functions

### `student_join_classroom()`

**Route:** `/student/join_classroom`

**Methods:** `GET` `POST`

**Purpose:** Allow students to join a classroom using a join code.

**Sample output:** Success message and redirect to home on successful join.

---

### `student_my_classrooms()`

**Route:** `/student/my_classrooms`

**Methods:** `GET`

**Purpose:** Display all classrooms joined by the student.

**Sample output:** List of joined classrooms with access to quizzes.

---

### `take_quiz(quiz_id, classroom_id)`

**Route:** `/take-quiz/<int:quiz_id>/<int:classroom_id>`

**Methods:** `GET` `POST`

**Purpose:** Allow students to take a quiz and submit answers.

**Sample output:** Quiz interface and score results after submission.

---

### `student_view_classroom(classroom_id)`

**Route:** `/student/classroom/<int:classroom_id>`

**Methods:** `GET`

**Purpose:** Show classroom details, available quizzes, and leaderboard to students.

**Sample output:** Classroom view with quiz list and class rankings.

---

## Shop System

### `shop()`

**Route:** `/shop`

**Methods:** `GET`

**Purpose:** Display available items for purchase with learning points.

**Sample output:** Shop interface with available avatars and items.

---

### `buy_item(item_id)`

**Route:** `/shop/buy/<int:item_id>`

**Methods:** `GET`

**Purpose:** Process purchase of shop items using learning points.

**Sample output:** Purchase confirmation or error message.

---

### `select_avatar(avatar_icon)`

**Route:** `/shop/select-avatar/<avatar_icon>`

**Methods:** `GET`

**Purpose:** Allow students to select and activate purchased avatars.

**Sample output:** Avatar selection confirmation.

---

## API Endpoints

### `api_students()`

**Route:** `/api/students`

**Methods:** `GET`

**Purpose:** Retrieve list of all students with their learning points.

**Sample output:** JSON with student data including IDs, names, and points.

  ```json
  {
    "students": [
      {
        "id": 1,
        "name": "Lasse",
        "email": "lasse@gmail.com",
        "learning_points": 78
      },
      ...
    ],
    "total": 10
  }

---

### `api_shop_items()`

**Route:** `/api/shop-items`

**Methods:** `GET`

**Purpose:** Get list of available shop items and their prices.

**Sample output:** JSON with shop items data including names, prices, and types.