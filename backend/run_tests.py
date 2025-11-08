"""
Run all backend tests
"""

import subprocess
import sys
import os

def run_tests():
    """Run pytest tests"""
    print("🧪 Running Backend Tests")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run pytest
    result = subprocess.run(
        ["pytest", "-v", "--tb=short", "--cov=app", "--cov-report=term-missing"],
        capture_output=False
    )
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)


