"""
Simple Python syntax and import test for TaskFlow
This script verifies that all Python files have correct syntax
"""
import py_compile
import sys
from pathlib import Path


def check_file_syntax(file_path: str) -> bool:
    """Check if a Python file has valid syntax."""
    try:
        py_compile.compile(file_path, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ SYNTAX ERROR in {file_path}:")
        print(f"  {e}")
        return False


def main():
    """Check all project Python files."""
    print("\n" + "="*80)
    print("TaskFlow Python Syntax Verification")
    print("="*80)
    
    project_root = Path(__file__).parent
    python_files = []
    
    # Find all Python files
    for py_file in project_root.rglob("*.py"):
        if "__pycache__" not in str(py_file):
            python_files.append(py_file)
    
    print(f"\nFound {len(python_files)} Python files to check:\n")
    
    passed = 0
    failed = 0
    
    for py_file in sorted(python_files):
        relative_path = py_file.relative_to(project_root)
        if check_file_syntax(str(py_file)):
            print(f"✓ {relative_path}")
            passed += 1
        else:
            print(f"✗ {relative_path}")
            failed += 1
    
    print("\n" + "="*80)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*80 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
