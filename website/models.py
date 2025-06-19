from . import db
from flask_login import UserMixin
import secrets

# Association table for User (student) and Classroom many-to-many relationship
classroom_members = db.Table('classroom_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True)
)

# Association table for Classroom and Quiz many-to-many relationship
classroom_quizzes = db.Table('classroom_quizzes',
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True),
    db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(50))  # 'student' or 'teacher'
    learning_points = db.Column(db.Integer, default=0) # User's total LPs
    # Relationship for teachers to their created classrooms
    classrooms_created = db.relationship('Classroom', foreign_keys='[Classroom.teacher_id]', backref='teacher', lazy=True)
    # Relationship for students to the classrooms they've joined
    joined_classrooms = db.relationship('Classroom', secondary=classroom_members,
                                        backref=db.backref('students', lazy='dynamic'),
                                        lazy='dynamic')
    quiz_attempts = db.relationship('StudentQuizAttempt', backref='student', lazy='dynamic') # Added

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Added: who created quiz
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade="all, delete-orphan") # Added
    # Add other relevant quiz fields here, e.g., description, number of questions
    # Example: description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Quiz {self.name}>'

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    join_code = db.Column(db.String(8), unique=True, nullable=False)
    # Relationship to quizzes in this classroom (many-to-many)
    quizzes = db.relationship('Quiz', secondary=classroom_quizzes,
                              backref=db.backref('classrooms_assigned_to', lazy='dynamic'),
                              lazy='dynamic')
    quiz_attempts = db.relationship('StudentQuizAttempt', backref='classroom', lazy='dynamic') # Added

    def __repr__(self):
        return f'<Classroom {self.name} - {self.join_code}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    learning_points = db.Column(db.Integer, nullable=False, default=1)
    answers = db.relationship('Answer', backref='question', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Question {self.text[:50]}>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Answer {self.text[:50]} ({self.is_correct})>'

class StudentQuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    score = db.Column(db.Integer, default=0) # LPs earned for this quiz in this classroom
    # Potentially add submission timestamp, answers given etc.

    def __repr__(self):
        return f'<StudentQuizAttempt student_id={self.student_id} quiz_id={self.quiz_id} classroom_id={self.classroom_id} score={self.score}>'
