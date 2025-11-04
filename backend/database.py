"""Database operations for Mirror application."""
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path
import pandas as pd

from models import User, JournalEntry, Bias, WeeklySummary


class Database:
    """Database handler for SQLite operations."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection."""
        if db_path is None:
            # Default to mirror.db in project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(project_root, "mirror.db")
        self.db_path = db_path
        self.ensure_database()
    
    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def ensure_database(self):
        """Create database and tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                onboarding_data TEXT
            )
        """)
        
        # Create journal_entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_text TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sentiment_score REAL,
                valence REAL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Create biases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS biases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id INTEGER NOT NULL,
                bias_type TEXT NOT NULL,
                detected_pattern TEXT,
                explanation TEXT,
                FOREIGN KEY (entry_id) REFERENCES journal_entries(id)
            )
        """)
        
        # Create weekly_summaries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weekly_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                week_start DATE NOT NULL,
                summary_text TEXT NOT NULL,
                themes TEXT,
                emotions TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, week_start)
            )
        """)
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_entries_user_timestamp 
            ON journal_entries(user_id, timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_biases_entry 
            ON biases(entry_id)
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, email: str, name: str, onboarding_data: dict) -> int:
        """Create a new user and return user_id."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (email, name, onboarding_data)
                VALUES (?, ?, ?)
            """, (email, name, json.dumps(onboarding_data)))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            # User already exists, get their ID
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            return result['id'] if result else None
        finally:
            conn.close()
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def add_journal_entry(self, user_id: int, entry_text: str, 
                         sentiment_score: float, valence: float) -> int:
        """Add a new journal entry."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO journal_entries 
            (user_id, entry_text, sentiment_score, valence)
            VALUES (?, ?, ?, ?)
        """, (user_id, entry_text, sentiment_score, valence))
        
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return entry_id
    
    def get_user_entries(self, user_id: int, limit: Optional[int] = None) -> List[Dict]:
        """Get journal entries for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT * FROM journal_entries 
            WHERE user_id = ? 
            ORDER BY timestamp DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_entries_dataframe(self, user_id: int) -> pd.DataFrame:
        """Get entries as pandas DataFrame for analysis."""
        conn = self.get_connection()
        
        query = """
            SELECT timestamp, sentiment_score, valence 
            FROM journal_entries 
            WHERE user_id = ? 
            ORDER BY timestamp ASC
        """
        
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def add_bias(self, entry_id: int, bias_type: str, 
                 detected_pattern: str, explanation: str) -> int:
        """Add detected bias."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO biases (entry_id, bias_type, detected_pattern, explanation)
            VALUES (?, ?, ?, ?)
        """, (entry_id, bias_type, detected_pattern, explanation))
        
        bias_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return bias_id
    
    def get_entry_biases(self, entry_id: int) -> List[Dict]:
        """Get biases for a journal entry."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM biases WHERE entry_id = ?
        """, (entry_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def save_weekly_summary(self, user_id: int, week_start: datetime,
                           summary_text: str, themes: List[str], 
                           emotions: List[str]) -> int:
        """Save or update weekly summary."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        week_start_str = week_start.strftime('%Y-%m-%d')
        
        cursor.execute("""
            INSERT OR REPLACE INTO weekly_summaries 
            (user_id, week_start, summary_text, themes, emotions)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, week_start_str, summary_text, 
              json.dumps(themes), json.dumps(emotions)))
        
        summary_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return summary_id
    
    def get_weekly_summary(self, user_id: int, week_start: datetime) -> Optional[Dict]:
        """Get weekly summary for a specific week."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        week_start_str = week_start.strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT * FROM weekly_summaries 
            WHERE user_id = ? AND week_start = ?
        """, (user_id, week_start_str))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            result = dict(row)
            if result.get('themes'):
                result['themes'] = json.loads(result['themes'])
            if result.get('emotions'):
                result['emotions'] = json.loads(result['emotions'])
            return result
        return None

