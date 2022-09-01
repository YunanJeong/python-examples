"""Unit Test용 모듈 (unittest 패키지 사용).

- 테스트함수: unittest.TestCase를 상속한 클래스에서 함수명에 test_라는 prefix가 붙으면 테스트함수로 인식한다.
- $ python {파일명.py}: 실행(일반 함수 제외하고, 테스트 함수들만 실행된다.)
- $ python {파일명.py} -v: 자세한 결과 출력. 각 함수의 docstring 출력.
"""
import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import util  # NOQA


def _insert_data(val1, val2):
    """테스트클래스 밖에서 일반함수를 기술할 수 있다."""
    return {"value1": val1, "value2": val2}


class MyCustomTests(unittest.TestCase):

    data = None

    def setUp(self):
        """전처리(각 테스트함수마다 실행)."""
        print('\n============== UnitTest Begins ================')
        # 인프라 셋업
        # 설정파일 셋업 등 전처리 코드
        self.data = _insert_data(1, 2)

    def tearDown(self):
        """후처리(각 테스트함수마다 실행)."""
        print('============== UnitTest Ends ==================')
        # 인프라 종료
        # 데이터 정리 등 마무리 코드

    def test_pass(self):
        """pass는 그냥 pass."""
        pass

    def test_run(self):
        """단순 실행여부만 체크."""
        util.sum(1, 2)

    def test_print(self):
        """print를 넣을 수 있다."""
        print(util.sum(1, 2))

    def test_sum(self):
        """일반적인 함수의 유닛테스트.

        Note:
            - assert: 일반적으로 유닛테스트에 사용되는 assert다. True or False 입력에 따라 Pass or Fail 판정을 보여준다.
        """
        assert util.sum(1, 2) == 3

    def test_sum_with(self):
        """전처리 설정값으로 유닛테스트."""
        assert util.sum(self.data['value1'], self.data['value2']) == 3

    def _insert_data2(val1, val2):
        """테스트클래스 안에서 일반함수를 기술할 수 있다. `test_` prefix만 없으면 된다."""
        return {"value1": val1, "value2": val2}


if __name__ == '__main__':
    unittest.main()
