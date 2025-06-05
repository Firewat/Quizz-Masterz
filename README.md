# Quiz Masters 🎓

A comprehensive Flask-based web application for creating, managing, and taking educational quizzes. Quiz Masters provides a platform for teachers to create and manage classrooms, create quizzes, and for students to join classrooms and take quizzes with multiple answer support and partial credit scoring.

## 🌟 Features

### For Teachers
- **Classroom Management**: Create and manage multiple classrooms
- **Quiz Creation**: Build quizzes with multiple-choice questions supporting multiple correct answers
- **Student Monitoring**: View student performance and quiz results
- **Answer Key Management**: Set multiple correct answers with flexible scoring

### For Students
- **Classroom Participation**: Join classrooms using classroom codes
- **Quiz Taking**: Take quizzes with multiple answer selection capability
- **Performance Tracking**: View quiz results with detailed scoring breakdown
- **Modern UI**: Clean, responsive interface with space-themed design

### System Features
- **Multiple Answer Support**: Students can select multiple answers per question
- **Partial Credit Scoring**: Intelligent scoring system with partial credit for partially correct answers
- **User Authentication**: Secure login and registration system
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Beautiful space-themed interface with glassmorphism effects

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd QuizMasters/Quizzz
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python main.py
   ```
   The database will be automatically created on first run.

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 📁 Project Structure

```
QuizMasters/Quizzz/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── instance/              # Database and instance files
├── migrations/            # Database migration files
├── website/               # Main application package
│   ├── __init__.py       # App factory and configuration
│   ├── models.py         # Database models
│   ├── views.py          # Main application routes
│   ├── auth.py           # Authentication routes
│   ├── forms.py          # WTForms form definitions
│   ├── components.py     # Reusable components
│   ├── static/           # Static files (CSS, images, JS)
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   └── templates/        # Jinja2 templates
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── sign_up.html
│       ├── profile.html
│       ├── create_quiz.html
│       ├── take_quiz.html
│       ├── quiz_results.html
│       └── ...
```

## 🎯 Usage Guide

### Getting Started

1. **Create an Account**
   - Visit the homepage and click "Sign Up"
   - Choose between Teacher or Student account types
   - Fill in your details and create your account

2. **For Teachers**
   - After logging in, create a classroom from your dashboard
   - Create quizzes with multiple-choice questions
   - Set multiple correct answers for each question
   - Share the classroom code with students

3. **For Students**
   - Log in to your account
   - Use "Join Classroom" on the homepage
   - Enter the classroom code provided by your teacher
   - Take available quizzes and view your results

### Quiz System

#### Creating Quizzes (Teachers)
1. Go to your classroom
2. Click "Create Quiz"
3. Add questions with multiple choice answers
4. Select multiple correct answers for each question
5. Publish the quiz for students

#### Taking Quizzes (Students)
1. Enter a classroom
2. Select an available quiz
3. For each question, select one or more answers using checkboxes
4. Submit the quiz to see your results

#### Scoring System
- **Full Credit (10 points)**: All correct answers selected, no incorrect answers
- **Partial Credit (1-5 points)**: Some correct answers selected, penalty for incorrect selections
- **No Credit (0 points)**: No correct answers selected
- **Negative Points (-2 points)**: Only incorrect answers selected

## 🛠️ Technical Details

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy with SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Forms**: Flask-WTF and WTForms
- **Authentication**: Flask-Login
- **Database Migrations**: Flask-Migrate

### Key Components

#### Models (`models.py`)
- **User**: Handles both teachers and students
- **Classroom**: Manages classroom information
- **Quiz**: Stores quiz metadata
- **Question**: Individual quiz questions
- **Answer**: Answer choices for questions
- **QuizResult**: Stores student quiz attempts
- **UserClassroom**: Many-to-many relationship for classroom membership

#### Forms (`forms.py`)
- Dynamic form generation for quizzes with checkbox support
- User registration and login forms
- Classroom and quiz creation forms

#### Views (`views.py`)
- Main application logic and route handlers
- Quiz processing with multiple answer support
- Dashboard and classroom management

#### Authentication (`auth.py`)
- User registration and login
- Session management
- Role-based access control

### Database Schema

The application uses SQLAlchemy ORM with the following main relationships:
- Users can be teachers or students
- Teachers can create multiple classrooms
- Students can join multiple classrooms
- Classrooms can have multiple quizzes
- Quizzes have multiple questions with multiple answers
- Students can take quizzes multiple times

## 🎨 UI/UX Features

- **Space Theme**: Beautiful earth background with cosmic aesthetics
- **Glassmorphism**: Modern transparent card designs
- **Responsive Design**: Works on all device sizes
- **Intuitive Navigation**: Clear user flow for both teachers and students
- **Visual Feedback**: Clear indicators for quiz results and partial credit

## 🔧 Development

### Running in Development Mode
```bash
python main.py
```
The app runs with debug mode enabled for development.

### Database Management
The application uses Flask-Migrate for database versioning:
```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

### Adding New Features
1. Update models in `models.py` if database changes are needed
2. Create/update forms in `forms.py`
3. Add routes in `views.py` or `auth.py`
4. Create/update templates in `templates/`
5. Add any static assets to `static/`

## 📝 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For questions or issues, please create an issue in the repository or contact the development team.

---

**Quiz Masters** - Making education interactive and engaging! 🎓✨


