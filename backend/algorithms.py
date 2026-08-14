"""
Algorithms module for TaskFlow.
Includes insertion_sort, binary_search, and linear_search with operation counting.
"""


class AlgorithmCounter:
    """Wrapper to count operations during algorithm execution."""
    
    def __init__(self):
        self.comparisons = 0
        self.assignments = 0
        self.swaps = 0
        self.iterations = 0
    
    def reset(self):
        """Reset all counters."""
        self.comparisons = 0
        self.assignments = 0
        self.swaps = 0
        self.iterations = 0
    
    def get_stats(self):
        """Return statistics dictionary."""
        return {
            "comparisons": self.comparisons,
            "assignments": self.assignments,
            "swaps": self.swaps,
            "iterations": self.iterations
        }


class TaskSorter:
    """Task sorting algorithms with operation counting."""
    
    def __init__(self):
        self.counter = AlgorithmCounter()
    
    def insertion_sort(self, tasks, key='priority'):
        """
        Insertion sort - in-place sorting algorithm.
        Sorts tasks by the specified key (priority, title, etc.).
        
        Priority order: high (2) > medium (1) > low (0)
        
        Args:
            tasks: List of tasks to sort
            key: Attribute name to sort by (default: 'priority')
        
        Returns:
            Sorted list and operation statistics
        """
        self.counter.reset()
        
        # Define priority mapping
        priority_map = {'low': 0, 'medium': 1, 'high': 2}
        
        # Work with a copy to maintain in-place semantics
        arr = list(tasks)
        n = len(arr)
        
        for i in range(1, n):
            self.counter.iterations += 1
            key_task = arr[i]
            self.counter.assignments += 1
            
            j = i - 1
            
            # Get sort values
            if key == 'priority':
                key_val = priority_map.get(key_task.priority, 1)
            else:
                key_val = getattr(key_task, key, '')
            
            while j >= 0:
                self.counter.comparisons += 1
                self.counter.iterations += 1
                
                if key == 'priority':
                    j_val = priority_map.get(getattr(arr[j], key, 'medium'), 1)
                else:
                    j_val = getattr(arr[j], key, '')
                
                if j_val <= key_val:
                    break
                
                arr[j + 1] = arr[j]
                self.counter.assignments += 1
                self.counter.swaps += 1
                j -= 1
            
            arr[j + 1] = key_task
            self.counter.assignments += 1
        
        return arr, self.counter.get_stats()


class TaskSearcher:
    """Task search algorithms with operation counting."""
    
    def __init__(self):
        self.counter = AlgorithmCounter()
    
    def linear_search(self, tasks, search_term, key='title'):
        """
        Linear search - sequential search through all tasks.
        
        Args:
            tasks: List of tasks to search
            search_term: String to search for
            key: Attribute name to search in (default: 'title')
        
        Returns:
            List of matching tasks and operation statistics
        """
        self.counter.reset()
        results = []
        search_term_lower = search_term.lower()
        
        for i, task in enumerate(tasks):
            self.counter.iterations += 1
            self.counter.comparisons += 1
            
            task_value = str(getattr(task, key, '')).lower()
            
            if search_term_lower in task_value:
                results.append(task)
                self.counter.assignments += 1
        
        return results, self.counter.get_stats()
    
    def binary_search(self, tasks, search_term, key='title'):
        """
        Binary search for substring matching on sorted data.
        
        NOTE: This is NOT a traditional binary search for exact values.
        This performs substring matching on alphabetically sorted data.
        It uses binary search to navigate the sorted array and find items
        containing the search term, then recursively explores both sides.
        
        This approach is useful for demonstrating:
        - Sorting overhead (O(n log n))
        - Binary search navigation (log n comparisons per branch)
        - Substring matching across sorted results
        
        Total complexity: O(n log n) for sorting + O(n) for substring matching
        
        Args:
            tasks: List of tasks to search
            search_term: String to search for (case-insensitive)
            key: Attribute name to search in (default: 'title')
        
        Returns:
            List of matching tasks and operation statistics
        """
        self.counter.reset()
        
        # Sorting step - O(n log n)
        sorted_tasks = sorted(tasks, key=lambda t: str(getattr(t, key, '')).lower())
        
        search_term_lower = search_term.lower()
        results = []
        
        def binary_search_helper(arr, target, left, right):
            """
            Helper function using binary search navigation to explore sorted array.
            When a match is found, explores both left and right sides recursively
            to find all occurrences of the substring.
            """
            if left > right:
                self.counter.comparisons += 1
                return
            
            mid = (left + right) // 2
            self.counter.iterations += 1
            self.counter.comparisons += 1
            
            mid_value = str(getattr(arr[mid], key, '')).lower()
            
            if target in mid_value:
                # Found a match - record it
                results.append(arr[mid])
                self.counter.assignments += 1
                
                # Search left side for more matches
                binary_search_helper(arr, target, left, mid - 1)
                # Search right side for more matches
                binary_search_helper(arr, target, mid + 1, right)
            elif target < mid_value:
                # Continue searching in left half
                binary_search_helper(arr, target, left, mid - 1)
            else:
                # Continue searching in right half
                binary_search_helper(arr, target, mid + 1, right)
        
        if sorted_tasks:
            binary_search_helper(sorted_tasks, search_term_lower, 0, len(sorted_tasks) - 1)
        
        return results, self.counter.get_stats()


# Global instances
task_sorter = TaskSorter()
task_searcher = TaskSearcher()


def sort_tasks_by_priority(tasks):
    """
    Sort tasks by priority using insertion sort.
    Returns sorted tasks and operation statistics.
    """
    return task_sorter.insertion_sort(tasks, key='priority')


def search_tasks_linear(tasks, search_term):
    """
    Search tasks using linear search.
    Returns matching tasks and operation statistics.
    """
    return task_searcher.linear_search(tasks, search_term, key='title')


def search_tasks_binary(tasks, search_term):
    """
    Search tasks using binary search.
    Returns matching tasks and operation statistics.
    """
    return task_searcher.binary_search(tasks, search_term, key='title')
