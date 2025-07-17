---
title: Design Decisions
nav_order: 3
---

{: .no_toc }
# Design Decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Table of Contents
01: Web Application Framework Selection - Flask with Jinja2
02: Database Architecture - SQLite with SQLAlchemy
03: Frontend Architecture - Bootstrap with Jinja2

## 01: Web Application Framework Selection - Flask with Jinja2

### Meta
**Status**: Decided  
**Updated**: 20-06-2025

### Problem Statement
We needed to choose a web application framework that would allow us to:
- Create an interactive quiz platform
- Handle user authentication and sessions
- Manage database operations efficiently
- Support template-based rendering
- Maintain easy testability and deployment
- Enable rapid development with a small team

### Decision
We have decided to use Flask as our web framework with Jinja2 templating engine, SQLite database, and Python backend. This decision was made based on the following requirements:
- Need for a lightweight yet powerful web framework
- Simple integration with SQLite for data persistence
- Built-in template engine for dynamic HTML rendering
- Strong Python ecosystem for educational applications
- Easy learning curve for team members

### Regarded Options
We considered several technical approaches:

**Web Framework Comparison:**

Criterion | Flask + Jinja2 | Django | FastAPI
----------|---------------|---------|----------
Learning Curve | ✔️ Simple and intuitive | ❌ Steeper learning curve | ✔️ Modern and intuitive
Development Speed | ✔️ Rapid prototyping | ✔️ Lots of built-in features | ✔️ Fast development
Database Integration | ✔️ SQLAlchemy support | ✔️ ORM included | ✔️ Async database support
Template System | ✔️ Jinja2 built-in | ✔️ Django Templates | ❌ No built-in templating
Project Size | ✔️ Perfect for medium apps | ❌ Overkill for our needs | ✔️ Good for APIs
Flexibility | ✔️ Highly flexible | ❌ More rigid structure | ✔️ Very flexible

Key factors for choosing Flask:
1. Lightweight and flexible architecture
2. Perfect balance of simplicity and functionality
3. Excellent documentation and community support
4. Built-in Jinja2 templating for dynamic HTML
5. Easy integration with SQLite for data storage
6. Simple deployment process

## 02: Database Architecture - SQLite with SQLAlchemy

### Meta
**Status**: Decided  
**Updated**: 20-06-2025

### Problem Statement
For the quiz platform, we needed a database structure that:
- Manages user profiles and authentication
- Stores quiz content and results
- Enables classroom management
- Supports shop system and points management
- Is easy to maintain and scale

### Decision
We chose SQLite with SQLAlchemy ORM, with the following structure:
- Normalized database structure with foreign key relationships
- Efficient indexing of frequently queried fields
- Cascading deletion for dependent records
- Transaction integrity for critical operations

### Rationale
- Perfect for medium-sized applications
- Easy integration with Flask
- No separate database installation required
- Robust ORM functionality through SQLAlchemy
- Simple backup and migration

## 03: Frontend Architecture - Bootstrap with Jinja2

### Meta
**Status**: Decided  
**Updated**: 20-06-2025

### Problem Statement
The user interface needed to:
- Be responsive and user-friendly
- Provide consistent design
- Enable dynamic quiz interactions
- Ensure easy navigation
- Support gamification elements

### Decision
Implementation of a frontend architecture based on:
- Bootstrap for responsive design
- Jinja2 templates for dynamic HTML generation
- AJAX for real-time updates
- Client-side validation
- Modular CSS system for various components

### Rationale
- Bootstrap provides a mature grid system
- Jinja2 enables efficient template inheritance
- Easy integration of gamification elements
- Optimized user interaction through AJAX
- Good browser compatibility
