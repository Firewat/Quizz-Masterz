# Responsible: LAsse
# filepath: c:\Users\lasse\Desktop\Full_Stack_Quizz_Masterz\website\components.py
"""
Python-based UI Components for Quiz Masters
Provides reusable component classes for generating HTML programmatically
"""

from markupsafe import Markup


# Base class for all reusable UI components
class Component:
    """Base component class for UI elements"""
    # Base class providing common functionality for all UI components


# Renders clickable buttons with custom styling
class Button(Component):
    """Interactive button component with styling and actions"""
    # Button rendering with various styles and click handlers


# Creates bordered containers for organizing content
class Card(Component):
    """Card layout component for content display"""
    # Card container with header, body, and footer sections


# Displays status messages to users
class Alert(Component):
    """Alert/notification component for user feedback"""
    # Success, error, warning, and info alert messages


# Handles form field rendering and validation
class Form(Component):
    """Form component with field rendering and validation"""
    # Comprehensive form handling with Flask-WTF integration


# Displays quiz information in card format
class QuizCard(Component):
    """Specialized card component for quiz display"""
    # Quiz information presentation with actions and metadata


# Creates main page layouts with navigation
class Dashboard(Component):
    """Dashboard layout component with widgets"""
    # Main layout for student/teacher dashboards with navigation


# Manages responsive column layouts
class Grid(Component):
    """Responsive grid layout component"""
    # Bootstrap-style grid system for responsive layouts


# Converts Flask forms to HTML with styling
def render_form(form, template_name=None):
    """Utility function for rendering Flask-WTF forms"""
    # Enhanced form rendering with accessibility and styling


# Builds dashboard interface for student users
def create_student_dashboard(user):
    """Generate student dashboard layout"""
    # Student-specific dashboard with quiz history and progress


# Builds dashboard interface for teacher users
def create_teacher_dashboard(user):
    """Generate teacher dashboard layout"""
    # Teacher-specific dashboard with quiz management and analytics

    

