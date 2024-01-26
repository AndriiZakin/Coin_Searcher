import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    
    # Discover tests in the current directory
    suite = loader.discover('.', pattern='test*.py')

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Exit the script with an error code if tests failed.
    if not result.wasSuccessful():
        exit(1)