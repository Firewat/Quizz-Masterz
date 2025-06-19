from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Classroom, User, Quiz, Question, Answer, StudentQuizAttempt # Added Quiz, Question, Answer, StudentQuizAttempt
from . import db
import secrets

views = Blueprint('views', __name__)

TEST_QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is this code doing?",
        "code": '''from flask import Blueprint, render_template
from flask_login import login_required, current_user

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)''',
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
        "code": '''user = User.query.filter_by(email=email).first()
if user:
    if check_password_hash(user.password, password):
        login_user(user, remember=True)
        return redirect(url_for('views.home'))''',
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
        "code": '''class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))''',
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
    return render_template("home.html", user=current_user)


@views.route('/test-quiz')
@login_required
def test_quiz():
    session['current_question'] = 0
    session['quiz_answers'] = []
    session['quiz_score'] = 0
    return redirect(url_for('views.test_quiz_question'))


@views.route('/test-quiz/question', methods=['GET', 'POST'])
@login_required
def test_quiz_question():
    if 'current_question' not in session:
        return redirect(url_for('views.test_quiz'))
    
    current_q = session['current_question']
    
    if request.method == 'POST':
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
        
        if session['current_question'] >= len(TEST_QUIZ_QUESTIONS):
            return redirect(url_for('views.test_quiz_results'))
        
        return redirect(url_for('views.test_quiz_question'))
    
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
    if 'quiz_answers' not in session:
        return redirect(url_for('views.test_quiz'))
    
    answers = session['quiz_answers']
    score = session['quiz_score']
    total = len(TEST_QUIZ_QUESTIONS)
    
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
    pass


@views.route('/delete-note-form', methods=['POST'])
def delete_note_form():
    pass


@views.route('/profile')
@login_required
def profile():
    pass


@views.route('/quizzes')
@login_required
def quizzes():
    pass


@views.route('/edit-quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    pass


@views.route('/manage-questions/<int:quiz_id>')
@login_required
def manage_questions(quiz_id):
    pass


@views.route('/manage-answers/<int:question_id>', methods=['GET', 'POST'])
@login_required
def manage_answers(question_id):
    pass


@views.route('/edit-question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    pass


@views.route('/delete-question/<int:question_id>', methods=['POST'])
@login_required
def delete_question(question_id):
    pass


@views.route('/join-quiz', methods=['GET', 'POST'])
@login_required
def join_quiz():
    pass


@views.route('/join-quiz-popup', methods=['GET', 'POST'])
@login_required
def join_quiz_popup():
    pass


@views.route('/take-quiz/<int:quiz_id>/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id, classroom_id):
    if current_user.role != 'student':
        flash('Only students can take quizzes.', category='error')
        return redirect(url_for('views.home'))

    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)

    if classroom not in current_user.joined_classrooms:
        flash('You are not a member of the classroom this quiz belongs to.', category='error')
        return redirect(url_for('views.student_my_classrooms'))

    if quiz not in classroom.quizzes:
        flash('This quiz is not available in this classroom.', category='error')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))

    # Check if student has already attempted this quiz in this classroom
    existing_attempt = StudentQuizAttempt.query.filter_by(
        student_id=current_user.id, 
        quiz_id=quiz.id, 
        classroom_id=classroom.id
    ).first()

    if existing_attempt:
        flash('You have already completed this quiz in this classroom.', category='info')
        # Optionally, redirect to a results page or back to classroom view
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))


    questions = quiz.questions.all()
    if not questions:
        flash('This quiz has no questions yet.', category='error')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))

    if request.method == 'POST':
        total_score_for_attempt = 0
        
        for question in questions:
            selected_answer_ids = request.form.getlist(f'question_{question.id}')
            question_score = 0
            correct_answers_for_question = [str(a.id) for a in question.answers if a.is_correct]
            
            is_question_correct = False
            if selected_answer_ids:
                for sel_id in selected_answer_ids:
                    if sel_id in correct_answers_for_question:
                        is_question_correct = True
                        break 
            
            if is_question_correct:
                question_score += question.learning_points
            else:
                pass # No points for incorrect or unattempted

            total_score_for_attempt += question_score

        # Update student's total learning points
        current_user.learning_points = (current_user.learning_points or 0) + total_score_for_attempt
        
        # Record the attempt
        new_attempt = StudentQuizAttempt(
            student_id=current_user.id,
            quiz_id=quiz.id,
            classroom_id=classroom.id,
            score=total_score_for_attempt
        )
        db.session.add(new_attempt)
        db.session.commit()

        flash(f'Quiz submitted! You scored {total_score_for_attempt} LP on "{quiz.name}". Your total LP is now {current_user.learning_points}.', category='success')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))

    # GET request: display the quiz
    # We need to pass the classroom_id to the template for the form action
    return render_template('take_quiz.html', user=current_user, quiz=quiz, questions=questions, classroom_id=classroom_id, classroom=classroom)

@views.route('/quiz-result-review/<int:quiz_id>')
@login_required
def quiz_result_review(quiz_id):
    pass


@views.route('/quiz-history')
@login_required
def quiz_history():
    pass


@views.route('/classrooms')
@login_required
def classrooms():
    pass


@views.route('/teacher/classrooms', methods=['GET'])
@login_required
def teacher_classrooms():
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    classrooms = Classroom.query.filter_by(teacher_id=current_user.id).all()
    return render_template("teacher_classrooms.html", user=current_user, classrooms=classrooms)


@views.route('/teacher/create_classroom', methods=['GET', 'POST'])
@login_required
def create_classroom():
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        classroom_name = request.form.get('classroom_name')
        if not classroom_name:
            flash('Classroom name cannot be empty!', category='error')
        else:
            join_code = secrets.token_hex(3).upper()
            new_classroom = Classroom(name=classroom_name, teacher_id=current_user.id, join_code=join_code)
            db.session.add(new_classroom)
            db.session.commit()
            flash(f'Classroom "{classroom_name}" created successfully! Join Code: {join_code}', category='success')
            return redirect(url_for('views.teacher_classrooms'))
    return render_template("create_classroom.html", user=current_user)


@views.route('/teacher/edit_classroom/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def edit_classroom(classroom_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    classroom = Classroom.query.get_or_404(classroom_id)
    if classroom.teacher_id != current_user.id:
        flash('You do not have permission to edit this classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))

    if request.method == 'POST':
        if 'update_name' in request.form:
            new_name = request.form.get('classroom_name')
            if not new_name:
                flash('Classroom name cannot be empty!', category='error')
            else:
                classroom.name = new_name
                db.session.commit()
                flash('Classroom name updated successfully!', category='success')
        elif 'delete_classroom' in request.form:
            # Add logic to handle quizzes and student enrollments before deleting
            db.session.delete(classroom)
            db.session.commit()
            flash('Classroom deleted successfully!', category='success')
            return redirect(url_for('views.teacher_classrooms'))
        
        return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))

    return render_template("edit_classroom.html", user=current_user, classroom=classroom)

@views.route('/teacher/kick_student/<int:classroom_id>/<int:student_id>', methods=['POST'])
@login_required
def kick_student(classroom_id, student_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))

    classroom = Classroom.query.get_or_404(classroom_id)
    if classroom.teacher_id != current_user.id:
        flash('You do not have permission to modify this classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))

    student_to_kick = User.query.get_or_404(student_id)

    if student_to_kick in classroom.students:
        classroom.students.remove(student_to_kick)
        db.session.commit()
        flash(f'{student_to_kick.first_name} has been kicked from the classroom.', category='success')
    else:
        flash(f'{student_to_kick.first_name} is not in this classroom.', category='error')

    return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))


# ---- Teacher Quiz Management ----
@views.route('/teacher/classroom/<int:classroom_id>/add_quiz', methods=['GET', 'POST'])
@login_required
def add_quiz_to_classroom(classroom_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    classroom = Classroom.query.get_or_404(classroom_id)
    if classroom.teacher_id != current_user.id:
        flash('You do not own this classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))

    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        if quiz_id == 'new':
            return redirect(url_for('views.create_quiz_for_classroom', classroom_id=classroom.id))
        else:
            quiz = Quiz.query.get(quiz_id)
            if quiz and quiz.teacher_id == current_user.id:
                if quiz not in classroom.quizzes:
                    classroom.quizzes.append(quiz)
                    db.session.commit()
                    flash(f'Quiz "{quiz.name}" added to classroom "{classroom.name}".', category='success')
                else:
                    flash(f'Quiz "{quiz.name}" is already in this classroom.', category='info')
            else:
                flash('Invalid quiz selected or you do not own this quiz.', category='error')
        return redirect(url_for('views.teacher_classrooms')) # Or back to edit_classroom

    # Get quizzes created by this teacher that are not already in this classroom
    teacher_quizzes = Quiz.query.filter_by(teacher_id=current_user.id).all()
    existing_classroom_quiz_ids = [q.id for q in classroom.quizzes]
    available_quizzes = [q for q in teacher_quizzes if q.id not in existing_classroom_quiz_ids]
    
    return render_template('add_quiz_to_classroom.html', user=current_user, classroom=classroom, available_quizzes=available_quizzes)

@views.route('/teacher/classroom/<int:classroom_id>/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz_for_classroom(classroom_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    classroom = Classroom.query.get_or_404(classroom_id) # Ensure classroom context
    if classroom.teacher_id != current_user.id:
        flash('You do not own this classroom context.', category='error')
        return redirect(url_for('views.teacher_classrooms'))

    if request.method == 'POST':
        quiz_name = request.form.get('quiz_name')
        if not quiz_name:
            flash('Quiz name cannot be empty.', category='error')
        else:
            new_quiz = Quiz(name=quiz_name, teacher_id=current_user.id)
            db.session.add(new_quiz)
            # Add to classroom directly after creation
            classroom.quizzes.append(new_quiz)
            db.session.commit()
            flash(f'Quiz "{new_quiz.name}" created and added to classroom. Now add questions.', category='success')
            return redirect(url_for('views.teacher_manage_quiz_questions', quiz_id=new_quiz.id))
    return render_template('teacher_create_quiz.html', user=current_user, classroom=classroom)

@views.route('/teacher/quiz/<int:quiz_id>/manage_questions', methods=['GET', 'POST'])
@login_required
def teacher_manage_quiz_questions(quiz_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != current_user.id:
        flash('You do not own this quiz.', category='error')
        return redirect(url_for('views.teacher_classrooms')) # Or a general quiz list page

    if request.method == 'POST':
        question_text = request.form.get('question_text')
        learning_points = request.form.get('learning_points', type=int)
        if not question_text or learning_points is None or learning_points < 0:
            flash('Question text cannot be empty and learning points must be a non-negative number.', category='error')
        else:
            new_question = Question(quiz_id=quiz.id, text=question_text, learning_points=learning_points)
            db.session.add(new_question)
            db.session.commit()
            flash('New question added.', category='success')
            return redirect(url_for('views.teacher_manage_question_answers', question_id=new_question.id))
    
    questions = quiz.questions.all()
    return render_template('teacher_manage_questions.html', user=current_user, quiz=quiz, questions=questions)

@views.route('/teacher/question/<int:question_id>/manage_answers', methods=['GET', 'POST'])
@login_required
def teacher_manage_question_answers(question_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    question = Question.query.get_or_404(question_id)
    quiz = question.quiz
    if quiz.teacher_id != current_user.id:
        flash('You do not own the quiz this question belongs to.', category='error')
        return redirect(url_for('views.teacher_classrooms'))

    if request.method == 'POST':
        answer_text = request.form.get('answer_text')
        is_correct = 'is_correct' in request.form

        if not answer_text:
            flash('Answer text cannot be empty.', category='error')
        elif len(question.answers.all()) >= 4 and not request.form.get('edit_answer_id'): # Limit to 4 answers for new adds
             flash('You can add a maximum of 4 answers per question.', category='error')
        else:
            # This part is simplified; real edit/delete would need more logic
            # For now, just adding new answers
            new_answer = Answer(question_id=question.id, text=answer_text, is_correct=is_correct)
            db.session.add(new_answer)
            db.session.commit()
            flash('Answer added.', category='success')
            # Stay on the same page to add more answers or finish
            return redirect(url_for('views.teacher_manage_question_answers', question_id=question.id))

    answers = question.answers.all()
    return render_template('teacher_manage_answers.html', user=current_user, question=question, answers=answers, quiz_id=quiz.id)

# ---- End Teacher Quiz Management ----

@views.route('/student/join_classroom', methods=['GET', 'POST'])
@login_required
def student_join_classroom():
    if current_user.role != 'student':
        flash('Only students can join classrooms.', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        join_code = request.form.get('join_code')
        if not join_code:
            flash('Join code cannot be empty.', category='error')
        else:
            classroom_to_join = Classroom.query.filter_by(join_code=join_code).first()
            if classroom_to_join:
                if current_user in classroom_to_join.students:
                    flash('You are already a member of this classroom.', category='info')
                else:
                    classroom_to_join.students.append(current_user)
                    db.session.commit()
                    flash(f'Successfully joined classroom: {classroom_to_join.name}!', category='success')
                    return redirect(url_for('views.home')) # Or back to a student dashboard page
            else:
                flash('Invalid join code. Classroom not found.', category='error')
    
    return render_template("student_join_classroom.html", user=current_user)


@views.route('/student/my_classrooms', methods=['GET'])
@login_required
def student_my_classrooms():
    if current_user.role != 'student':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    # Get classrooms the student has joined
    # The joined_classrooms relationship on the User model provides this directly
    classrooms_joined = current_user.joined_classrooms.all() # Use .all() if you need to iterate in template immediately
    
    return render_template("student_my_classrooms.html", user=current_user, classrooms_joined=classrooms_joined)


@views.route('/student/classroom/<int:classroom_id>', methods=['GET'])
@login_required
def student_view_classroom(classroom_id):
    if current_user.role != 'student':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))

    classroom = Classroom.query.get_or_404(classroom_id)

    if classroom not in current_user.joined_classrooms:
        flash('You are not a member of this classroom.', category='error')
        return redirect(url_for('views.student_my_classrooms'))

    available_quizzes = classroom.quizzes.all()

    # Leaderboard logic
    # Fetch StudentQuizAttempt, sum scores per student for this classroom, then order
    # This is a simplified version. A more robust solution might use SQLAlchemy aggregates.
    attempts_in_classroom = StudentQuizAttempt.query.filter_by(classroom_id=classroom.id).all()
    student_scores = {}
    for attempt in attempts_in_classroom:
        student_scores[attempt.student_id] = student_scores.get(attempt.student_id, 0) + attempt.score
    
    # Sort students by score
    sorted_student_ids = sorted(student_scores.keys(), key=lambda sid: student_scores[sid], reverse=True)
    
    leaderboard = []
    for student_id in sorted_student_ids:
        student_user = User.query.get(student_id)
        if student_user: # Ensure student exists
            leaderboard.append({'name': student_user.first_name, 'score': student_scores[student_id]})

    # Ensure User.learning_points is available for the student
    student_total_lp = current_user.learning_points if current_user.learning_points is not None else 0

    return render_template("student_view_classroom_details.html", 
                         user=current_user, 
                         classroom=classroom,
                         available_quizzes=available_quizzes,
                         leaderboard=leaderboard,
                         student_total_lp=student_total_lp) # Pass total LP
