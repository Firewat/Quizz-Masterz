---
title: Architecture
parent: Technical Docs
nav_order: 1
layout: default
---

{: .no_toc }
# Architecture

{: .attention }
> This page describes how the application is structured and how important parts of the app work. It should give a new-joiner sufficient technical knowledge for contributing to the codebase.
> 
> See [this blog post](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) for an explanation of the concept and these examples:
>
> + <https://github.com/rust-lang/rust-analyzer/blob/master/docs/dev/architecture.md>
> + <https://github.com/Uriopass/Egregoria/blob/master/ARCHITECTURE.md>
> + <https://github.com/davish/obsidian-full-calendar/blob/main/src/README.md>
> 
> For structural and behavioral illustration, you might want to leverage [Mermaid](../ui-components.md), e.g., by charting common [C4](https://c4model.com/) or [UML](https://www.omg.org/spec/UML) diagrams.
> 
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

[Give a high-level overview of what your app does and how it achieves it: similar to the value proposition, but targeted at a fellow developer who wishes to contribute.]

For Teachers

    Classroom Management & Creation: Create and manage multiple classrooms.

    Quiz Creation: Build quizzes with multiple-choice questions supporting multiple correct answers.

    Student Monitoring: View student performance and quiz results.

    Set Learning Points: Set multiple correct answers with flexible scoring for Students to earn Learning Points (LP).

For Students

    Classroom Participation: Join classrooms using unique classroom codes.

    Quiz Taking: Take quizzes with multiple answer selection capability.

    (TODO) Performance Tracking: View quiz results with detailed scoring breakdown and earn LPs for your right answers.

    (TODO) Shop: Level up and earn Skins for your Profile.

System Features

    Multiple Answer Support: Students can select multiple answers per question.

    Partial Credit Scoring: Scoring system with partial credit for partially correct answers and penalties for incorrect selections.

    User Authentication: Secure login and registration system with role-based access (Teacher/Student).

## Codemap

[Describe how your app is structured. Don't aim for completeness, rather describe *just* the most important parts.]

## Cross-cutting concerns

[Describe anything that is important for a solid understanding of your codebase. Most likely, you want to explain the behavior of (parts of) your application. In this section, you may also link to important [design decisions](../design-decisions.md).]
