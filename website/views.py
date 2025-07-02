# source: [13,17,18,21,22,25,37]

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Classroom, User, Quiz, Question, Answer, StudentQuizAttempt
from . import db
import secrets

views = Blueprint('views', __name__)

def require_role(role):
    if current_user.role != role:
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    return None

def get_classroom_or_404(classroom_id, teacher_check=True):
    classroom = Classroom.query.get_or_404(classroom_id)
    if teacher_check and classroom.teacher_id != current_user.id:
        flash('You do not own this classroom.', category='error')
        return None
    return classroom

def get_quiz_or_404(quiz_id, teacher_check=True):
    quiz = Quiz.query.get_or_404(quiz_id)
    if teacher_check and quiz.teacher_id != current_user.id:
        flash('You do not own this quiz.', category='error')
        return None
    return quiz


@views.route('/')
@login_required
def home():
    available_quizzes = []
    if current_user.role == 'student':
        #AI used to shorten this section
        for classroom in current_user.joined_classrooms:
            for quiz in classroom.quizzes.filter_by(is_published=True):
                if not StudentQuizAttempt.query.filter_by(
                    student_id=current_user.id, quiz_id=quiz.id, classroom_id=classroom.id
                ).first():
                    available_quizzes.append({'quiz': quiz, 'classroom': classroom})
    
    return render_template("home.html", user=current_user, available_quizzes=available_quizzes)
        # until here


@views.route('/profile')
@login_required
def profile():
    level_info = None
    if current_user.role == 'student':
        level_info = current_user.get_level_info()
    
    return render_template("profile.html", user=current_user, 
                           level_info=level_info)



@views.route('/take-quiz/<int:quiz_id>/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id, classroom_id):
    if current_user.role != 'student':
        flash('Only students can take quizzes.', category='error')
        return redirect(url_for('views.home'))

    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)

    if not quiz.is_published:
        flash('This quiz is not available yet.', category='error')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))

    if classroom not in current_user.joined_classrooms:
        flash('You are not a member of the classroom.', category='error')
        return redirect(url_for('views.student_my_classrooms'))

    if quiz not in classroom.quizzes:
        flash('This quiz is not available in this classroom.', category='error')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))

    existing_attempt = StudentQuizAttempt.query.filter_by(
        student_id=current_user.id, 
        quiz_id=quiz.id, 
        classroom_id=classroom.id
    ).first()

    if existing_attempt:
        flash('You have already completed this quiz in this classroom.', category='info')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))


    questions = quiz.questions.all()
    if not questions:
        flash('This quiz has no questions yet.', category='error')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))

    if request.method == 'POST':
        total_score = 0
        #AI used to shorten this section
        for question in questions:
            selected_answers = request.form.getlist(f'question_{question.id}')
            correct_answers = [str(a.id) for a in question.answers if a.is_correct]
            
            if any(sel in correct_answers for sel in selected_answers):
                total_score += question.learning_points

        current_user.learning_points = (current_user.learning_points or 0) + total_score
        
        new_attempt = StudentQuizAttempt(
            student_id=current_user.id, quiz_id=quiz.id, 
            classroom_id=classroom.id, score=total_score
        )
        db.session.add(new_attempt)
        db.session.commit()
        # until here
        flash(f'Done! You scored {total_score} LP on "{quiz.name}". Your total LP is now {current_user.learning_points}.', category='success')
        return redirect(url_for('views.student_view_classroom', classroom_id=classroom_id))

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
                flash('Classroom name cannot be empty', category='error')
            else:
                classroom.name = new_name
                db.session.commit()
                flash('Classroom name updated successfully', category='success')
        elif 'delete_classroom' in request.form:
            db.session.delete(classroom)
            db.session.commit()
            flash('Classroom deleted successfully', category='success')
            return redirect(url_for('views.teacher_classrooms'))
        
        return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))




    #AI used to shorten this section
    attempts = StudentQuizAttempt.query.filter_by(classroom_id=classroom.id).all()
    student_scores = {}
    for attempt in attempts:
        student_scores[attempt.student_id] = student_scores.get(attempt.student_id, 0) + attempt.score

    leaderboard = sorted([{
        'name': student.first_name, 'email': student.email, 'student_id': student.id,
        'score': student_scores.get(student.id, 0)
    } for student in classroom.students.all()], key=lambda x: x['score'], reverse=True)
    # until here

    classroom_quizzes = classroom.quizzes.filter_by(is_published=True).all()
    draft_quizzes = Quiz.query.filter_by(teacher_id=current_user.id, is_published=False).all()
    
    quiz_reviews = []
    
    for quiz in classroom_quizzes:
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
        return redirect(url_for('views.teacher_classrooms')) 


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
    classroom = Classroom.query.get_or_404(classroom_id) 
    if classroom.teacher_id != current_user.id:
        flash('You do not own this classroom context.', category='error')
        return redirect(url_for('views.teacher_classrooms'))

    if request.method == 'POST':
        quiz_name = request.form.get('quiz_name')
        if not quiz_name:
            flash('Quiz name cannot be empty.', category='error')
        else:
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
    

    classroom_id = request.args.get('classroom_id', type=int)

    if request.method == 'POST':
        answer_text = request.form.get('answer_text')
        is_correct = 'is_correct' in request.form

        if not answer_text:
            flash('Answer text cannot be empty.', category='error')
        elif len(question.answers.all()) >= 4 and not request.form.get('edit_answer_id'): 
             flash('You can add a maximum of 4 answers per question.', category='error')
        else:
            new_answer = Answer(question_id=question.id, text=answer_text, is_correct=is_correct)
            db.session.add(new_answer)
            db.session.commit()
            flash('Answer added.', category='success')
            return redirect(url_for('views.teacher_manage_question_answers', question_id=question.id, classroom_id=classroom_id))

    answers = question.answers.all()
    
    quiz_classroom = quiz.classrooms_assigned_to.first()
    if quiz_classroom:
        classroom_id = quiz_classroom.id
    
    return render_template('teacher_manage_answers.html', user=current_user, question=question, answers=answers, quiz_id=quiz.id, classroom_id=classroom_id)





@views.route('/teacher/quiz/<int:quiz_id>/save_draft/<int:classroom_id>')
@login_required
def save_quiz_draft(quiz_id, classroom_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if quiz.teacher_id != current_user.id or classroom.teacher_id != current_user.id:
        flash('You do not own this quiz or classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))
    

    flash(f'Quiz "{quiz.name}" saved as draft!', category='success')
    return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))





@views.route('/teacher/quiz/<int:quiz_id>/upload_to_classroom/<int:classroom_id>')
@login_required
def upload_quiz_to_classroom(quiz_id, classroom_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if quiz.teacher_id != current_user.id or classroom.teacher_id != current_user.id:
        flash('You do not own this quiz or classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))
    

    #AI used to shorten this section
    if quiz.questions.count() == 0:
        flash('Cannot upload quiz without any questions!', category='error')
        return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))
    
    questions_without_answers = [q.text[:50] + "..." for q in quiz.questions if q.answers.count() == 0]
    if questions_without_answers:
        flash(f'Cannot upload quiz! Some questions have no answers: {", ".join(questions_without_answers)}', category='error')
        return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))
    # until here

    quiz.is_published = True
    if quiz not in classroom.quizzes:
        classroom.quizzes.append(quiz)
    db.session.commit()
    
    flash(f'Quiz "{quiz.name}" uploaded and is now available to students!', category='success')
    return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))




@views.route('/teacher/quiz/<int:quiz_id>/review/<int:classroom_id>')
@login_required
def quiz_review_details(quiz_id, classroom_id):
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if quiz.teacher_id != current_user.id or classroom.teacher_id != current_user.id:
        flash('You do not own this quiz or classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))

    if quiz not in classroom.quizzes:
        flash('This quiz is not in the specified classroom.', category='error')
        return redirect(url_for('views.edit_classroom', classroom_id=classroom.id))
    

    all_students = classroom.students.all()
    

    submissions = StudentQuizAttempt.query.filter_by(
        quiz_id=quiz.id, 
        classroom_id=classroom.id
    ).all()
    

    submissions_by_student = {submission.student_id: submission for submission in submissions}
    

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
    

    student_details.sort(key=lambda x: (not x['has_taken'], -x['score'] if x['has_taken'] else 0))
    

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
    if current_user.role != 'teacher':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if quiz.teacher_id != current_user.id or classroom.teacher_id != current_user.id:
        flash('You do not own this quiz or classroom.', category='error')
        return redirect(url_for('views.teacher_classrooms'))
    
    quiz_name = quiz.name
    

    if quiz.is_published and quiz in classroom.quizzes:
        classroom.quizzes.remove(quiz)

        StudentQuizAttempt.query.filter_by(quiz_id=quiz.id, classroom_id=classroom.id).delete()
        db.session.commit()
        flash(f'Quiz "{quiz_name}" has been removed from classroom "{classroom.name}".', category='success')
    elif not quiz.is_published:

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
                    return redirect(url_for('views.home')) 
            else:
                flash('Invalid join code. Classroom not found.', category='error')
    
    return render_template("student_join_classroom.html", user=current_user)





@views.route('/student/my_classrooms', methods=['GET'])
@login_required
def student_my_classrooms():
    if current_user.role != 'student':
        flash('Access denied.', category='error')
        return redirect(url_for('views.home'))
    
    classrooms_joined = current_user.joined_classrooms.all() 
    
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


    available_quizzes_data = []
    published_quizzes = classroom.quizzes.filter_by(is_published=True).all()
    for quiz in published_quizzes:

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

    #AI used to shorten this section
    attempts = StudentQuizAttempt.query.filter_by(classroom_id=classroom.id).all()
    student_scores = {}
    for attempt in attempts:
        student_scores[attempt.student_id] = student_scores.get(attempt.student_id, 0) + attempt.score
    
    leaderboard = sorted([{
        'name': student.first_name, 'score': student_scores.get(student.id, 0)
    } for student in classroom.students.all()], key=lambda x: x['score'], reverse=True)

    student_total_lp = current_user.learning_points if current_user.learning_points is not None else 0
    
    return render_template("student_view_classroom_details.html", 
                         user=current_user, 
                         classroom=classroom,
                         available_quizzes=available_quizzes_data,
                         leaderboard=leaderboard,
                         student_total_lp=student_total_lp) 
    # until here



@views.route('/teacher/quizzes')
@login_required
def teacher_quizzes():
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', category='error')
        return redirect(url_for('views.home'))
    
    teacher_quizzes = Quiz.query.filter_by(teacher_id=current_user.id).all()
    
    return render_template("teacher_quizzes.html", user=current_user, quizzes=teacher_quizzes)



@views.route('/student/quizzes')
@login_required
def student_quizzes():
    if current_user.role != 'student':
        flash('Access denied. Students only.', category='error')
        return redirect(url_for('views.home'))
#AI used to shorten this section
    available_quizzes = []
    for classroom in current_user.joined_classrooms:
        for quiz in classroom.quizzes:
            existing_attempt = StudentQuizAttempt.query.filter_by(
                student_id=current_user.id, quiz_id=quiz.id, classroom_id=classroom.id
            ).first()
            available_quizzes.append({
                'quiz': quiz, 'classroom': classroom, 'taken': existing_attempt is not None
            })
    
    return render_template("student_quizzes.html", user=current_user, available_quizzes=available_quizzes)
    # until here









# Shop Route (TODO: Implement working Shop)
@views.route('/shop')
@login_required
def shop():
    if current_user.role != 'student':
        flash('Access denied. Shop is only available to students.', category='error')
        return redirect(url_for('views.home'))
    
    return render_template("shop.html", user=current_user)




