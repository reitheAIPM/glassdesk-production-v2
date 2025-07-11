"""
Database migration system for GlassDesk
Handles schema changes and versioning as mentioned in contributing guidelines
"""

import os
import logging
from typing import List, Dict, Any
from datetime import datetime
from .database_schema import get_database_connection

class MigrationManager:
    """Manages database migrations and schema versioning"""
    
    def __init__(self):
        self.migrations_table_sql = """
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            version VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            checksum VARCHAR(64)
        );
        """
        
        self.migrations: List[Dict[str, Any]] = [
            {
                'version': '001',
                'name': 'initial_schema',
                'sql': """
                -- Initial schema migration
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
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
                
                CREATE TABLE IF NOT EXISTS zoom_meetings (
                    id VARCHAR(255) PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    topic TEXT,
                    start_time TIMESTAMP,
                    duration INTEGER,
                    recording_files JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
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
            },
            {
                'version': '002',
                'name': 'add_slack_messages',
                'sql': """
                -- Add Slack messages table
                CREATE TABLE IF NOT EXISTS slack_messages (
                    id VARCHAR(255) PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    channel_id VARCHAR(255),
                    text TEXT,
                    timestamp VARCHAR(50),
                    thread_ts VARCHAR(50),
                    reactions JSONB,
                    attachments JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            }
        ]
    
    def init_migrations_table(self) -> bool:
        """Initialize the migrations tracking table"""
        connection = get_database_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute(self.migrations_table_sql)
            connection.commit()
            cursor.close()
            connection.close()
            logging.info("Migrations table initialized")
            return True
        except Exception as e:
            logging.error(f"Failed to initialize migrations table: {str(e)}")
            if connection:
                connection.close()
            return False
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of already applied migration versions"""
        connection = get_database_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT version FROM migrations ORDER BY version")
            versions = [row[0] for row in cursor.fetchall()]
            cursor.close()
            connection.close()
            return versions
        except Exception as e:
            logging.error(f"Failed to get applied migrations: {str(e)}")
            if connection:
                connection.close()
            return []
    
    def apply_migration(self, migration: Dict[str, Any]) -> bool:
        """Apply a single migration"""
        connection = get_database_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Apply the migration SQL
            cursor.execute(migration['sql'])
            
            # Record the migration
            cursor.execute(
                "INSERT INTO migrations (version, name) VALUES (%s, %s)",
                (migration['version'], migration['name'])
            )
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logging.info(f"Applied migration {migration['version']}: {migration['name']}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to apply migration {migration['version']}: {str(e)}")
            if connection:
                connection.rollback()
                connection.close()
            return False
    
    def run_migrations(self) -> bool:
        """Run all pending migrations"""
        # Initialize migrations table
        if not self.init_migrations_table():
            return False
        
        # Get already applied migrations
        applied_versions = self.get_applied_migrations()
        
        # Find pending migrations
        pending_migrations = [
            m for m in self.migrations 
            if m['version'] not in applied_versions
        ]
        
        if not pending_migrations:
            logging.info("No pending migrations")
            return True
        
        logging.info(f"Running {len(pending_migrations)} pending migrations")
        
        # Apply each pending migration
        for migration in pending_migrations:
            if not self.apply_migration(migration):
                return False
        
        logging.info("All migrations completed successfully")
        return True

# Global migration manager instance
migration_manager = MigrationManager() 