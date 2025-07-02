# source: [13,18]
"""
Main Application Entry Point for Quiz Masters
Flask application startup and development server configuration
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    # Development server 
    app.run(debug=True)