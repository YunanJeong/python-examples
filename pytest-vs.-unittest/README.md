# pytest-vs.-unittest
How to conduct Unit Test

## pytest
- 보편적으로 많이쓴다.
- 파이썬 디폴트는 아니라서 설치해야 한다.
    - `$ pip install pytest`

- 테스트 파일: 파일명에 `test_` 또는 `_test`로 prefix, postfix가 붙은 파이썬 모듈을 테스트파일로 인식한다.
- 테스트 함수: 함수명에 `test_` prefix가 붙으면 테스트용 함수 (unittest 패키지와 동일한 부분)
- `$ pytest`
    -'모든 하위 디렉토리'의 '테스트 파일'에서 '테스트 함수'를 검사한다.
- `$ pytest {파일명.py}`
    - 한 파일 내의 테스트 함수들을 검사한다. 이 땐, 파일명은 테스트파일 형식이 아니어도 된다.
    - `$ pytest -s`: stdout 프린트 내용 콘솔 출력
    - `$ pytest -v`: 좀 더 자세한 결과 출력
- fixture 함수
    - fixture로 선언된 함수는 테스트 함수에서 인자로 받을 수 있다.
    - 여러 fixture를 한 테스트 함수에서 동시에 가져올 수 있으며, reusable하다.
    - fixture로 테스트시 전처리, 후처리를 구현할 수 있다.
        - `@pytest.fixture(scope='function')`: 디폴트. 각 테스트함수에서 fixture함수를 콜할 때마다 실행됨
        - `@pytest.fixture(scope='module')`: 여러 번 호출해도, 모듈(*.py) 당 최초 1번만 실행됨.
        - `@pytest.fixture(scope='session')`: 여러 번 호출해도, pytest 프로그램 실행동안 최초 1번만 실행됨.
    - 별도 모듈에 선언할 수 있다.
    - fixture 선언은 `import pytest` 가 필요하다.


## unittest
- 파이썬에 기본 탑재된 패키지다.
- 기본적으로 Class 선언이 필요해서 코드가 지저분해지고, 자바처럼 카멜표기법으로 기술되어 있다.
    - 이는 Pythonic 하지 못하다. 편의상 pytest를 쓰는게 깔끔하다.

- 테스트함수: `unittest.TestCase`를 상속한 클래스에서 함수명에 `test_`라는 prefix가 붙으면 테스트함수로 인식한다.
- `$ python {파일명.py}`: 실행(일반 함수 제외하고, 테스트 함수들만 실행된다.)
- `$ python {파일명.py} -v`: 자세한 결과 출력. 각 함수의 docstring 출력.

