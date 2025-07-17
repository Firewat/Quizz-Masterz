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

## 01: Web Application Framework Selection - Flask with Jinja2

### Meta
**Status**: Decided  
**Updated**: 2024-02-20

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
