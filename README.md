# python-examples

python example, skill, and practice

## 참고: python에서 정확한 스코프 용어

- 패키지: 한 디렉토리안에 있는 py파일 모음. 일반적으로 `import xxx` 하는게 이것. PyPi에서 다운받을 수 있는 라이브러리 1개에 해당
- 모듈: py파일 1개
- 모듈레벨 변수: 파이썬에서 전역변수
- 클래스 변수:
  - 객체지향으로 기술시, Class 안쪽, Method 바깥쪽에 선언된 변수.
  - 블로그 등에서 `클래스 변수와 모듈레벨 변수를 둘 다 전역변수라고 칭하여 혼용하는 경우가 종종 있는데, 엄밀히 말하면 모듈레벨 변수만 전역변수라고 하는게 맞다. 헷갈리지 말자`
- 인스턴스 변수: self키워드와 함께 선언된 변수, 인스턴스 생성시 값이 할당되는 변수
- 지역 변수: 메소드 안에서 선언된 변수

### 파이썬 변수 스코프 유형 예

```py
module_var = "모듈 레벨 변수(전역 변수)"

class MyClass:
    class_var = "클래스 변수"

    def __init__(self, value):
        # 인스턴스 변수
        self.instance_var = value

    def method(self):
        local_var: "지역 변수"
        print("모듈 레벨 변수:", module_var)
        print("클래스 변수:", MyClass.class_var)
        print("인스턴스 변수:", self.instance_var)
        print("지역 변수:", local_var)

obj = MyClass("인스턴스 변수")  # 인스턴스 생성
obj.method()
```

### 출력

```sh
모듈 레벨 변수: 모듈 레벨 변수(전역 변수)
클래스 변수: 클래스 변수
인스턴스 변수: 인스턴스 변수
지역 변수: 지역 변수
```

## 가상환경 비교

- 결론: 어지간하면 venv 쓰면된다.

### venv

- 용도: 프로젝트 별 독립된 가상환경 생성&관리
- 특징:
  - python 3.3 이후 표준
  - 일반적으로 추가설치 불필요
  - python 프로젝트 공유시 배포방법(REAMDE.md 등)으로 가장 널리 쓰임
  - virtualenv의 경량화된 모듈
- 용법:
  - 프로젝트 루트경로에 `venv` 디렉토리를 생성하고, 그 안에 가상환경 관련파일을 모두 저장하는 방식
  - 디렉토리명, 위치는 변경가능하지만 위 방식이 가장 보편적
  - 단순하지만 직관적이라 관리 쉬움
- 단점:
  - python 버전 별 가상환경 구축 불가

```sh
# 가상 환경 생성  # 보통은 <env_name>는 venv,myenv 정도로 씀
python -m venv <env_name>

# 가상 환경 활성화
# Windows
<env_name>\Scripts\activate
# macOS/Linux
source <env_name>/bin/activate

# 가상 환경 비활성화
deactivate

# 가상 환경 삭제 (그냥 디렉토리 삭제해버리면됨)
rm -rf <env_name>

# 가상 환경 내에서 패키지(모듈) 설치 (가상환경 활성화 후 사용할 것)
pip install <package_name>

# 가상 환경 내에서 설치된 패키지 목록 확인
pip list
```

### virtualenv

- 용도: 프로젝트 별 독립된 가상환경 생성&관리
- 특징:
  - venv보다 기능 많음
  - venv와 호환됨. 명령어도 거의 비슷.
  - python 2,3 버전의 패키지에 모두 호환 가능
  - Cli에서 전체 가상환경 목록을 제어가능(조회&생성&활성화)
- 단점:
  - python 버전 별 가상환경 구축 불가
  - 별도 설치 필요

```sh
# 현재경로에 'myenv' 가상환경 생성
virtualenv myenv
```

### pyenv

- 용도: python 버전 별 가상환경 관리
- 특징:
  - 모듈말고, `언어 버전을 바꿔야 할 때` 사용
  - 프로젝트 별 패키지환경을 관리하기 위해 virtualenv, venv와 함께 사용됨
- 용법:
  - 현재 세션에서 특정버전 python을 활성화하는 방식
- 단점:
  - `활성화시 CLI가 느려지는데, 생각보다 많이 답답`하므로 필요할 때만 설치하자
  - 그래도 python 설치속도는 anaconda 보다 빠른 듯? python 버전 관리에는 대체제가 딱히 별로 없다.

### pyenv-virtualenv

- pyenv와 virtualenv를 결합한 도구
- pyenv에서 virutalenv를 서브모듈처럼 사용
- virtualenv를 설치하는 것과는 다른 것이니 주의
- 기능 많고 좋긴 한데, 다소 난해할 수 있으니 필요할 때만 설치&활성화 하자

### pipx

- 용도: 가상환경 없이 python을 전역환경에서 쓰고 싶을 때 사용
- 특징:
  - `pip install`처럼 `pipx install`로 설치가능
  - pipx로 설치된 패키지는 패키지마다 독립된 가상환경에 설치됨
  - 하지만 각 패키지는 전역처럼 호출가능
- 굳이 이런 방식을 쓰는 이유
  - python을 전역 환경에서 사용하는 것은 비권장
  - 전역 pip로 패키지 설치시 OS 및 기타 시스템 환경과 충돌 가능성 있음
  - python 활용도가 증가하면서 이런 문제가 많아졌고, python 3.11 부터는 전역에서 pip install시 에러or경고 메시지 출력
- 단점
  - -r 옵션 미지원. requirements.txt로 패키지 일괄 설치 불가.
- 설치&사용 방법
```
# pipx는 내부적으로 pip를 활용하기때문에 사전설치 필요
# 둘 다 다음처럼 전역에 설치하면 됨
sudo apt install -y pip pipx
```
