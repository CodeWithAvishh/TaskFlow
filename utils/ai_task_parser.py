"""
AI Quick Task Parser for TaskFlow
Parses natural language task descriptions and extracts structured information
"""

import re
from datetime import datetime, timedelta


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
    
    def extract_priority(self, text):
        """Extract priority from text."""
        text_lower = text.lower()
        
        for priority, keywords in self.PRIORITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return priority
        
        return 'medium'  # Default priority
    
    def extract_due_date(self, text):
        """Extract due date from text."""
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
    
    def extract_title(self, text):
        """Extract task title from text."""
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
    
    def parse(self, text):
        """
        Parse natural language task description.
        
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


def parse_multiple_tasks(text):
    """Parse multiple tasks from a text block."""
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


def format_task_output(task):
    """Format parsed task for display."""
    output = f"""
Task: {task['title']}
Priority: {task['priority'].upper()}
"""
    if task['due_date']:
        output += f"Due Date: {task['due_date']}\n"
    
    return output.strip()


def main():
    """Interactive task parser."""
    print("\n" + "="*80)
    print("TaskFlow AI Quick Task Parser")
    print("="*80)
    print("\nThis tool parses natural language into structured tasks.")
    print("It extracts title, priority, and due date from text.\n")
    print("Examples:")
    print('  "Fix critical login bug - urgent, due tomorrow"')
    print('  "Write API documentation by next Friday"')
    print('  "Low priority: refactor old code"')
    print("="*80 + "\n")
    
    parser = TaskParser()
    
    try:
        while True:
            print("\nOptions:")
            print("  1. Parse single task")
            print("  2. Parse multiple tasks")
            print("  3. Test examples")
            print("  4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                print("\nEnter task description:")
                text = input("> ").strip()
                if text:
                    task = parser.parse(text)
                    print("\n" + format_task_output(task))
                    print(f"\nRaw output: {task}")
            
            elif choice == '2':
                print("\nEnter multiple tasks (one per line, press Enter twice to finish):")
                lines = []
                while True:
                    line = input().strip()
                    if not line:
                        if lines:
                            break
                        continue
                    lines.append(line)
                
                text = '\n'.join(lines)
                tasks = parse_multiple_tasks(text)
                
                print(f"\nParsed {len(tasks)} task(s):\n")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {format_task_output(task)}\n")
            
            elif choice == '3':
                examples = [
                    "Fix critical login bug - urgent, due tomorrow",
                    "Write API documentation by next Friday",
                    "Low priority: refactor old code",
                    "Setup database backup - high priority - 2026-12-31",
                    "Review pull requests - medium - this week",
                    "Update dependencies",
                    "Optimize slow database query - blocking",
                ]
                
                print("\nTesting examples:\n")
                for example in examples:
                    task = parser.parse(example)
                    print(f"Input: {example}")
                    print(f"Output: {format_task_output(task)}")
                    print()
            
            elif choice == '4':
                print("\nGoodbye!")
                break
            
            else:
                print("Invalid option. Please select 1-4.")
    
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
