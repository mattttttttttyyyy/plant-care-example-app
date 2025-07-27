#!/usr/bin/env python3
"""
Database initialization script
"""

from app import create_app
from database.models import db

def init_database():
    """Initialize the database with all tables"""
    app = create_app()
    
    with app.app_context():
        # This will create all tables with the current schema
        db.create_all()
        print("Database initialized successfully!")
        print("Tables created with all new columns.")

if __name__ == "__main__":
    init_database() 