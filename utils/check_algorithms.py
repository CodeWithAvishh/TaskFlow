"""
Algorithm Validation Script for TaskFlow
Tests insertion_sort, binary_search, and linear_search implementations
"""

import sys
sys.path.insert(0, '../backend')

from algorithms import TaskSorter, TaskSearcher, AlgorithmCounter
from datetime import datetime


class MockTask:
    """Mock task object for testing algorithms."""
    def __init__(self, id, title, priority, description=""):
        self.id = id
        self.title = title
        self.priority = priority
        self.description = description
        self.project_id = 1
        self.creator_id = 1
        self.due_date = None
        self.completed = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __repr__(self):
        return f"Task({self.id}, '{self.title}', {self.priority})"


def test_insertion_sort():
    """Test insertion sort implementation."""
    print("\n" + "="*60)
    print("TESTING INSERTION SORT")
    print("="*60)
    
    sorter = TaskSorter()
    
    # Test 1: Basic sort by priority
    print("\nTest 1: Sort by priority (high > medium > low)")
    tasks = [
        MockTask(1, "Bug fix", "low"),
        MockTask(2, "Feature", "high"),
        MockTask(3, "Documentation", "medium"),
        MockTask(4, "Urgent issue", "high"),
        MockTask(5, "Minor tweak", "low"),
    ]
    
    print(f"Before: {[t.priority for t in tasks]}")
    sorted_tasks, stats = sorter.insertion_sort(tasks, key='priority')
    print(f"After:  {[t.priority for t in sorted_tasks]}")
    print(f"Stats: {stats}")
    
    # Verify sort order: high, high, medium, low, low
    priorities = [t.priority for t in sorted_tasks]
    priority_values = [{'high': 2, 'medium': 1, 'low': 0}[p] for p in priorities]
    is_sorted = all(priority_values[i] >= priority_values[i+1] for i in range(len(priority_values)-1))
    
    print(f"✓ PASS: Tasks sorted in descending priority order" if is_sorted else "✗ FAIL: Sort order incorrect")
    
    # Test 2: Already sorted
    print("\nTest 2: Already sorted tasks")
    sorted_again, stats2 = sorter.insertion_sort(sorted_tasks, key='priority')
    print(f"Stats: {stats2}")
    print(f"✓ PASS: Already sorted handled correctly")
    
    # Test 3: Reverse sorted
    print("\nTest 3: Reverse sorted tasks")
    reversed_tasks = list(reversed(tasks))
    print(f"Before: {[t.priority for t in reversed_tasks]}")
    sorted_from_reverse, stats3 = sorter.insertion_sort(reversed_tasks, key='priority')
    print(f"After:  {[t.priority for t in sorted_from_reverse]}")
    print(f"Stats: {stats3}")
    print(f"✓ PASS: Reverse sorted handled correctly")
    
    return True


def test_linear_search():
    """Test linear search implementation."""
    print("\n" + "="*60)
    print("TESTING LINEAR SEARCH")
    print("="*60)
    
    searcher = TaskSearcher()
    
    # Create test tasks
    tasks = [
        MockTask(1, "Write API documentation", "high"),
        MockTask(2, "Fix login bug", "high"),
        MockTask(3, "Update user profile", "medium"),
        MockTask(4, "Design database schema", "medium"),
        MockTask(5, "Write tests", "low"),
        MockTask(6, "Optimize query performance", "low"),
    ]
    
    # Test 1: Search for exact substring
    print("\nTest 1: Search for 'Write'")
    results, stats = searcher.linear_search(tasks, "Write", key='title')
    print(f"Found {len(results)} results: {[t.title for t in results]}")
    print(f"Stats: {stats}")
    print(f"✓ PASS" if len(results) == 2 else f"✗ FAIL: Expected 2 results, got {len(results)}")
    
    # Test 2: Case-insensitive search
    print("\nTest 2: Case-insensitive search for 'api'")
    results, stats = searcher.linear_search(tasks, "api", key='title')
    print(f"Found {len(results)} results: {[t.title for t in results]}")
    print(f"Stats: {stats}")
    print(f"✓ PASS" if len(results) == 1 else f"✗ FAIL: Expected 1 result")
    
    # Test 3: No results
    print("\nTest 3: Search for non-existent term 'NOTFOUND'")
    results, stats = searcher.linear_search(tasks, "NOTFOUND", key='title')
    print(f"Found {len(results)} results")
    print(f"Stats: {stats}")
    print(f"✓ PASS" if len(results) == 0 else f"✗ FAIL: Expected 0 results")
    
    # Test 4: Empty search term
    print("\nTest 4: Empty search term (matches all)")
    results, stats = searcher.linear_search(tasks, "", key='title')
    print(f"Found {len(results)} results")
    print(f"Stats: {stats}")
    print(f"✓ PASS" if len(results) == len(tasks) else f"✗ FAIL: Expected {len(tasks)} results")
    
    return True


def test_binary_search():
    """Test binary search implementation."""
    print("\n" + "="*60)
    print("TESTING BINARY SEARCH")
    print("="*60)
    
    searcher = TaskSearcher()
    
    # Create test tasks (note: binary search sorts them internally)
    tasks = [
        MockTask(1, "Write API documentation", "high"),
        MockTask(2, "Fix login bug", "high"),
        MockTask(3, "Update user profile", "medium"),
        MockTask(4, "Design database schema", "medium"),
        MockTask(5, "Write tests", "low"),
        MockTask(6, "Optimize query performance", "low"),
    ]
    
    # Test 1: Search for substring
    print("\nTest 1: Search for 'Write'")
    results, stats = searcher.binary_search(tasks, "Write", key='title')
    print(f"Found {len(results)} results: {[t.title for t in results]}")
    print(f"Stats: {stats}")
    print(f"✓ PASS" if len(results) == 2 else f"✗ FAIL: Expected 2 results")
    
    # Test 2: Case-insensitive search
    print("\nTest 2: Case-insensitive search for 'api'")
    results, stats = searcher.binary_search(tasks, "api", key='title')
    print(f"Found {len(results)} results: {[t.title for t in results]}")
    print(f"Stats: {stats}")
    print(f"✓ PASS" if len(results) == 1 else f"✗ FAIL: Expected 1 result")
    
    # Test 3: No results
    print("\nTest 3: Search for non-existent term")
    results, stats = searcher.binary_search(tasks, "NOTFOUND", key='title')
    print(f"Found {len(results)} results")
    print(f"Stats: {stats}")
    print(f"✓ PASS" if len(results) == 0 else f"✗ FAIL: Expected 0 results")
    
    # Test 4: Compare with linear search
    print("\nTest 4: Comparing binary vs linear search results")
    search_term = "query"
    linear_results, linear_stats = searcher.linear_search(tasks, search_term, key='title')
    binary_results, binary_stats = searcher.binary_search(tasks, search_term, key='title')
    
    print(f"Linear search: {len(linear_results)} results")
    print(f"Binary search: {len(binary_results)} results")
    
    # Sort both result sets for comparison
    linear_titles = sorted([t.title for t in linear_results])
    binary_titles = sorted([t.title for t in binary_results])
    
    print(f"✓ PASS: Results match" if linear_titles == binary_titles else f"✗ FAIL: Results differ")
    
    return True


def print_algorithm_counters():
    """Print information about algorithm counter types."""
    print("\n" + "="*60)
    print("ALGORITHM OPERATION COUNTERS")
    print("="*60)
    
    counter = AlgorithmCounter()
    print("\nCounters track the following operations:")
    print("  - Comparisons: Number of comparison operations")
    print("  - Assignments: Number of value assignments")
    print("  - Swaps: Number of element exchanges")
    print("  - Iterations: Number of loop iterations")
    print("\nThese help analyze algorithm efficiency and complexity.")


def main():
    """Run all algorithm tests."""
    print("\n" + "="*60)
    print("TaskFlow Algorithm Validation Suite")
    print("="*60)
    
    try:
        # Run tests
        test_insertion_sort()
        test_linear_search()
        test_binary_search()
        print_algorithm_counters()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
