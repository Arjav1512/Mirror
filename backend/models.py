"""Data models for Mirror application."""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class User:
    """User model."""
    id: Optional[int] = None
    email: str = ""
    name: str = ""
    created_at: Optional[datetime] = None
    onboarding_data: Optional[dict] = None
    
    def to_dict(self):
        """Convert user to dictionary."""
        data = asdict(self)
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.onboarding_data:
            data['onboarding_data'] = json.dumps(self.onboarding_data)
        return data


@dataclass
class JournalEntry:
    """Journal entry model."""
    id: Optional[int] = None
    user_id: int = 0
    entry_text: str = ""
    timestamp: Optional[datetime] = None
    sentiment_score: Optional[float] = None
    valence: Optional[float] = None
    
    def to_dict(self):
        """Convert entry to dictionary."""
        data = asdict(self)
        if self.timestamp:
            data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class Bias:
    """Cognitive bias detection model."""
    id: Optional[int] = None
    entry_id: int = 0
    bias_type: str = ""
    detected_pattern: str = ""
    explanation: str = ""
    
    def to_dict(self):
        """Convert bias to dictionary."""
        return asdict(self)


@dataclass
class WeeklySummary:
    """Weekly summary model."""
    id: Optional[int] = None
    user_id: int = 0
    week_start: Optional[datetime] = None
    summary_text: str = ""
    themes: Optional[list] = None
    emotions: Optional[list] = None
    
    def to_dict(self):
        """Convert summary to dictionary."""
        data = asdict(self)
        if self.week_start:
            data['week_start'] = self.week_start.isoformat()
        if self.themes:
            data['themes'] = json.dumps(self.themes)
        if self.emotions:
            data['emotions'] = json.dumps(self.emotions)
        return data

