"""
Performance Benchmarking Suite for TaskFlow Algorithms
Benchmarks insertion_sort, linear_search, and binary_search with different input sizes.
"""

import sys
from pathlib import Path
import time
import random
import math

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from algorithms import TaskSorter, TaskSearcher
from datetime import datetime


class MockTask:
    """Mock task object for benchmarking."""
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
        return f"Task({self.id}, '{self.title}')"


def generate_tasks(count: int) -> list:
    """
    Generate mock tasks for benchmarking.
    
    Args:
        count: Number of tasks to generate
        
    Returns:
        List of MockTask objects
    """
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


def benchmark_insertion_sort(sizes: list) -> list:
    """
    Benchmark insertion sort with different input sizes.
    
    Args:
        sizes: List of input sizes to benchmark
        
    Returns:
        List of benchmark results
    """
    print("\n" + "="*100)
    print("INSERTION SORT BENCHMARK")
    print("="*100)
    print(f"\n{'Input Size':<15} {'Comparisons':<15} {'Assignments':<15} {'Swaps':<15} {'Time (ms)':<15}")
    print("-"*100)
    
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
        
        print(f"{size:<15} {stats['comparisons']:<15} {stats['assignments']:<15} {stats['swaps']:<15} {elapsed_ms:<15.4f}")
        
        results.append({
            'size': size,
            'comparisons': stats['comparisons'],
            'assignments': stats['assignments'],
            'swaps': stats['swaps'],
            'iterations': stats['iterations'],
            'time_ms': elapsed_ms
        })
    
    return results


def benchmark_linear_search(sizes: list) -> list:
    """
    Benchmark linear search with different input sizes.
    
    Args:
        sizes: List of input sizes to benchmark
        
    Returns:
        List of benchmark results
    """
    print("\n" + "="*100)
    print("LINEAR SEARCH BENCHMARK")
    print("="*100)
    print(f"\n{'Input Size':<15} {'Search Term':<20} {'Results Found':<15} {'Comparisons':<15} {'Time (ms)':<15}")
    print("-"*100)
    
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
        
        print(f"{size:<15} '{search_term}':{17} {found_count:<15} {stats['comparisons']:<15} {elapsed_ms:<15.4f}")
        
        results.append({
            'size': size,
            'search_term': search_term,
            'results': found_count,
            'comparisons': stats['comparisons'],
            'iterations': stats['iterations'],
            'time_ms': elapsed_ms
        })
    
    return results


def benchmark_binary_search(sizes: list) -> list:
    """
    Benchmark binary search with different input sizes.
    
    Note: Binary search in this implementation performs substring matching on sorted data.
    
    Args:
        sizes: List of input sizes to benchmark
        
    Returns:
        List of benchmark results
    """
    print("\n" + "="*100)
    print("BINARY SEARCH BENCHMARK (Substring matching on sorted data)")
    print("="*100)
    print(f"\n{'Input Size':<15} {'Search Term':<20} {'Results Found':<15} {'Comparisons':<15} {'Time (ms)':<15}")
    print("-"*100)
    
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
        
        print(f"{size:<15} '{search_term}':{17} {found_count:<15} {stats['comparisons']:<15} {elapsed_ms:<15.4f}")
        
        results.append({
            'size': size,
            'search_term': search_term,
            'results': found_count,
            'comparisons': stats['comparisons'],
            'iterations': stats['iterations'],
            'time_ms': elapsed_ms
        })
    
    return results


def print_complexity_analysis(sort_results: list, linear_results: list, binary_results: list):
    """
    Print complexity analysis and comparison of results.
    
    Args:
        sort_results: Insertion sort benchmark results
        linear_results: Linear search benchmark results
        binary_results: Binary search benchmark results
    """
    print("\n" + "="*100)
    print("COMPLEXITY ANALYSIS & RESULTS COMPARISON")
    print("="*100)
    
    print("\n" + "─"*100)
    print("INSERTION SORT")
    print("─"*100)
    print("Time Complexity: O(n²)")
    print("Space Complexity: O(1) - in-place sorting")
    print("\nPerformance Analysis:")
    
    for result in sort_results:
        n = result['size']
        # For random data, average case is O(n²/4) comparisons
        expected_avg = n * (n - 1) // 4
        expected_worst = n * (n - 1) // 2
        
        print(f"\n  n = {n}:")
        print(f"    Actual comparisons:     {result['comparisons']}")
        print(f"    Expected average:       ~{expected_avg}")
        print(f"    Expected worst-case:    {expected_worst}")
        print(f"    Execution time:         {result['time_ms']:.4f} ms")
    
    print("\n" + "─"*100)
    print("LINEAR SEARCH")
    print("─"*100)
    print("Time Complexity: O(n)")
    print("Space Complexity: O(k) where k is number of results")
    print("\nAdvantages:")
    print("  • Works on unsorted data")
    print("  • Simple to implement")
    print("  • Cache-friendly for small datasets")
    print("\nPerformance Analysis:")
    
    for result in linear_results:
        n = result['size']
        print(f"\n  n = {n}:")
        print(f"    Comparisons:      {result['comparisons']}")
        print(f"    Results found:    {result['results']}")
        print(f"    Execution time:   {result['time_ms']:.4f} ms")
    
    print("\n" + "─"*100)
    print("BINARY SEARCH (Substring matching on sorted data)")
    print("─"*100)
    print("Time Complexity: O(n log n) for sorting + O(n) for substring search")
    print("Space Complexity: O(n) for sorted copy + O(k) for results")
    print("\nNOTE: This implementation sorts before searching and performs")
    print("substring matching, which is NOT a traditional binary search.")
    print("\nPerformance Analysis:")
    
    for result in binary_results:
        n = result['size']
        log_n = math.log2(n) if n > 0 else 0
        
        print(f"\n  n = {n}:")
        print(f"    Comparisons:      {result['comparisons']}")
        print(f"    Results found:    {result['results']}")
        print(f"    Execution time:   {result['time_ms']:.4f} ms")
        print(f"    log₂(n):          {log_n:.2f}")
    
    print("\n" + "─"*100)
    print("SEARCH ALGORITHM COMPARISON")
    print("─"*100)
    
    if len(linear_results) >= 3 and len(binary_results) >= 3:
        # Compare at size 1000
        linear_1000 = next((r for r in linear_results if r['size'] == 1000), None)
        binary_1000 = next((r for r in binary_results if r['size'] == 1000), None)
        
        if linear_1000 and binary_1000:
            print("\nComparison at n = 1000:")
            print(f"  Linear Search Comparisons:  {linear_1000['comparisons']}")
            print(f"  Binary Search Comparisons:  {binary_1000['comparisons']}")
            
            comparison_ratio = linear_1000['comparisons'] / max(binary_1000['comparisons'], 1)
            print(f"  Ratio (Linear / Binary):    {comparison_ratio:.2f}x")
            
            print(f"\n  Linear Search Time:   {linear_1000['time_ms']:.4f} ms")
            print(f"  Binary Search Time:   {binary_1000['time_ms']:.4f} ms")
            
            time_ratio = linear_1000['time_ms'] / max(binary_1000['time_ms'], 0.0001)
            print(f"  Time Ratio (Linear / Binary): {time_ratio:.2f}x")
            
            print("\nKey Observation:")
            print("  Binary search sorts the data (O(n log n)) before searching.")
            print("  For a single search, linear search is typically faster.")
            print("  For multiple searches, binary search setup cost amortizes.")
    
    print("\n" + "─"*100)
    print("RECOMMENDATIONS")
    print("─"*100)
    print("\n1. Use INSERTION SORT for:")
    print("   • Small datasets (< 100 items)")
    print("   • Nearly sorted data")
    print("   • Online sorting (items arrive gradually)")
    
    print("\n2. Use LINEAR SEARCH for:")
    print("   • Unsorted data")
    print("   • Single search operation")
    print("   • Small to medium datasets")
    
    print("\n3. Use BINARY SEARCH for:")
    print("   • Multiple searches on same sorted data")
    print("   • Large sorted datasets")
    print("   • When search cost must be minimized")


def main():
    """Run all benchmarks."""
    print("\n" + "="*100)
    print("TaskFlow Algorithm Performance Benchmarking Suite")
    print("="*100)
    print(f"\nPython: {sys.version.split()[0]}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Define input sizes
    sizes = [100, 500, 1000]
    
    try:
        # Run benchmarks
        print("\nGenerating test data and running benchmarks...")
        sort_results = benchmark_insertion_sort(sizes)
        linear_results = benchmark_linear_search(sizes)
        binary_results = benchmark_binary_search(sizes)
        
        # Print analysis
        print_complexity_analysis(sort_results, linear_results, binary_results)
        
        print("\n" + "="*100)
        print("✓ BENCHMARKING COMPLETED SUCCESSFULLY")
        print("="*100)
        print("\nNote: Actual times may vary based on system load and hardware.")
        print("Run multiple times for more consistent results.")
        print("="*100 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
