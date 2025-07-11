"""
Database package for GlassDesk
Contains schema definitions and database initialization logic
"""

from .database_schema import init_database

__all__ = ['init_database'] 