# source: [16,37]

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')


