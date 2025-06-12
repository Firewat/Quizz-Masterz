# Responsible: Lasse
# filepath: c:\Users\lasse\Desktop\Full_Stack_Quizz_Masterz\website\models.py
"""
Database Models for Quiz Masters Application
SQLAlchemy models defining the data structure for users, quizzes, classrooms, and related entities
"""

from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Enhanced user model with role-based access"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(50))  # 'student' or 'teacher'
