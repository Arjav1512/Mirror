"""Supabase database operations for Mirror application."""
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class SupabaseDatabase:
    """Database handler for Supabase operations with RLS."""

    def __init__(self):
        """Initialize Supabase client."""
        supabase_url = os.getenv('VITE_SUPABASE_URL')
        supabase_key = os.getenv('VITE_SUPABASE_ANON_KEY')

        if not supabase_url or not supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")

        self.client: Client = create_client(supabase_url, supabase_key)
        self._current_user_id: Optional[str] = None

    def set_user_context(self, user_id: str):
        """Set the current user context for operations."""
        self._current_user_id = user_id

    def create_user(self, email: str, name: str, onboarding_data: dict) -> str:
        """
        Create a new user and return user_id.
        Note: In production, this should use Supabase Auth.
        For now, we create users directly in the database.
        """
        try:
            response = self.client.table('users').insert({
                'email': email,
                'name': name,
                'onboarding_data': onboarding_data
            }).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]['id']
            raise Exception("Failed to create user")
        except Exception as e:
            existing_user = self.get_user_by_email(email)
            if existing_user:
                return existing_user['id']
            raise e

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        try:
            response = self.client.table('users')\
                .select('*')\
                .eq('email', email)\
                .maybeSingle()\
                .execute()

            return response.data
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID."""
        try:
            response = self.client.table('users')\
                .select('*')\
                .eq('id', user_id)\
                .maybeSingle()\
                .execute()

            return response.data
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    def add_journal_entry(
        self,
        user_id: str,
        entry_text: str,
        sentiment_score: float,
        valence: float
    ) -> str:
        """Add a new journal entry and return entry_id."""
        try:
            response = self.client.table('journal_entries').insert({
                'user_id': user_id,
                'entry_text': entry_text,
                'sentiment_score': sentiment_score,
                'valence': valence
            }).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]['id']
            raise Exception("Failed to create entry")
        except Exception as e:
            print(f"Error adding entry: {e}")
            raise e

    def get_user_entries(self, user_id: str, limit: Optional[int] = None) -> List[Dict]:
        """Get journal entries for a user."""
        try:
            query = self.client.table('journal_entries')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('timestamp', desc=True)

            if limit:
                query = query.limit(limit)

            response = query.execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching entries: {e}")
            return []

    def get_entries_dataframe(self, user_id: str) -> pd.DataFrame:
        """Get entries as pandas DataFrame for analysis."""
        try:
            response = self.client.table('journal_entries')\
                .select('timestamp, sentiment_score, valence')\
                .eq('user_id', user_id)\
                .order('timestamp', desc=False)\
                .execute()

            if not response.data:
                return pd.DataFrame()

            df = pd.DataFrame(response.data)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])

            return df
        except Exception as e:
            print(f"Error creating dataframe: {e}")
            return pd.DataFrame()

    def add_bias(
        self,
        entry_id: str,
        bias_type: str,
        detected_pattern: str,
        explanation: str
    ) -> str:
        """Add detected bias and return bias_id."""
        try:
            response = self.client.table('biases').insert({
                'entry_id': entry_id,
                'bias_type': bias_type,
                'detected_pattern': detected_pattern,
                'explanation': explanation
            }).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]['id']
            raise Exception("Failed to create bias")
        except Exception as e:
            print(f"Error adding bias: {e}")
            raise e

    def get_entry_biases(self, entry_id: str) -> List[Dict]:
        """Get biases for a journal entry."""
        try:
            response = self.client.table('biases')\
                .select('*')\
                .eq('entry_id', entry_id)\
                .execute()

            return response.data or []
        except Exception as e:
            print(f"Error fetching biases: {e}")
            return []

    def get_user_biases(self, user_id: str) -> List[Dict]:
        """Get all biases for a user's entries."""
        try:
            response = self.client.table('biases')\
                .select('*, journal_entries!inner(user_id)')\
                .eq('journal_entries.user_id', user_id)\
                .execute()

            return response.data or []
        except Exception as e:
            print(f"Error fetching user biases: {e}")
            return []

    def save_weekly_summary(
        self,
        user_id: str,
        week_start: datetime,
        summary_text: str,
        themes: List[str],
        emotions: List[str]
    ) -> str:
        """Save or update weekly summary."""
        try:
            week_start_str = week_start.strftime('%Y-%m-%d')

            response = self.client.table('weekly_summaries').upsert({
                'user_id': user_id,
                'week_start': week_start_str,
                'summary_text': summary_text,
                'themes': themes,
                'emotions': emotions
            }).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]['id']
            raise Exception("Failed to save summary")
        except Exception as e:
            print(f"Error saving summary: {e}")
            raise e

    def get_weekly_summary(self, user_id: str, week_start: datetime) -> Optional[Dict]:
        """Get weekly summary for a specific week."""
        try:
            week_start_str = week_start.strftime('%Y-%m-%d')

            response = self.client.table('weekly_summaries')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('week_start', week_start_str)\
                .maybeSingle()\
                .execute()

            return response.data
        except Exception as e:
            print(f"Error fetching summary: {e}")
            return None

    def delete_entry(self, entry_id: str) -> bool:
        """Delete a journal entry (cascades to biases)."""
        try:
            self.client.table('journal_entries')\
                .delete()\
                .eq('id', entry_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False
