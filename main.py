# Responsible: Furkan
# filepath: c:\Users\lasse\Desktop\Full_Stack_Quizz_Masterz\main.py
"""
Main Application Entry Point for Quiz Masters
Flask application startup and development server configuration
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    # Development server 
    app.run(debug=True)