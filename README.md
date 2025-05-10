# Quizz Masterz – Deine Wissensreise

**Quizz Masterz** ist eine intuitive, unterhaltsame Quiz-Web-App, die Wissen mit spielerischem Fortschritt verbindet. Nutzer:innen reisen über eine virtuelle Weltkarte, lösen thematische Quizfragen, schalten neue Regionen frei und treten gegen andere an.

## Team

**Name:** Quizz Masterz  
**Contributors:** Furkan Dinc, David Levi, Lasse Schulz

## Idee

Viele Lernplattformen sind unübersichtlich oder nicht motivierend genug. Unser Ziel ist es, Lernen spannender zu machen – durch Gamification, soziale Herausforderungen und eine ansprechende visuelle Aufbereitung.

## Konzept

- Interaktive Weltkarte mit freischaltbaren Themenbereichen  
- Quiz-Spielmodi mit Punkten, Jokern, Belohnungen  
- Möglichkeit, eigene Quizze zu erstellen und (zu teilen)
- Optional: Herausforderungen gegen Freund:innen oder Bossgegner  

## Zielgruppen

- Schüler:innen, Studierende  
- Lehrkräfte mit Fokus auf interaktive Inhalte  
- Wissensbegeisterte, die spielerisch lernen wollen  

## Tech Stack

- **Backend:** Python (Flask), SQLite  
- **Frontend:** HTML, CSS, JavaScript, Jinja  
- **Daten:** JSON  

## Projektstruktur

```
quiz-webapp/
├── backend/
│   ├── app.py                # Haupt-Flask-App
│   ├── routes/               # Strukturierte Blueprints für verschiedene Funktionen
│   │   ├── auth.py           # Login, Registrierung, Sessions
│   │   ├── quiz.py           # Quiz-Logik und Spielfunktionen
│   │   └── worldmap.py       # Logik zur Weltkarte & Themenfortschritt
│   ├── models/               # Datenbankmodelle (User, Quiz, Fragen etc.)
│   │   ├── user.py
│   │   ├── quiz.py
│   │   └── progress.py
│   ├── services/             # Hilfsfunktionen & Business-Logik
│   │   ├── scoring.py
│   │   ├── map_logic.py
│   │   └── json_parser.py
│   └── database/             # Initialisierung & SQLite-Verwaltung
│       ├── init_db.py
│       └── schema.sql

├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── map.js         # Weltkarte-Interaktionen
│   │   │   └── quiz.js        # Quizsteuerung
│   │   └── images/
│   │       ├── continents/    # Icons/Visuals zu Quiz-Kategorien
│   │       └── ui/            # Buttons, Fortschrittsleisten etc.
│   └── templates/
│       ├── layout.html        # Grundlayout 
│       ├── index.html         # Startseite
│       ├── login.html         # Login/Register
│       ├── dashboard.html     # Profilübersicht
│       ├── worldmap.html      # Weltkarte & Kategorien
│       └── quiz.html          # Quizanzeige

├── quizzes/
│   ├── history.json
│   ├── science.json
│   └── geography.json

├── docs/
│   ├── concept.md            # Konzept, Zielgruppen, UX
│   ├── goals.md              # Teamziele & Fortschritte
│   └── gamification.md       # Beschreibung Gamification-Ansatz „Wissensreise“

├── tests/
│   ├── test_quiz_logic.py
│   ├── test_user_flow.py
│   └── test_worldmap_unlocks.py

├── requirements.txt
├── README.md
└── run.py                   # Startpunkt für die App (alias für app.py)


```

