"""Unit Test용 모듈 (unittest 패키지 사용)."""
import unittest
import util


class CustomTests(unittest.TestCase):

    def setUp(self):
        """전처리(각 테스트 공통)."""
        print('\n============== UnitTest Begins ================')

    def tearDown(self):
        """후처리(각 테스트 공통)."""
        print('============== UnitTest Ends ==================')

    def test_sum(self):
        util.sum(1+2)

if __name__ == '__main__':
    unittest.main()
