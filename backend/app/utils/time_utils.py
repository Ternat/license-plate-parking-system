from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Format datetime object to readable string (English format)"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_duration_hours(start: datetime, end: datetime) -> float:
    """Calculate duration between two datetimes in hours"""
    duration_seconds = (end - start).total_seconds()
    return round(duration_seconds / 3600, 2)