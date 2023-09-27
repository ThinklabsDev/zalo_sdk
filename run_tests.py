import unittest
from test.test_oa_request import ZaloSendRequestBody


def create_test_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader(
    ).loadTestsFromTestCase(ZaloSendRequestBody))
    return test_suite


if __name__ == "__main__":
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print()
