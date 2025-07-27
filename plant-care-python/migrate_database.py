#!/usr/bin/env python3
"""
Database migration script to add new columns to the plants table
"""

import sqlite3
import os
from app import create_app
from database.models import db

def migrate_database():
    """Add new columns to the plants table if they don't exist"""
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Create all tables (this will create the database if it doesn't exist)
        db.create_all()
        
        # Get the database file path
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if new columns exist
        cursor.execute("PRAGMA table_info(plants)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print("Existing columns:", columns)
        
        # Add new columns if they don't exist
        new_columns = [
            ('english_name', 'TEXT'),
            ('description', 'TEXT'),
            ('care_instructions', 'TEXT')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                print(f"Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE plants ADD COLUMN {column_name} {column_type}")
            else:
                print(f"Column {column_name} already exists")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("Database migration completed successfully!")

if __name__ == "__main__":
    migrate_database() 