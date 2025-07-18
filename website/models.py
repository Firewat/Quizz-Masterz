# source: [15,14,37]
from . import db
from flask_login import UserMixin


classroom_members = db.Table('classroom_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True)
)

classroom_quizzes = db.Table('classroom_quizzes',
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True),
    db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(50))
    learning_points = db.Column(db.Integer, default=0)
    selected_avatar = db.Column(db.String(100), default=None)  
    unlocked_avatars = db.Column(db.Text, default='')  
    classrooms_created = db.relationship('Classroom', foreign_keys='[Classroom.teacher_id]', backref='teacher', lazy=True)
    joined_classrooms = db.relationship('Classroom', secondary=classroom_members,
                                        backref=db.backref('students', lazy='dynamic'),
                                        lazy='dynamic')
    quiz_attempts = db.relationship('StudentQuizAttempt', backref='student', lazy='dynamic')

    def get_level_info(self):
        if not self.learning_points or self.learning_points < 100:
            return {
                'current_level': 0,
                'current_lp': self.learning_points or 0,
                'next_level_lp': 100,
                'progress_percentage': ((self.learning_points or 0) / 100) * 100,
                'remaining_lp': 100 - (self.learning_points or 0),
                'level_start_lp': 0,
                'lp_in_current_level': self.learning_points or 0,
                'lp_needed_for_next': 100,
                'is_max_level': False
            }
        
        level = 1
        level_threshold = 100
        
        while self.learning_points >= level_threshold * 2:
            level += 1
            level_threshold *= 2
        
        next_level_threshold = level_threshold * 2
        
        lp_in_current_level = self.learning_points - level_threshold
        lp_needed_for_next = next_level_threshold - level_threshold
        progress_percentage = (lp_in_current_level / lp_needed_for_next) * 100
        
        return {
            'current_level': level,
            'current_lp': self.learning_points,
            'level_start_lp': level_threshold,
            'next_level_lp': next_level_threshold,
            'progress_percentage': min(max(progress_percentage, 0), 100),
            'remaining_lp': max(next_level_threshold - self.learning_points, 0),
            'lp_in_current_level': lp_in_current_level,
            'lp_needed_for_next': lp_needed_for_next,
            'is_max_level': False
        }

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade="all, delete-orphan")
    teacher = db.relationship('User', backref=db.backref('created_quizzes', lazy='dynamic'))

    def __repr__(self):
        return f'<Quiz {self.name}>'

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    join_code = db.Column(db.String(8), unique=True, nullable=False)
    quizzes = db.relationship('Quiz', secondary=classroom_quizzes,
                              backref=db.backref('classrooms_assigned_to', lazy='dynamic'),
                              lazy='dynamic')
    quiz_attempts = db.relationship('StudentQuizAttempt', backref='classroom', lazy='dynamic')

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
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<StudentQuizAttempt student_id={self.student_id} quiz_id={self.quiz_id} classroom_id={self.classroom_id} score={self.score}>'
    
    