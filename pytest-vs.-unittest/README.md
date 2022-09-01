# pytest-vs.-unittest
How to conduct Unit Test

## pytest
### 개요
- 보편적으로 많이 쓴다.
- 파이썬 디폴트는 아니라서 설치해야 한다.
    - `$ pip install pytest`



### 실행
- 테스트 파일: 파일명 앞뒤로 `test_` 또는 `_test`가 붙은 파이썬 모듈
- 테스트 함수: 함수명 앞에 `test_` 가 붙으면 테스트용 함수로 인식 (unittest 패키지와 동일한 부분)
- `$ pytest`
    - '모든 하위 디렉토리'의 '테스트 파일'에서 '테스트 함수'를 검증
- `$ pytest {파일명.py}`
    - 한 파일 내의 테스트 함수들을 검증한다. 이 땐, 파일명은 테스트파일 형식이 아니어도 된다.
- `$ pytest -s`
    - stdout 프린트 내용 콘솔 출력
- `$ pytest -v`
    - 좀 더 자세한 결과 출력


### fixture function
- fixture 함수는 테스트 함수의 인자가 될 수 있다.
    - 한 테스트 함수에서 여러 fixture 함수를 동시에 취할 수 있고, reusable하다.
- fixture로 테스트시 전, 후처리를 구현 가능
    - `@pytest.fixture(scope='function')`: 디폴트. 각 테스트함수에서 fixture함수를 콜할 때마다 실행됨
    - `@pytest.fixture(scope='module')`: 여러 번 호출해도, 모듈(*.py) 당 최초 1번만 실행됨.
    - `@pytest.fixture(scope='session')`: 여러 번 호출해도, pytest 프로그램 실행동안 최초 1번만 실행됨.
- fixture들을 별도 모듈로 선언해놓고 쓸 수 있다.
- fixture 선언은 `import pytest` 가 필요


## unittest
### 개요
- 파이썬 기본 탑재 패키지
- Class 선언이 필요해서 코드가 지저분해지고, 자바처럼 카멜표기법으로 기술되어 있다.
    - 전반적으로 Pythonic 하지 않다. pytest를 쓰는게 깔끔하다.



### 실행
- 테스트 함수
    - `unittest.TestCase`를 상속한 클래스 내에서, 함수명에 `test_`라는 prefix가 붙으면 테스트 함수로 인식
- `$ python {파일명.py}`
    - 지정파일에서 테스트 함수를 검증
- `$ python {파일명.py} -v`
    - 자세한 결과 출력. 각 함수의 docstring도 출력.

