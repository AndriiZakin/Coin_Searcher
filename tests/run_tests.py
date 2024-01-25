import unittest
import os
import sys

# Get the current working directory
parent_dir = os.getcwd()

# Add the parent directory to the Python path
sys.path.append(parent_dir)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    
    # Define the directories where your tests are
    test_dirs = [os.path.join(parent_dir, 'find_coins/tests'), os.path.join(parent_dir, 'simulation/tests')]
    
    # Create a test suite
    suite = unittest.TestSuite()

    # Discover tests from each directory and add them to the test suite
    for dir in test_dirs:
        suite.addTests(loader.discover(dir))

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Exit the script with an error code if tests failed.
    if not result.wasSuccessful():
        exit(1)