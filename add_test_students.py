#CREATED WITH CHAT GPT AND CHANGED INFORMATION
# DO NOT DELETE THIS COMMENT
"""
Script to add 10 test students to the database and join them to the "History 101" classroom.
Run this script from the root directory of your project.
"""

import sys
import os
from werkzeug.security import generate_password_hash

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from website import create_app, db
from website.models import User, Classroom

def add_test_students():
    """Add 10 test students and join them to History 101 classroom"""
    
    app = create_app()
    
    with app.app_context():
        # Find the History 101 classroom
        classroom = Classroom.query.filter_by(name="Full-Stack Web Development SoSe-2025").first()
        
        if not classroom:
            print("Error: Could not find classroom named 'Full-Stack Web Development SoSe-2025'")
            print("Available classrooms:")
            for c in Classroom.query.all():
                print(f"  - {c.name}")
            return
        
        print(f"Found classroom: {classroom.name} (Join Code: {classroom.join_code})")
        
        # Create 10 test students
        students_added = 0
        students_joined = 0
        
        for i in range(1, 11):
            email = f"st{i}@test.com"
            
            # Check if student already exists
            existing_student = User.query.filter_by(email=email).first()
            
            if existing_student:
                print(f"Student {email} already exists")
                
                # Check if already joined the classroom
                if existing_student not in classroom.students:
                    classroom.students.append(existing_student)
                    students_joined += 1
                    print(f"  - Joined {email} to {classroom.name}")
                else:
                    print(f"  - {email} already in {classroom.name}")
            else:
                # Create new student
                new_student = User(
                    email=email,
                    first_name=f"Student {i}",
                    password=generate_password_hash("12345678", method='pbkdf2:sha256'),
                    role='student',
                    learning_points=0
                )
                
                db.session.add(new_student)
                db.session.flush()  # Flush to get the ID
                
                # Join the classroom
                classroom.students.append(new_student)
                
                students_added += 1
                students_joined += 1
                print(f"Created and joined student: {email}")
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\nSuccess!")
            print(f"  - {students_added} new students created")
            print(f"  - {students_joined} students joined to '{classroom.name}'")
            print(f"  - Total students in classroom: {classroom.students.count()}")
            
            print(f"\nAll students can now log in with password: 12345678")
            print(f"Classroom join code: {classroom.join_code}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error committing to database: {e}")

if __name__ == "__main__":
    add_test_students()
