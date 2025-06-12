# Responsible: Lasse
# filepath: c:\Users\lasse\Desktop\Full_Stack_Quizz_Masterz\website\forms.py
"""
Enhanced Python-based Forms for Quiz Masters
All form logic handled in Python using Flask-WTF with improved validation and accessibility
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """login form with better validation"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    """sign up form with comprehensive validation"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=150)])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class CreateQuizForm(FlaskForm):
    """Form for creating a new quiz"""



class CreateClassroomForm(FlaskForm):
    """Enhanced form for creating a classroom"""
    # Form for teachers to create new classrooms with name and settings


class JoinQuizForm(FlaskForm):
    """Enhanced form for joining a quiz"""
    # Form for students to join a quiz using access code


class JoinClassroomForm(FlaskForm):
    """Enhanced form for students to join a classroom"""
    # Form for students to join a classroom using classroom code


class EditProfileForm(FlaskForm):
    """Enhanced form for editing user profile"""
    # Form for users to edit their profile information like name and email


class ChangePasswordForm(FlaskForm):
    """Enhanced form for changing password"""
    # Form for users to change their password with current and new password fields


class QuizAnswerForm(FlaskForm):
    """Dynamic form for quiz answers - created programmatically"""
    # Dynamic form generated based on quiz questions for student answers


class SearchForm(FlaskForm):
    """Form for searching quizzes/classrooms"""
    # Form with search field for finding quizzes and classrooms


class NoteForm(FlaskForm):
    """Form for creating a note"""
    # Form for students to create and save notes


class EditQuizForm(FlaskForm):
    """Form for editing quiz details"""
    # Form for editing existing quiz title, description, and settings


class EditQuestionForm(FlaskForm):
    """Form for editing a question"""
    # Form for editing existing question text and learning points


class EditClassroomForm(FlaskForm):
    """Form for editing classroom details"""
    # Form for editing classroom name and settings


class AddQuizToClassroomForm(FlaskForm):
    """Form for adding a quiz to a classroom"""
    # Form for teachers to assign existing quizzes to classrooms


class CreateQuestionWithAnswersForm(FlaskForm):
    """Enhanced form for creating questions with up to 4 answers"""
    # Comprehensive form for creating questions with multiple answer options


class AddAnswerForm(FlaskForm):
    """Form for adding a single answer to a question"""
    # Form for adding individual answer options to existing questions


class StudentQuizForm(FlaskForm):
    """Form for students to create quizzes"""
    # Form allowing students to create their own quizzes with basic settings


# Form rendering utilities and dynamic form creation functions
# These include utility classes and functions for rendering forms and creating dynamic quiz forms

