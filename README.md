# Flask Quiz App – Create, Play, Share!

An intuitive and fun web app that lets users play quizzes, create their own, share them, and challenge others – either in real-time or asynchronously. Built with Flask (Python) and using JSON for flexible question storage.

## Features

-  **Play quizzes**: Answer questions in the browser with automatic scoring and instant feedback.
-  **Create quizzes**: Build your own quizzes via a web form or by uploading JSON.
-  **Share & challenge**: Generate shareable links and invite friends to compete.
-  **Multiplayer mode**: Play in real-time (using WebSockets) or asynchronously.
-  **Stats & high scores**: Track progress, view leaderboards, and compare results.

##  Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Data storage**: JSON files (optionally SQLite for persistence)
- **Real-time support**: Flask-SocketIO (for multiplayer mode)

## 📁 Project Structure

```bash
flask-quiz-app/
│
├── app.py                # Main Flask application
├── templates/
│   └── index.html        # Main UI and quiz interface
├── static/
│   ├── style.css         # CSS styles
│   └── script.js         # Client-side interactivity
├── quizzes/
│   └── example_quiz.json      # Sample quiz in JSON format
├── requirements.txt      # Python dependencies
└── README.md             # This file
