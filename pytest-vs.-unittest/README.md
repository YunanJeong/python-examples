# pytest-vs.-unittest
How to conduct Unit Test

## unittest
- 파이썬에 기본 탑재된 패키지다.
- 기본적으로 Class 선언이 필요해서 코드가 지저분해지고, 자바처럼 카멜표기법으로 기술되어 있다.
    - 이는 Pythonic 하지 못하다. 편의상 pytest를 쓰는게 깔끔하다.

## pytest
- 보편적으로 많이쓴다.
- 파이썬 디폴트는 아니라서 설치해야 한다.

- 테스트 파일: 파일명에 `test_` 또는 `_test`로 prefix, postfix가 붙은 파이썬 모듈을 테스트파일로 인식한다.
- 테스트 함수: 함수명에 `test_` prefix가 붙으면 테스트용 함수 (unittest 패키지와 동일한 부분)
- `$ pytest`
    -'모든 하위 디렉토리'의 '테스트 파일'에서 '테스트 함수'를 검사한다.
- `$ pytest {파일명.py}`
    - 한 파일 내의 테스트 함수들을 검사한다. 이 땐, 파일명은 테스트파일 형식이 아니어도 된다.
    - `pytest -s`: stdout 프린트 내용 콘솔 출력
    - `pytest -v`: 좀 더 자세한 결과 출력
