# Simple Database Migration Script
# Responsible: AI Assistant
"""
Simple Database Migration Script for Quiz Masters
Uses direct Flask-Migrate CLI commands
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    print("="*50)
    print("🗄️  Quiz Masters - Simple Migration Manager")
    print("="*50)
    print()
    
    # Set Flask app environment variable
    os.environ['FLASK_APP'] = 'main.py'
    
    print("Available commands:")
    print("1. init     - Initialize migration repository")
    print("2. migrate  - Create a new migration")
    print("3. upgrade  - Apply migrations to database")
    print("4. current  - Show current migration")
    print("5. history  - Show migration history")
    print("6. exit     - Exit")
    print()
    
    while True:
        choice = input("Enter command (1-6 or command name): ").strip().lower()
        
        if choice in ["1", "init"]:
            print(" Initializing migration repository...")
            success = run_command("flask db init")
            if success:
                print("Migration repository initialized!")
            else:
                print("Failed to initialize migrations")
                
        elif choice in ["2", "migrate"]:
            message = input("Enter migration message (or press Enter for default): ").strip()
            if not message:
                message = "Auto migration"
            print(f" Creating migration: {message}")
            success = run_command(f'flask db migrate -m "{message}"')
            if success:
                print("Migration created!")
            else:
                print(" Failed to create migration")
                
        elif choice in ["3", "upgrade"]:
            print(" Applying migrations...")
            success = run_command("flask db upgrade")
            if success:
                print("Database upgraded!")
            else:
                print("Failed to upgrade database")
                
        elif choice in ["4", "current"]:
            print("📊 Current migration:")
            run_command("flask db current")
            
        elif choice in ["5", "history"]:
            print("Migration history:")
            run_command("flask db history")
            
        elif choice in ["6", "exit"]:
            break
        else:
            print("Invalid choice. Please try again.")
        print()

if __name__ == "__main__":
    main()
