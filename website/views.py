# Responsible: Lasse
# filepath: c:\Users\lasse\Desktop\Full_Stack_Quizz_Masterz\website\views.py
"""
Main Views and Routes for Quiz Masters Application
Flask routes handling user interactions, quiz management, and classroom functionality
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# Test quiz data
TEST_QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is this code doing?",
        "code": """from flask import Blueprint, render_template
from flask_login import login_required, current_user

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)""",
        "options": [
            "Creating a database table",
            "Defining a route that renders a home page template",
            "Sending an email to the user",
            "Deleting user data"
        ],
        "correct": 1
    },
    {
        "id": 2,
        "question": "What is this code doing?",
        "code": """user = User.query.filter_by(email=email).first()
if user:
    if check_password_hash(user.password, password):
        login_user(user, remember=True)
        return redirect(url_for('views.home'))""",
        "options": [
            "Creating a new user account",
            "Deleting a user from database",
            "Checking user credentials and logging them in",
            "Updating user profile information"
        ],
        "correct": 2
    },
    {
        "id": 3,
        "question": "What is this code doing?",
        "code": """class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))""",
        "options": [
            "Creating a function to send emails",
            "Defining a database model for user data",
            "Creating a login form",
            "Setting up a web server"
        ],
        "correct": 1
    }
]


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """Main dashboard for both students and teachers"""
    return render_template("home.html", user=current_user)


@views.route('/test-quiz')
@login_required
def test_quiz():
    """Start the test quiz"""
    session['current_question'] = 0
    session['quiz_answers'] = []
    session['quiz_score'] = 0
    return redirect(url_for('views.test_quiz_question'))


@views.route('/test-quiz/question', methods=['GET', 'POST'])
@login_required
def test_quiz_question():
    """Display current quiz question"""
    if 'current_question' not in session:
        return redirect(url_for('views.test_quiz'))
    
    current_q = session['current_question']
    
    if request.method == 'POST':
        # Process answer
        selected_answer = int(request.form.get('answer', 0))
        question = TEST_QUIZ_QUESTIONS[current_q]
        
        is_correct = selected_answer == question['correct']
        session['quiz_answers'].append({
            'question_id': question['id'],
            'selected': selected_answer,
            'correct': question['correct'],
            'is_correct': is_correct
        })
        
        if is_correct:
            session['quiz_score'] += 1
        
        session['current_question'] += 1
        
        # Check if quiz is complete
        if session['current_question'] >= len(TEST_QUIZ_QUESTIONS):
            return redirect(url_for('views.test_quiz_results'))
        
        return redirect(url_for('views.test_quiz_question'))
    
    # Display current question
    if current_q >= len(TEST_QUIZ_QUESTIONS):
        return redirect(url_for('views.test_quiz_results'))
    
    question = TEST_QUIZ_QUESTIONS[current_q]
    return render_template("test_quiz.html", 
                         question=question, 
                         question_num=current_q + 1, 
                         total=len(TEST_QUIZ_QUESTIONS),
                         user=current_user)


@views.route('/test-quiz/results')
@login_required
def test_quiz_results():
    """Show quiz results"""
    if 'quiz_answers' not in session:
        return redirect(url_for('views.test_quiz'))
    
    answers = session['quiz_answers']
    score = session['quiz_score']
    total = len(TEST_QUIZ_QUESTIONS)
    
    # Add question details for results display
    detailed_results = []
    for answer in answers:
        question = TEST_QUIZ_QUESTIONS[answer['question_id'] - 1]
        detailed_results.append({
            'question': question,
            'selected': answer['selected'],
            'correct': answer['correct'],
            'is_correct': answer['is_correct']
        })
    
    return render_template("test_quiz_results.html", 
                         results=detailed_results, 
                         score=score, 
                         total=total,
                         user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    """Delete a user's note"""
    # Handle AJAX requests for note deletion


@views.route('/delete-note-form', methods=['POST'])
def delete_note_form():
    """Alternative note deletion handler"""
    # Form-based note deletion with redirect


@views.route('/profile')
@login_required
def profile():
    """User profile page with statistics"""
    # Display user information, learning points, and achievement metrics


@views.route('/quizzes')
@login_required
def quizzes():
    """Quiz management page for teachers"""
    # List all quizzes created by the current teacher with management options


@views.route('/edit-quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    """Edit quiz details and settings"""
    # Form for updating quiz title, description, and learning points


@views.route('/manage-questions/<int:quiz_id>')
@login_required
def manage_questions(quiz_id):
    """Manage questions for a specific quiz"""
    # Add, edit, and delete questions within a quiz


@views.route('/manage-answers/<int:question_id>', methods=['GET', 'POST'])
@login_required
def manage_answers(question_id):
    """Manage answer options for a question"""
    # Add and modify answer choices for quiz questions


@views.route('/edit-question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    """Edit individual question content"""
    # Form for updating question text and point values


@views.route('/delete-question/<int:question_id>', methods=['POST'])
@login_required
def delete_question(question_id):
    """Delete a question from a quiz"""
    # Remove question and associated answers


@views.route('/join-quiz', methods=['GET', 'POST'])
@login_required
def join_quiz():
    """Join a quiz using access code"""
    # Form for students to enter quiz codes and start taking quizzes


@views.route('/join-quiz-popup', methods=['GET', 'POST'])
@login_required
def join_quiz_popup():
    """Popup version of quiz joining"""
    # AJAX-compatible quiz joining interface


@views.route('/take-quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    """Take a quiz and submit answers"""
    # Quiz-taking interface with question display and answer submission


@views.route('/quiz-result-review/<int:quiz_id>')
@login_required
def quiz_result_review(quiz_id):
    """Review quiz results and correct answers"""
    # Display quiz performance with correct/incorrect answer breakdown


@views.route('/quiz-history')
@login_required
def quiz_history():
    """View user's quiz history and scores"""
    # List of all quizzes taken by the student with scores and dates


@views.route('/classrooms')
@login_required
def classrooms():
    """Classroom management for teachers"""
    # Create, manage, and view classrooms with student enrollment


@views.route('/edit-classroom/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def edit_classroom(classroom_id):
    """Edit classroom details"""
    # Form for updating classroom name and settings


@views.route('/add-quiz-to-classroom/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def add_quiz_to_classroom(classroom_id):
    """Assign existing quizzes to a classroom"""
    # Interface for connecting quizzes with specific classrooms


@views.route('/review-submissions/<int:quiz_id>')
@login_required
def review_submissions(quiz_id):
    """Review all student submissions for a quiz"""
    # Teacher interface for viewing student performance on quizzes


@views.route('/student-quizzes')
@login_required
def student_quizzes():
    """Student quiz creation interface"""
    # Allow students to create and share their own quizzes
