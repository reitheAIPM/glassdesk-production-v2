"""
Database schema and initialization for GlassDesk
Provides SQL schema definitions and database setup functions
"""

import os
import logging
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

# SQL schema definition
SCHEMA_SQL = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gmail messages table
CREATE TABLE IF NOT EXISTS gmail_messages (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    thread_id VARCHAR(255),
    subject TEXT,
    sender TEXT,
    recipient TEXT,
    date TIMESTAMP,
    snippet TEXT,
    body TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Zoom meetings table
CREATE TABLE IF NOT EXISTS zoom_meetings (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    topic TEXT,
    start_time TIMESTAMP,
    duration INTEGER,
    recording_files JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Asana tasks table
CREATE TABLE IF NOT EXISTS asana_tasks (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT,
    completed BOOLEAN,
    assignee TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def get_database_connection() -> Optional[psycopg2.extensions.connection]:
    """Get database connection using environment variables"""
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'glassdesk'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            port=os.getenv('DB_PORT', '5432')
        )
        return connection
    except Exception as e:
        logging.error(f"Database connection failed: {str(e)}")
        return None

def init_database() -> bool:
    """Initialize database with schema"""
    connection = get_database_connection()
    if not connection:
        logging.error("Cannot initialize database - no connection available")
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(SCHEMA_SQL)
        connection.commit()
        cursor.close()
        connection.close()
        logging.info("Database schema initialized successfully")
        return True
    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}")
        if connection:
            connection.close()
        return False

def create_user(email: str, name: str) -> Optional[int]:
    """Create a new user and return user ID"""
    connection = get_database_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (email, name) VALUES (%s, %s) RETURNING id",
            (email, name)
        )
        user_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        connection.close()
        logging.info(f"Created user {email} with ID {user_id}")
        return user_id
    except Exception as e:
        logging.error(f"Failed to create user {email}: {str(e)}")
        if connection:
            connection.close()
        return None

def store_gmail_message(user_id: int, message_data: dict) -> bool:
    """Store Gmail message in database"""
    connection = get_database_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO gmail_messages 
            (id, user_id, thread_id, subject, sender, recipient, date, snippet, body)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                subject = EXCLUDED.subject,
                snippet = EXCLUDED.snippet,
                body = EXCLUDED.body
        """, (
            message_data['id'],
            user_id,
            message_data.get('threadId'),
            message_data.get('subject', ''),
            message_data.get('from', ''),
            message_data.get('to', ''),
            message_data.get('date'),
            message_data.get('snippet', ''),
            message_data.get('body', '')
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        logging.error(f"Failed to store Gmail message: {str(e)}")
        if connection:
            connection.close()
        return False 