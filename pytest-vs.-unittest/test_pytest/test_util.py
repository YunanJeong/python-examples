"""Unit Test용 모듈 (pytest 패키지 사용).

    - 테스트파일: 파일명에 test_ 또는 _test로 prefix,postfix가 붙은 파이썬 모듈을 테스트파일로 인식한다.
    - 테스트함수: unittest 패키지와 마찬가지로, 함수 앞에 test_가 붙으면 테스트용 함수로 인식한다.
    - $ pytest
        =>'모든 하위 디렉토리'의 '테스트 파일'에서 '테스트 함수'를 검사한다.
    - $ pytest {파일명.py}
        => 한 파일 내의 테스트 함수들을 검사한다. 이 땐, 파일명은 테스트파일 형식이 아니어도 된다.

    => 옵션 "-s": stdout 프린트 내용 콘솔 출력
    => 옵션 "-v": 좀 더 자세한 결과 출력
    @pytest.fixture(scope='fucntion'): 디폴트. 각 테스트함수에서 fixture함수를 콜할 때마다 실행됨
    @pytest.fixture(scope='module'): 여러 번 호출해도, 모듈(*.py) 당 최초 1번만 실행됨.
    @pytest.fixture(scope='session'): 여러 번 호출해도, pytest 프로그램 실행동안 최초 1번만 실행됨.
"""
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import util  # NOQA


def _insert_data(val1, val2):
    """일반함수도 기술할 수 있다. test_prefix만 없으면 된다."""
    data = {"value1": val1, "value2": val2}
    return data


@pytest.fixture(scope='module')
def setup():
    """테스트 전, 후 처리 과정.

    Returns:
        data: 테스트에 사용될 인자를 넘겨줄 수 있다.
    Note:
        yield는 return처럼 값을 반환하지만, 함수를 나가지않고 이후로도 코드를 기술할 수 있게 해준다.
        여기에선, yield 이후는 후처리 과정에 해당한다.
    """
    print('\n----------전처리(setup) ... ----------\n')
    # 인프라 셋업
    # 설정파일 셋업 등 전처리 코드
    data = _insert_data(1, 2)

    yield data
    print('\n----------후처리(teardown) ... ----------')
    # "테스트가 끝난 후" 실행된다. scope 지정에 영향받음.
    # 인프라 종료
    # 데이터 정리 등 마무리 코드


def test_sum():
    """일반적인 함수의 유닛테스트.

    Note:
        - assert: 일반적으로 유닛테스트에 사용되는 assert다. True or False 입력에 따라 Pass or Fail 판정을 보여준다.
        - assert 없이 print를 찍어봐도 된다.
    """
    print(util.sum(1, 2))
    assert util.sum(1, 2) == 3


def test_sum_with(setup):
    """전처리 설정값으로 유닛테스트.

    Args:
        setup (fixture function): 전처리함수 setup의 반환값(return or yield)

    Note:
        fixture scope 설정에 따라 setup의 재실행유무가 다르다.
    """
    assert util.sum(setup["value1"], setup["value2"]) == 3
