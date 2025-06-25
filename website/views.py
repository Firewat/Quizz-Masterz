from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Classroom, User, Quiz, Question, Answer, StudentQuizAttempt, UserSkin
from . import db
import secrets

views = Blueprint('views', __name__)

def require_role(role):
    """Helper function to check user role and redirect if unauthorized"""
    if current_user.role != role:
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    return None

def get_classroom_or_404(classroom_id, teacher_check=True):
    """Helper function to get classroom and validate teacher ownership"""
    classroom = Classroom.query.get_or_404(classroom_id)
    if teacher_check and classroom.teacher_id != current_user.id:
        flash('You do not own this classroom.', category='error')
        return None
    return classroom

def get_quiz_or_404(quiz_id, teacher_check=True):
    """Helper function to get quiz and validate teacher ownership"""
    quiz = Quiz.query.get_or_404(quiz_id)
    if teacher_check and quiz.teacher_id != current_user.id:
        flash('You do not own this quiz.', category='error')
        return None
    return quiz



@views.route('/profile')
@login_required
def profile():
    # Get user's selected skin if they're a student
    selected_skin = None
    level_info = None
    if current_user.role == 'student':
        selected_skin = UserSkin.query.filter_by(user_id=current_user.id, is_selected=True).first()
        level_info = current_user.get_level_info()
    
    return render_template("profile.html", user=current_user, selected_skin=selected_skin, level_info=level_info)

@views.route('/take-quiz/<int:quiz_id>/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id, classroom_id):
    if current_user.role != 'student':
        flash('Only students can take quizzes.', category='error')
        return redirect(url_for('views.home'))

    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)

    # Check if quiz is published
    if not quiz.is_published:
        flash('This quiz is not available yet.', category='error')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))

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

    # Leaderboard logic for teacher view
    # Get all students in the classroom
    all_students = classroom.students.all()
    
    # Get quiz attempts for scoring
    attempts_in_classroom = StudentQuizAttempt.query.filter_by(classroom_id=classroom.id).all()
    student_scores = {}
    for attempt in attempts_in_classroom:
        student_scores[attempt.student_id] = student_scores.get(attempt.student_id, 0) + attempt.score
    
    # Create leaderboard entries for all students
    leaderboard = []
    for student in all_students:
        # Get student's selected skin
        selected_skin = UserSkin.query.filter_by(user_id=student.id, is_selected=True).first()
        
        leaderboard_entry = {
            'name': student.first_name,
            'email': student.email,
            'student_id': student.id,
            'score': student_scores.get(student.id, 0),  # 0 if no attempts
            'skin': selected_skin
        }
        leaderboard.append(leaderboard_entry)
    
    # Sort by score (highest first)
    leaderboard.sort(key=lambda x: x['score'], reverse=True)

    # Get quizzes and their submissions for review
    # Get published quizzes in this classroom
    classroom_quizzes = classroom.quizzes.filter_by(is_published=True).all()
    # Get draft quizzes created by this teacher (not yet in classroom)
    draft_quizzes = Quiz.query.filter_by(teacher_id=current_user.id, is_published=False).all()
    
    quiz_reviews = []
    
    # Process published quizzes with submissions
    for quiz in classroom_quizzes:
        # Get all submissions for this quiz in this classroom
        submissions = StudentQuizAttempt.query.filter_by(
            quiz_id=quiz.id, 
            classroom_id=classroom.id
        ).all()
        
        quiz_review = {
            'quiz': quiz,
            'submissions': [],
            'is_published': True
        }
        
        for submission in submissions:
            student = User.query.get(submission.student_id)
            quiz_review['submissions'].append({
                'student_name': student.first_name,
                'student_email': student.email,
                'score': submission.score,
                'submission_id': submission.id
            })
        
        quiz_reviews.append(quiz_review)
    
    # Add draft quizzes (no submissions yet)
    draft_quiz_reviews = []
    for quiz in draft_quizzes:
        draft_quiz_review = {
            'quiz': quiz,
            'is_published': False,
            'has_questions': quiz.questions.count() > 0,
            'questions_have_answers': all(q.answers.count() > 0 for q in quiz.questions) if quiz.questions.count() > 0 else False
        }
        draft_quiz_reviews.append(draft_quiz_review)

    return render_template("edit_classroom.html", user=current_user, classroom=classroom, leaderboard=leaderboard, quiz_reviews=quiz_reviews, draft_quiz_reviews=draft_quiz_reviews)

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


# Teacher Quiz Management Routes
@views.route('/teacher/classroom/<int:classroom_id>/add_quiz', methods=['GET', 'POST'])
@login_required
def add_quiz_to_classroom(classroom_id):
    role_check = require_role('teacher')
    if role_check: return role_check
    
    classroom = get_classroom_or_404(classroom_id)
    if not classroom: return redirect(url_for('views.teacher_classrooms'))

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

    # Get published quizzes created by this teacher that are not already in this classroom
    teacher_quizzes = Quiz.query.filter_by(teacher_id=current_user.id, is_published=True).all()
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
            # Create quiz as draft (not published and not added to classroom yet)
            new_quiz = Quiz(name=quiz_name, teacher_id=current_user.id, is_published=False)
            db.session.add(new_quiz)
            db.session.commit()
            flash(f'Quiz "{new_quiz.name}" created as draft. Now add questions.', category='success')
            return redirect(url_for('views.teacher_manage_quiz_questions', quiz_id=new_quiz.id, classroom_id=classroom.id))
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
        return redirect(url_for('views.teacher_classrooms'))
    
    # Get classroom_id from request args if provided
    classroom_id = request.args.get('classroom_id', type=int)

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
            return redirect(url_for('views.teacher_manage_question_answers', question_id=new_question.id, classroom_id=classroom_id))
    
    questions = quiz.questions.all()
    return render_template('teacher_manage_questions.html', user=current_user, quiz=quiz, questions=questions, classroom_id=classroom_id)

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
    
    # Get classroom_id from request args if provided
    classroom_id = request.args.get('classroom_id', type=int)

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
            return redirect(url_for('views.teacher_manage_question_answers', question_id=question.id, classroom_id=classroom_id))

    answers = question.answers.all()
    return render_template('teacher_manage_answers.html', user=current_user, question=question, answers=answers, quiz_id=quiz.id, classroom_id=classroom_id)

# ---- End Teacher Quiz Management ----

@views.route('/teacher/quiz/<int:quiz_id>/save_draft/<int:classroom_id>')
@login_required
def save_quiz_draft(quiz_id, classroom_id):
    """Save quiz as draft and return to classroom"""
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if quiz.teacher_id != current_user.id or classroom.teacher_id != current_user.id:
        flash('You do not own this quiz or classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))
    
    # Quiz remains as draft (is_published=False)
    flash(f'Quiz "{quiz.name}" saved as draft!', category='success')
    return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))

@views.route('/teacher/quiz/<int:quiz_id>/upload_to_classroom/<int:classroom_id>')
@login_required
def upload_quiz_to_classroom(quiz_id, classroom_id):
    """Publish quiz and make it available to students"""
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if quiz.teacher_id != current_user.id or classroom.teacher_id != current_user.id:
        flash('You do not own this quiz or classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))
    
    # Check if quiz has questions
    if quiz.questions.count() == 0:
        flash('Cannot upload quiz without any questions!', category='error')
        return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))
    
    # Check if questions have answers
    questions_without_answers = []
    for question in quiz.questions:
        if question.answers.count() == 0:
            questions_without_answers.append(question.text[:50] + "...")
    
    if questions_without_answers:
        flash(f'Cannot upload quiz! Some questions have no answers: {", ".join(questions_without_answers)}', category='error')
        return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))
    
    # Publish the quiz and add to classroom
    quiz.is_published = True
    if quiz not in classroom.quizzes:
        classroom.quizzes.append(quiz)
    db.session.commit()
    
    flash(f'Quiz "{quiz.name}" uploaded and is now available to students!', category='success')
    return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))

@views.route('/teacher/quiz/<int:quiz_id>/review/<int:classroom_id>')
@login_required
def quiz_review_details(quiz_id, classroom_id):
    """Show detailed review of a quiz including all students and submissions"""
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if quiz.teacher_id != current_user.id or classroom.teacher_id != current_user.id:
        flash('You do not own this quiz or classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))
    
    # Check if quiz is in this classroom
    if quiz not in classroom.quizzes:
        flash('This quiz is not in the specified classroom.', category='error')
        return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))
    
    # Get all students in the classroom
    all_students = classroom.students.all()
    
    # Get all submissions for this quiz in this classroom
    submissions = StudentQuizAttempt.query.filter_by(
        quiz_id=quiz.id, 
        classroom_id=classroom.id
    ).all()
    
    # Create a mapping of student_id to submission
    submissions_by_student = {submission.student_id: submission for submission in submissions}
    
    # Create detailed student data
    student_details = []
    for student in all_students:
        submission = submissions_by_student.get(student.id)
        student_detail = {
            'student': student,
            'has_taken': submission is not None,
            'score': submission.score if submission else 0,
            'submission': submission
        }
        student_details.append(student_detail)
    
    # Sort: students who took it first (by score desc), then students who haven't taken it
    student_details.sort(key=lambda x: (not x['has_taken'], -x['score'] if x['has_taken'] else 0))
    
    # Calculate statistics
    total_students = len(all_students)
    students_taken = len([s for s in student_details if s['has_taken']])
    students_not_taken = total_students - students_taken
    
    if students_taken > 0:
        average_score = sum(s['score'] for s in student_details if s['has_taken']) / students_taken
        highest_score = max(s['score'] for s in student_details if s['has_taken'])
        lowest_score = min(s['score'] for s in student_details if s['has_taken'])
    else:
        average_score = highest_score = lowest_score = 0
    
    stats = {
        'total_students': total_students,
        'students_taken': students_taken,
        'students_not_taken': students_not_taken,
        'average_score': round(average_score, 1),
        'highest_score': highest_score,
        'lowest_score': lowest_score,
        'participation_rate': round((students_taken / total_students * 100), 1) if total_students > 0 else 0
    }
    
    return render_template('quiz_review_details.html', 
                         user=current_user, 
                         quiz=quiz, 
                         classroom=classroom,
                         student_details=student_details,
                         stats=stats)

@views.route('/teacher/quiz/<int:quiz_id>/delete/<int:classroom_id>')
@login_required
def delete_quiz(quiz_id, classroom_id):
    """Remove a quiz from a classroom"""
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if quiz.teacher_id != current_user.id or classroom.teacher_id != current_user.id:
        flash('You do not own this quiz or classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))
    
    quiz_name = quiz.name
    
    # If the quiz is published and in the classroom, remove it from classroom
    if quiz.is_published and quiz in classroom.quizzes:
        classroom.quizzes.remove(quiz)
        # Delete student quiz attempts for this quiz in this classroom only
        StudentQuizAttempt.query.filter_by(quiz_id=quiz.id, classroom_id=classroom.id).delete()
        db.session.commit()
        flash(f'Quiz "{quiz_name}" has been removed from classroom "{classroom.name}".', category='success')
    elif not quiz.is_published:
        # For draft quizzes, we can delete them entirely since they're not published anywhere
        StudentQuizAttempt.query.filter_by(quiz_id=quiz.id).delete()
        db.session.delete(quiz)
        db.session.commit()
        flash(f'Draft quiz "{quiz_name}" has been deleted.', category='success')
    else:
        flash('Quiz is not in this classroom.', category='error')
    
    return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))

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

    # Import models at the beginning

    # Get available quizzes with taken status (only published quizzes)
    available_quizzes_data = []
    published_quizzes = classroom.quizzes.filter_by(is_published=True).all()
    for quiz in published_quizzes:
        # Check if student has taken this quiz
        existing_attempt = StudentQuizAttempt.query.filter_by(
            student_id=current_user.id,
            quiz_id=quiz.id,
            classroom_id=classroom.id
        ).first()
        
        quiz_data = {
            'quiz': quiz,
            'taken': existing_attempt is not None
        }
        available_quizzes_data.append(quiz_data)

    # Leaderboard logic    # Leaderboard logic - Show all students in classroom
    # Get all students in the classroom
    all_students = classroom.students.all()
    
    # Get quiz attempts for scoring
    attempts_in_classroom = StudentQuizAttempt.query.filter_by(classroom_id=classroom.id).all()
    student_scores = {}
    for attempt in attempts_in_classroom:
        student_scores[attempt.student_id] = student_scores.get(attempt.student_id, 0) + attempt.score
    
    # Create leaderboard entries for all students
    leaderboard = []
    for student in all_students:
        # Get student's selected skin
        selected_skin = UserSkin.query.filter_by(user_id=student.id, is_selected=True).first()
        
        leaderboard_entry = {
            'name': student.first_name,
            'score': student_scores.get(student.id, 0),  # 0 if no attempts
            'skin': selected_skin
        }
        leaderboard.append(leaderboard_entry)
    
    # Sort by score (highest first)
    leaderboard.sort(key=lambda x: x['score'], reverse=True)

    # Ensure User.learning_points is available for the student
    student_total_lp = current_user.learning_points if current_user.learning_points is not None else 0
    
    return render_template("student_view_classroom_details.html", 
                         user=current_user, 
                         classroom=classroom,
                         available_quizzes=available_quizzes_data,
                         leaderboard=leaderboard,
                         student_total_lp=student_total_lp) # Pass total LP

# Teacher Quizzes Route
@views.route('/teacher/quizzes')
@login_required
def teacher_quizzes():
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', category='error')
        return redirect(url_for('views.home'))
    
    # Get all quizzes created by this teacher
    teacher_quizzes = Quiz.query.filter_by(teacher_id=current_user.id).all()
    
    return render_template("teacher_quizzes.html", user=current_user, quizzes=teacher_quizzes)


# Student Quizzes Route  
@views.route('/student/quizzes')
@login_required
def student_quizzes():
    if current_user.role != 'student':
        flash('Access denied. Students only.', category='error')
        return redirect(url_for('views.home'))
    
    # Get quizzes available to this student through their classrooms
    student_classrooms = current_user.joined_classrooms
    available_quizzes = []
    
    for classroom in student_classrooms:
        for quiz in classroom.quizzes:
            # Check if student has taken this quiz by looking for existing attempts
            from .models import StudentQuizAttempt
            existing_attempt = StudentQuizAttempt.query.filter_by(
                student_id=current_user.id,
                quiz_id=quiz.id,
                classroom_id=classroom.id
            ).first()
            
            quiz_data = {
                'quiz': quiz,
                'classroom': classroom,
                'taken': existing_attempt is not None
            }
            available_quizzes.append(quiz_data)
    
    return render_template("student_quizzes.html", user=current_user, available_quizzes=available_quizzes)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

# Shop Route
@views.route('/shop')
@login_required
def shop():
    if current_user.role != 'student':
        flash('Access denied. Shop is only available to students.', category='error')
        return redirect(url_for('views.home'))
    
    # Skins
    skins = [
        {
            'id': 1,
            'name': 'Golden Crown',
            'description': 'A majestic golden crown for top performers',
            'price': 1000,
            'icon': 'fas fa-crown',
            'color': '#ffd700'
        },
        {
            'id': 2,
            'name': 'Wizard Hat',
            'description': 'Channel your inner wisdom with this magical hat',
            'price': 250,
            'icon': 'fas fa-hat-wizard',
            'color': '#8b5cf6'
        },
        {
            'id': 3,
            'name': 'Scholar Badge',
            'description': 'Show off your academic achievements',
            'price': 500,
            'icon': 'fas fa-medal',
            'color': '#10b981'
        },        {
            'id': 4,
            'name': 'Star Student',
            'description': 'Shine bright like a Diamond',
            'price': 100,
            'icon': 'fas fa-star',
            'color': '#f59e0b'
        },
        {
            'id': 5,
            'name': 'Lightning Bolt',
            'description': 'Strike with knowledge and speed',
            'price': 150,
            'icon': 'fas fa-bolt',
            'color': '#3b82f6'
        },
        {
            'id': 6,
            'name': 'Fire Phoenix',
            'description': 'Rise from challenges like a phoenix from the ashes',
            'price': 300,
            'icon': 'fas fa-fire',
            'color': '#ef4444'
        },
        {
            'id': 7,
            'name': 'Diamond Shield',
            'description': 'Unbreakable determination and excellence in learning',
            'price': 400,
            'icon': 'fas fa-shield-alt',
            'color': '#06b6d4'
        },
        {
            'id': 8,
            'name': 'Magic Wand',
            'description': 'Cast spells of knowledge and wisdom with this wand',
            'price': 200,
            'icon': 'fas fa-magic',
            'color': '#8b5cf6'
        },
        {
            'id': 9,
            'name': 'Trophy Master',
            'description': 'The ultimate achievement for quiz champions',
            'price': 750,
            'icon': 'fas fa-trophy',
            'color': '#f59e0b'
        }
    ]
    
    # Get user's owned skins
    owned_skins = UserSkin.query.filter_by(user_id=current_user.id).all()
    owned_skin_ids = [skin.skin_id for skin in owned_skins]
    selected_skin = UserSkin.query.filter_by(user_id=current_user.id, is_selected=True).first()
    
    return render_template("shop.html", user=current_user, skins=skins, owned_skin_ids=owned_skin_ids, selected_skin=selected_skin)

# Purchase Skin Route
@views.route('/shop/purchase/<int:skin_id>', methods=['POST'])
@login_required
def purchase_skin(skin_id):
    if current_user.role != 'student':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    if not current_user.learning_points or current_user.learning_points < 100:
        flash('You need at least 100 LP to unlock skins!', category='error')
        return redirect(url_for('views.shop'))
    
    # Check if already owned
    existing_skin = UserSkin.query.filter_by(user_id=current_user.id, skin_id=skin_id).first()
    if existing_skin:
        flash('You already own this skin!', category='error')
        return redirect(url_for('views.shop'))
      # Skin data
    skins_data = {
        1: {'name': 'Golden Crown', 'icon': 'fas fa-crown', 'color': '#ffd700'},
        2: {'name': 'Wizard Hat', 'icon': 'fas fa-hat-wizard', 'color': '#8b5cf6'},
        3: {'name': 'Scholar Badge', 'icon': 'fas fa-medal', 'color': '#10b981'},
        4: {'name': 'Star Student', 'icon': 'fas fa-star', 'color': '#f59e0b'},
        5: {'name': 'Lightning Bolt', 'icon': 'fas fa-bolt', 'color': '#3b82f6'},
        6: {'name': 'Fire Phoenix', 'icon': 'fas fa-fire', 'color': '#ef4444'},
        7: {'name': 'Diamond Shield', 'icon': 'fas fa-shield-alt', 'color': '#06b6d4'},
        8: {'name': 'Magic Wand', 'icon': 'fas fa-magic', 'color': '#8b5cf6'},
        9: {'name': 'Trophy Master', 'icon': 'fas fa-trophy', 'color': '#f59e0b'}
    }
    
    if skin_id not in skins_data:
        flash('Invalid skin!', category='error')
        return redirect(url_for('views.shop'))
    
    # Purchase skin (no LP deduction - skins are unlocked at 100 LP)
    skin_info = skins_data[skin_id]
    new_skin = UserSkin(
        user_id=current_user.id,
        skin_id=skin_id,
        skin_name=skin_info['name'],
        skin_icon=skin_info['icon'],
        skin_color=skin_info['color']
    )
    
    db.session.add(new_skin)
    db.session.commit()
    
    flash(f'Congratulations! You unlocked the {skin_info["name"]} skin!', category='success')
    return redirect(url_for('views.shop'))

# Select Skin Route
@views.route('/shop/select/<int:skin_id>', methods=['POST'])
@login_required
def select_skin(skin_id):
    if current_user.role != 'student':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    # Check if user owns this skin
    skin = UserSkin.query.filter_by(user_id=current_user.id, skin_id=skin_id).first()
    if not skin:
        flash('You do not own this skin!', category='error')
        return redirect(url_for('views.shop'))
    
    # Deselect all current skins
    UserSkin.query.filter_by(user_id=current_user.id, is_selected=True).update({'is_selected': False})
    
    # Select the new skin
    skin.is_selected = True
    db.session.commit()
    
    flash(f'You are now displaying the {skin.skin_name} skin!', category='success')
    return redirect(url_for('views.shop'))
