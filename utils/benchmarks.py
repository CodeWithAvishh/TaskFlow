"""
Performance Benchmarking Script for TaskFlow Algorithms
Benchmarks insertion_sort, linear_search, and binary_search with different input sizes
"""

import sys
sys.path.insert(0, '../backend')

import time
from algorithms import TaskSorter, TaskSearcher
from datetime import datetime
import random


class MockTask:
    """Mock task object for benchmarking."""
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
        return f"Task({self.id}, '{self.title}')"


def generate_tasks(count):
    """Generate mock tasks for benchmarking."""
    priorities = ['low', 'medium', 'high']
    titles = [
        'Fix login bug',
        'Write documentation',
        'Optimize database',
        'Update user interface',
        'Implement new feature',
        'Review pull requests',
        'Deploy to production',
        'Fix security issue',
        'Refactor code',
        'Write unit tests',
        'Update dependencies',
        'Create backup system',
        'Monitor server health',
        'Process user feedback',
        'Improve performance',
    ]
    
    tasks = []
    for i in range(count):
        title = random.choice(titles) + f" #{i}"
        priority = random.choice(priorities)
        tasks.append(MockTask(i+1, title, priority))
    
    return tasks


def benchmark_insertion_sort(sizes):
    """Benchmark insertion sort with different input sizes."""
    print("\n" + "="*80)
    print("INSERTION SORT BENCHMARK")
    print("="*80)
    print(f"\n{'Input Size':<15} {'Comparisons':<15} {'Assignments':<15} {'Time (ms)':<15}")
    print("-"*80)
    
    sorter = TaskSorter()
    results = []
    
    for size in sizes:
        # Generate random tasks
        tasks = generate_tasks(size)
        
        # Measure execution time
        start_time = time.time()
        sorted_tasks, stats = sorter.insertion_sort(tasks, key='priority')
        end_time = time.time()
        
        elapsed_ms = (end_time - start_time) * 1000
        
        print(f"{size:<15} {stats['comparisons']:<15} {stats['assignments']:<15} {elapsed_ms:<15.4f}")
        
        results.append({
            'size': size,
            'comparisons': stats['comparisons'],
            'assignments': stats['assignments'],
            'swaps': stats['swaps'],
            'iterations': stats['iterations'],
            'time_ms': elapsed_ms
        })
    
    return results


def benchmark_linear_search(sizes):
    """Benchmark linear search with different input sizes."""
    print("\n" + "="*80)
    print("LINEAR SEARCH BENCHMARK")
    print("="*80)
    print(f"\n{'Input Size':<15} {'Search Term':<20} {'Results':<10} {'Comparisons':<15} {'Time (ms)':<15}")
    print("-"*80)
    
    searcher = TaskSearcher()
    results = []
    search_term = "Fix"  # Common substring
    
    for size in sizes:
        # Generate random tasks
        tasks = generate_tasks(size)
        
        # Measure execution time
        start_time = time.time()
        found_tasks, stats = searcher.linear_search(tasks, search_term, key='title')
        end_time = time.time()
        
        elapsed_ms = (end_time - start_time) * 1000
        found_count = len(found_tasks)
        
        print(f"{size:<15} {search_term!r:<18} {found_count:<10} {stats['comparisons']:<15} {elapsed_ms:<15.4f}")
        
        results.append({
            'size': size,
            'search_term': search_term,
            'results': found_count,
            'comparisons': stats['comparisons'],
            'iterations': stats['iterations'],
            'time_ms': elapsed_ms
        })
    
    return results


def benchmark_binary_search(sizes):
    """Benchmark binary search with different input sizes."""
    print("\n" + "="*80)
    print("BINARY SEARCH BENCHMARK")
    print("="*80)
    print(f"\n{'Input Size':<15} {'Search Term':<20} {'Results':<10} {'Comparisons':<15} {'Time (ms)':<15}")
    print("-"*80)
    
    searcher = TaskSearcher()
    results = []
    search_term = "Fix"  # Common substring
    
    for size in sizes:
        # Generate random tasks
        tasks = generate_tasks(size)
        
        # Measure execution time
        start_time = time.time()
        found_tasks, stats = searcher.binary_search(tasks, search_term, key='title')
        end_time = time.time()
        
        elapsed_ms = (end_time - start_time) * 1000
        found_count = len(found_tasks)
        
        print(f"{size:<15} {search_term!r:<18} {found_count:<10} {stats['comparisons']:<15} {elapsed_ms:<15.4f}")
        
        results.append({
            'size': size,
            'search_term': search_term,
            'results': found_count,
            'comparisons': stats['comparisons'],
            'iterations': stats['iterations'],
            'time_ms': elapsed_ms
        })
    
    return results


def print_analysis(sort_results, linear_results, binary_results):
    """Print analysis and comparison of results."""
    print("\n" + "="*80)
    print("BENCHMARK ANALYSIS & COMPARISON")
    print("="*80)
    
    print("\nINSERTION SORT COMPLEXITY:")
    print("  Theoretical: O(n²) time, O(1) space")
    print("  In-place: Yes (maintains original array structure)")
    
    for result in sort_results:
        n = result['size']
        expected_comparisons = n * (n - 1) // 2  # Worst case for sorted data
        print(f"\n  Size {n}:")
        print(f"    Actual comparisons: {result['comparisons']}")
        print(f"    Expected (worst): {expected_comparisons}")
    
    print("\n" + "-"*80)
    print("\nLINEAR SEARCH COMPLEXITY:")
    print("  Theoretical: O(n) time")
    print("  Pros: Works on unsorted data")
    print("  Cons: Must check every element")
    
    for result in linear_results:
        n = result['size']
        print(f"\n  Size {n}:")
        print(f"    Comparisons: {result['comparisons']}")
        print(f"    Results found: {result['results']}")
    
    print("\n" + "-"*80)
    print("\nBINARY SEARCH COMPLEXITY:")
    print("  Theoretical: O(n log n) for sorting + O(k log n) for search")
    print("  Pros: Faster on large sorted datasets")
    print("  Cons: Requires sorted data")
    
    for result in binary_results:
        n = result['size']
        log_n = __import__('math').log2(n) if n > 0 else 0
        print(f"\n  Size {n}:")
        print(f"    Comparisons: {result['comparisons']}")
        print(f"    Results found: {result['results']}")
        print(f"    log₂(n): {log_n:.2f}")
    
    print("\n" + "-"*80)
    print("\nSEARCH ALGORITHM COMPARISON (for size 1000):")
    if len(linear_results) >= 3 and len(binary_results) >= 3:
        linear_1000 = linear_results[2]
        binary_1000 = binary_results[2]
        
        speedup = linear_1000['comparisons'] / max(binary_1000['comparisons'], 1)
        print(f"  Linear comparisons: {linear_1000['comparisons']}")
        print(f"  Binary comparisons: {binary_1000['comparisons']}")
        print(f"  Speedup ratio: {speedup:.2f}x")


def main():
    """Run all benchmarks."""
    print("\n" + "="*80)
    print("TaskFlow Algorithm Performance Benchmarking Suite")
    print("="*80)
    
    # Define input sizes
    sizes = [100, 500, 1000]
    
    try:
        # Run benchmarks
        sort_results = benchmark_insertion_sort(sizes)
        linear_results = benchmark_linear_search(sizes)
        binary_results = benchmark_binary_search(sizes)
        
        # Print analysis
        print_analysis(sort_results, linear_results, binary_results)
        
        print("\n" + "="*80)
        print("✓ BENCHMARKING COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nNote: Actual times may vary based on system load and hardware.")
        print("Run multiple times for more consistent results.")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
