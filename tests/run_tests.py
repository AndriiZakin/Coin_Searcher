import unittest
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    loader = unittest.TestLoader()
    
    # Define the directories where your tests are
    test_dirs = ['../find_coins/tests', '../simulation/tests']
    
    # Create a test suite
    suite = unittest.TestSuite()

    # Discover tests from each directory and add them to the test suite
    for dir in test_dirs:
        suite.addTests(loader.discover(dir, pattern='test*.py'))

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Exit the script with an error code if tests failed.
    if not result.wasSuccessful():
        exit(1)