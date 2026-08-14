"""
Algorithm Tests for TaskFlow
Tests insertion_sort, linear_search, and binary_search implementations.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from algorithms import TaskSorter, TaskSearcher, AlgorithmCounter
from datetime import datetime


class MockTask:
    """Mock task object for testing algorithms."""
    def __init__(self, id: int, title: str, priority: str, description: str = ""):
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


class TestInsertionSort:
    """Test suite for insertion sort algorithm."""
    
    def __init__(self):
        self.sorter = TaskSorter()
        self.passed = 0
        self.failed = 0
    
    def test_basic_priority_sort(self):
        """Test basic sort by priority (high > medium > low)."""
        print("\nTest 1: Sort by priority (high > medium > low)")
        tasks = [
            MockTask(1, "Bug fix", "low"),
            MockTask(2, "Feature", "high"),
            MockTask(3, "Documentation", "medium"),
            MockTask(4, "Urgent issue", "high"),
            MockTask(5, "Minor tweak", "low"),
        ]
        
        print(f"Before: {[t.priority for t in tasks]}")
        sorted_tasks, stats = self.sorter.insertion_sort(tasks, key='priority')
        print(f"After:  {[t.priority for t in sorted_tasks]}")
        print(f"Stats: {stats}")
        
        # Verify sort order: high, high, medium, low, low
        priorities = [t.priority for t in sorted_tasks]
        priority_values = [{'high': 2, 'medium': 1, 'low': 0}[p] for p in priorities]
        is_sorted = all(priority_values[i] >= priority_values[i+1] for i in range(len(priority_values)-1))
        
        if is_sorted:
            print("✓ PASS: Tasks sorted in descending priority order")
            self.passed += 1
        else:
            print("✗ FAIL: Sort order incorrect")
            self.failed += 1
    
    def test_already_sorted(self):
        """Test sorting already sorted tasks."""
        print("\nTest 2: Already sorted tasks")
        tasks = [
            MockTask(4, "Urgent issue", "high"),
            MockTask(2, "Feature", "high"),
            MockTask(3, "Documentation", "medium"),
            MockTask(1, "Bug fix", "low"),
            MockTask(5, "Minor tweak", "low"),
        ]
        
        sorted_again, stats = self.sorter.insertion_sort(tasks, key='priority')
        print(f"Stats: {stats}")
        
        priorities = [t.priority for t in sorted_again]
        priority_values = [{'high': 2, 'medium': 1, 'low': 0}[p] for p in priorities]
        is_sorted = all(priority_values[i] >= priority_values[i+1] for i in range(len(priority_values)-1))
        
        if is_sorted:
            print("✓ PASS: Already sorted handled correctly")
            self.passed += 1
        else:
            print("✗ FAIL: Sort failed")
            self.failed += 1
    
    def test_reverse_sorted(self):
        """Test sorting reverse-sorted tasks."""
        print("\nTest 3: Reverse sorted tasks")
        tasks = [
            MockTask(5, "Minor tweak", "low"),
            MockTask(1, "Bug fix", "low"),
            MockTask(3, "Documentation", "medium"),
            MockTask(2, "Feature", "high"),
            MockTask(4, "Urgent issue", "high"),
        ]
        
        print(f"Before: {[t.priority for t in tasks]}")
        sorted_from_reverse, stats = self.sorter.insertion_sort(tasks, key='priority')
        print(f"After:  {[t.priority for t in sorted_from_reverse]}")
        print(f"Stats: {stats}")
        
        priorities = [t.priority for t in sorted_from_reverse]
        priority_values = [{'high': 2, 'medium': 1, 'low': 0}[p] for p in priorities]
        is_sorted = all(priority_values[i] >= priority_values[i+1] for i in range(len(priority_values)-1))
        
        if is_sorted:
            print("✓ PASS: Reverse sorted handled correctly")
            self.passed += 1
        else:
            print("✗ FAIL: Reverse sort failed")
            self.failed += 1
    
    def test_single_task(self):
        """Test sorting a single task."""
        print("\nTest 4: Single task")
        tasks = [MockTask(1, "Single", "medium")]
        
        sorted_tasks, stats = self.sorter.insertion_sort(tasks, key='priority')
        print(f"Stats: {stats}")
        
        if len(sorted_tasks) == 1 and sorted_tasks[0].priority == "medium":
            print("✓ PASS: Single task handled")
            self.passed += 1
        else:
            print("✗ FAIL: Single task handling failed")
            self.failed += 1
    
    def test_empty_list(self):
        """Test sorting empty list."""
        print("\nTest 5: Empty list")
        tasks = []
        
        sorted_tasks, stats = self.sorter.insertion_sort(tasks, key='priority')
        print(f"Stats: {stats}")
        
        if len(sorted_tasks) == 0:
            print("✓ PASS: Empty list handled")
            self.passed += 1
        else:
            print("✗ FAIL: Empty list handling failed")
            self.failed += 1


class TestLinearSearch:
    """Test suite for linear search algorithm."""
    
    def __init__(self):
        self.searcher = TaskSearcher()
        self.passed = 0
        self.failed = 0
    
    def test_substring_search(self):
        """Test searching for exact substring."""
        print("\nTest 1: Search for 'Write'")
        tasks = [
            MockTask(1, "Write API documentation", "high"),
            MockTask(2, "Fix login bug", "high"),
            MockTask(3, "Update user profile", "medium"),
            MockTask(4, "Design database schema", "medium"),
            MockTask(5, "Write tests", "low"),
            MockTask(6, "Optimize query performance", "low"),
        ]
        
        results, stats = self.searcher.linear_search(tasks, "Write", key='title')
        print(f"Found {len(results)} results: {[t.title for t in results]}")
        print(f"Stats: {stats}")
        
        if len(results) == 2:
            print("✓ PASS: Substring search works")
            self.passed += 1
        else:
            print(f"✗ FAIL: Expected 2 results, got {len(results)}")
            self.failed += 1
    
    def test_case_insensitive(self):
        """Test case-insensitive search."""
        print("\nTest 2: Case-insensitive search for 'api'")
        tasks = [
            MockTask(1, "Write API documentation", "high"),
            MockTask(2, "Fix login bug", "high"),
            MockTask(3, "Update user profile", "medium"),
        ]
        
        results, stats = self.searcher.linear_search(tasks, "api", key='title')
        print(f"Found {len(results)} results: {[t.title for t in results]}")
        print(f"Stats: {stats}")
        
        if len(results) == 1:
            print("✓ PASS: Case-insensitive search works")
            self.passed += 1
        else:
            print(f"✗ FAIL: Expected 1 result, got {len(results)}")
            self.failed += 1
    
    def test_no_results(self):
        """Test search with no results."""
        print("\nTest 3: Search for non-existent term 'NOTFOUND'")
        tasks = [
            MockTask(1, "Write API documentation", "high"),
            MockTask(2, "Fix login bug", "high"),
        ]
        
        results, stats = self.searcher.linear_search(tasks, "NOTFOUND", key='title')
        print(f"Found {len(results)} results")
        print(f"Stats: {stats}")
        
        if len(results) == 0:
            print("✓ PASS: No results handled correctly")
            self.passed += 1
        else:
            print(f"✗ FAIL: Expected 0 results, got {len(results)}")
            self.failed += 1
    
    def test_empty_search_term(self):
        """Test search with empty term (matches all)."""
        print("\nTest 4: Empty search term (matches all)")
        tasks = [
            MockTask(1, "Task A", "high"),
            MockTask(2, "Task B", "medium"),
            MockTask(3, "Task C", "low"),
        ]
        
        results, stats = self.searcher.linear_search(tasks, "", key='title')
        print(f"Found {len(results)} results")
        print(f"Stats: {stats}")
        
        if len(results) == len(tasks):
            print("✓ PASS: Empty search term matches all")
            self.passed += 1
        else:
            print(f"✗ FAIL: Expected {len(tasks)} results, got {len(results)}")
            self.failed += 1


class TestBinarySearch:
    """Test suite for binary search algorithm."""
    
    def __init__(self):
        self.searcher = TaskSearcher()
        self.passed = 0
        self.failed = 0
    
    def test_substring_search(self):
        """Test binary search for substring."""
        print("\nTest 1: Binary search for 'Write'")
        tasks = [
            MockTask(1, "Write API documentation", "high"),
            MockTask(2, "Fix login bug", "high"),
            MockTask(3, "Update user profile", "medium"),
            MockTask(4, "Design database schema", "medium"),
            MockTask(5, "Write tests", "low"),
            MockTask(6, "Optimize query performance", "low"),
        ]
        
        results, stats = self.searcher.binary_search(tasks, "Write", key='title')
        print(f"Found {len(results)} results: {[t.title for t in results]}")
        print(f"Stats: {stats}")
        
        if len(results) == 2:
            print("✓ PASS: Binary search substring found")
            self.passed += 1
        else:
            print(f"✗ FAIL: Expected 2 results, got {len(results)}")
            self.failed += 1
    
    def test_case_insensitive(self):
        """Test binary search case-insensitive."""
        print("\nTest 2: Case-insensitive binary search for 'api'")
        tasks = [
            MockTask(1, "Write API documentation", "high"),
            MockTask(2, "Fix login bug", "high"),
            MockTask(3, "Update user profile", "medium"),
        ]
        
        results, stats = self.searcher.binary_search(tasks, "api", key='title')
        print(f"Found {len(results)} results: {[t.title for t in results]}")
        print(f"Stats: {stats}")
        
        if len(results) == 1:
            print("✓ PASS: Case-insensitive binary search works")
            self.passed += 1
        else:
            print(f"✗ FAIL: Expected 1 result, got {len(results)}")
            self.failed += 1
    
    def test_no_results(self):
        """Test binary search with no results."""
        print("\nTest 3: Binary search for non-existent term")
        tasks = [
            MockTask(1, "Write API documentation", "high"),
            MockTask(2, "Fix login bug", "high"),
        ]
        
        results, stats = self.searcher.binary_search(tasks, "NOTFOUND", key='title')
        print(f"Found {len(results)} results")
        print(f"Stats: {stats}")
        
        if len(results) == 0:
            print("✓ PASS: No results handled")
            self.passed += 1
        else:
            print(f"✗ FAIL: Expected 0 results, got {len(results)}")
            self.failed += 1
    
    def test_comparison_with_linear(self):
        """Compare binary search with linear search results."""
        print("\nTest 4: Comparing binary vs linear search results")
        tasks = [
            MockTask(1, "Write API documentation", "high"),
            MockTask(2, "Fix login bug", "high"),
            MockTask(3, "Update user profile", "medium"),
            MockTask(4, "Design database schema", "medium"),
            MockTask(5, "Write tests", "low"),
            MockTask(6, "Optimize query performance", "low"),
        ]
        
        search_term = "query"
        linear_results, linear_stats = self.searcher.linear_search(tasks, search_term, key='title')
        binary_results, binary_stats = self.searcher.binary_search(tasks, search_term, key='title')
        
        print(f"Linear search: {len(linear_results)} results")
        print(f"Binary search: {len(binary_results)} results")
        
        # Sort both result sets for comparison
        linear_titles = sorted([t.title for t in linear_results])
        binary_titles = sorted([t.title for t in binary_results])
        
        if linear_titles == binary_titles:
            print("✓ PASS: Results match")
            self.passed += 1
        else:
            print(f"✗ FAIL: Results differ")
            print(f"  Linear: {linear_titles}")
            print(f"  Binary: {binary_titles}")
            self.failed += 1


class TestAlgorithmCounters:
    """Test algorithm operation counters."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_counter_initialization(self):
        """Test counter initialization."""
        print("\nTest 1: Counter initialization")
        counter = AlgorithmCounter()
        stats = counter.get_stats()
        
        print(f"Initial stats: {stats}")
        
        if all(v == 0 for v in stats.values()):
            print("✓ PASS: Counter initialized to zeros")
            self.passed += 1
        else:
            print("✗ FAIL: Counter not properly initialized")
            self.failed += 1
    
    def test_counter_reset(self):
        """Test counter reset."""
        print("\nTest 2: Counter reset")
        counter = AlgorithmCounter()
        counter.comparisons = 10
        counter.assignments = 5
        counter.swaps = 3
        counter.iterations = 20
        
        counter.reset()
        stats = counter.get_stats()
        
        print(f"Stats after reset: {stats}")
        
        if all(v == 0 for v in stats.values()):
            print("✓ PASS: Counter reset works")
            self.passed += 1
        else:
            print("✗ FAIL: Counter not properly reset")
            self.failed += 1


def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*80)
    print("TASKFLOW ALGORITHM TEST SUITE")
    print("="*80)
    
    # Insertion Sort Tests
    print("\n" + "="*80)
    print("INSERTION SORT TESTS")
    print("="*80)
    sort_tests = TestInsertionSort()
    sort_tests.test_basic_priority_sort()
    sort_tests.test_already_sorted()
    sort_tests.test_reverse_sorted()
    sort_tests.test_single_task()
    sort_tests.test_empty_list()
    
    # Linear Search Tests
    print("\n" + "="*80)
    print("LINEAR SEARCH TESTS")
    print("="*80)
    linear_tests = TestLinearSearch()
    linear_tests.test_substring_search()
    linear_tests.test_case_insensitive()
    linear_tests.test_no_results()
    linear_tests.test_empty_search_term()
    
    # Binary Search Tests
    print("\n" + "="*80)
    print("BINARY SEARCH TESTS")
    print("="*80)
    binary_tests = TestBinarySearch()
    binary_tests.test_substring_search()
    binary_tests.test_case_insensitive()
    binary_tests.test_no_results()
    binary_tests.test_comparison_with_linear()
    
    # Counter Tests
    print("\n" + "="*80)
    print("ALGORITHM COUNTER TESTS")
    print("="*80)
    counter_tests = TestAlgorithmCounters()
    counter_tests.test_counter_initialization()
    counter_tests.test_counter_reset()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    total_passed = (sort_tests.passed + linear_tests.passed + 
                    binary_tests.passed + counter_tests.passed)
    total_failed = (sort_tests.failed + linear_tests.failed + 
                    binary_tests.failed + counter_tests.failed)
    total_tests = total_passed + total_failed
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Pass Rate: {total_passed/total_tests*100:.1f}%\n")
    
    if total_failed == 0:
        print("✓ ALL TESTS PASSED!")
    else:
        print(f"✗ {total_failed} test(s) failed")
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
