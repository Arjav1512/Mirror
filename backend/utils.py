"""Utility functions for Mirror application."""
from datetime import datetime, timedelta
from typing import Optional, Tuple


def get_week_start(date: Optional[datetime] = None) -> datetime:
    """
    Get the start of the week (Monday) for a given date.
    
    Args:
        date: Date to get week start for (defaults to today)
    
    Returns:
        Monday of the week
    """
    if date is None:
        date = datetime.now()
    
    # Get Monday of the week
    days_since_monday = date.weekday()
    monday = date - timedelta(days=days_since_monday)
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


def get_week_range(date: Optional[datetime] = None) -> Tuple[datetime, datetime]:
    """
    Get the start and end of the week for a given date.
    
    Args:
        date: Date to get week range for (defaults to today)
    
    Returns:
        Tuple of (week_start, week_end)
    """
    week_start = get_week_start(date)
    week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return (week_start, week_end)


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display."""
    return timestamp.strftime('%Y-%m-%d %H:%M')


def format_date(timestamp: datetime) -> str:
    """Format date for display."""
    return timestamp.strftime('%B %d, %Y')

