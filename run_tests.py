"""
Convenience script to run all unit tests for ControllerEmulator.
"""
import sys
import unittest


def run_tests():
    """Discover and run all tests."""
    # Discover all test files
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    print("=" * 70)
    print("  ControllerEmulator - Running Unit Tests")
    print("=" * 70)
    exit_code = run_tests()
    print("\n" + "=" * 70)
    if exit_code == 0:
        print("  [PASS] All tests passed!")
    else:
        print("  [FAIL] Some tests failed")
    print("=" * 70)
    sys.exit(exit_code)
