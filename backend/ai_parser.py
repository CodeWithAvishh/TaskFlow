"""
AI Quick Task Parser for TaskFlow
Parses natural language task descriptions and extracts structured information.

This is a rule-based parser, NOT an LLM. It recognizes specific keywords and patterns
to extract task information without requiring external API calls or language models.

Can be used independently for testing or integrated into FastAPI endpoints.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class TaskParser:
    """Parse natural language task descriptions into structured data."""
    
    PRIORITY_KEYWORDS = {
        'high': ['urgent', 'critical', 'asap', 'important', 'priority', 'high', 'blocking'],
        'medium': ['medium', 'normal', 'regular', 'standard'],
        'low': ['low', 'minor', 'trivial', 'whenever', 'eventually', 'backlog']
    }
    
    DUE_DATE_KEYWORDS = {
        'today': 0,
        'tomorrow': 1,
        'this week': 3,
        'next week': 7,
        'this month': 30,
        'next month': 60,
    }
    
    def __init__(self):
        pass
    
    def extract_priority(self, text: str) -> str:
        """
        Extract priority from text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Priority level: 'high', 'medium', or 'low'
        """
        text_lower = text.lower()
        
        for priority, keywords in self.PRIORITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return priority
        
        return 'medium'  # Default priority
    
    def extract_due_date(self, text: str) -> Optional[str]:
        """
        Extract due date from text.
        
        Recognizes:
        - Relative dates (today, tomorrow, this week, next week, etc.)
        - Specific dates (YYYY-MM-DD or MM/DD/YYYY)
        - Weekday names (Monday, Tuesday, etc.)
        
        Args:
            text: Input text to analyze
            
        Returns:
            Due date in YYYY-MM-DD format, or None if not found
        """
        text_lower = text.lower()
        
        # Check for specific date patterns
        # Pattern: YYYY-MM-DD or MM/DD/YYYY
        date_pattern = r'(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})'
        match = re.search(date_pattern, text)
        if match:
            return match.group(1)
        
        # Check for relative dates
        for keyword, days in self.DUE_DATE_KEYWORDS.items():
            if keyword in text_lower:
                due_date = datetime.now() + timedelta(days=days)
                return due_date.strftime('%Y-%m-%d')
        
        # Check for day of week
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i, day in enumerate(weekdays):
            if day in text_lower:
                # Calculate days until that day
                today = datetime.now()
                current_weekday = today.weekday()
                target_weekday = i  # Monday is 0
                
                days_ahead = target_weekday - current_weekday
                if days_ahead <= 0:
                    days_ahead += 7
                
                due_date = today + timedelta(days=days_ahead)
                return due_date.strftime('%Y-%m-%d')
        
        return None
    
    def extract_title(self, text: str) -> str:
        """
        Extract task title from text.
        
        Removes date patterns, time expressions, and priority keywords
        to get a clean title.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Cleaned task title
        """
        # Remove date patterns
        title = re.sub(r'\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4}', '', text)
        
        # Remove time expressions
        for keyword in list(self.DUE_DATE_KEYWORDS.keys()) + \
                       list(set(k for v in self.PRIORITY_KEYWORDS.values() for k in v)):
            title = re.sub(rf'\b{keyword}\b', '', title, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        title = re.sub(r'\s+', ' ', title).strip()
        
        # Ensure title is not too long
        if len(title) > 100:
            title = title[:97] + '...'
        
        return title if title else 'Untitled Task'
    
    def parse(self, text: str) -> Dict:
        """
        Parse natural language task description.
        
        Args:
            text: Natural language task description
        
        Returns:
            dict: Structured task data with keys:
                - title: Task title
                - priority: Task priority (low/medium/high)
                - due_date: Due date (YYYY-MM-DD format or None)
                - description: Original input text
        """
        return {
            'title': self.extract_title(text),
            'priority': self.extract_priority(text),
            'due_date': self.extract_due_date(text),
            'description': text
        }


def parse_multiple_tasks(text: str) -> List[Dict]:
    """
    Parse multiple tasks from a text block.
    
    Splits by newlines and supports list formats (bullets, numbers).
    
    Args:
        text: Text containing multiple task descriptions
        
    Returns:
        List of parsed task dictionaries
    """
    parser = TaskParser()
    
    # Split by common delimiters
    lines = text.split('\n')
    tasks = []
    
    for line in lines:
        line = line.strip()
        # Skip empty lines and common list prefixes
        if not line:
            continue
        
        line = re.sub(r'^[-*•]\s+', '', line)  # Remove bullet points
        line = re.sub(r'^\d+\.\s+', '', line)  # Remove numbered lists
        
        if line:
            parsed = parser.parse(line)
            tasks.append(parsed)
    
    return tasks


def format_task_output(task: Dict) -> str:
    """
    Format parsed task for display.
    
    Args:
        task: Parsed task dictionary
        
    Returns:
        Formatted string representation
    """
    output = f"""Task: {task['title']}
Priority: {task['priority'].upper()}"""
    
    if task['due_date']:
        output += f"\nDue Date: {task['due_date']}"
    
    return output
