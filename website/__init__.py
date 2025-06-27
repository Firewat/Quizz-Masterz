# Responsible: Lasse


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path



# Initialize database and migration objects
db = SQLAlchemy()
DB_NAME = "database.db"

# Initialize Flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the database
    db.init_app(app)


    # Initialize Flask-Migrate (deleted for now)
    # migrate.init_app(app, db)

    #import blueprints
    from .views import views
    from .auth import auth

    # Register blueprints for routing 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    
    with app.app_context():
        db.create_all()


    #import models after db is initialized
    from .models import User, Classroom, Quiz, Question, Answer, StudentQuizAttempt
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Create database if it doesn't exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database')
