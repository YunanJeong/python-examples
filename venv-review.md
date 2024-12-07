# 파이썬 개발환경 구축 및 가상환경 툴 비교

- 결론: 널리 배포할 땐 venv가 가장 무난, 개인 개발환경은 pyenv가 아주 편함

## venv

- 용도: 프로젝트 별 독립된 가상환경 생성&관리
- 특징:
  - python 3.3 이후 표준
  - 일반적으로 추가설치 불필요
  - python 프로젝트 공유시 배포방법(REAMDE.md 등 설명 포함)으로 가장 널리 쓰임
  - virtualenv의 경량화된 모듈
- 용법:
  - **프로젝트 루트경로에 `venv` 디렉토리를 생성하고, 그 안에 가상환경 관련파일을 모두 저장**하는 방식
  - 디렉토리명, 위치는 변경가능하지만 위 방식이 가장 보편적
  - **단순하지만 직관적**이라 관리 쉬움
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

## virtualenv

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

## pyenv

`python 버전 별` 가상환경 관리

### 특징

- 모듈말고, `언어 버전을 바꿔야 할 때` 사용
- 프로젝트 별 패키지환경을 관리하기 위해 virtualenv, venv와 함께 사용됨
- 최근엔 설치도 너무 쉬워지고 CLI 느려지는 이슈도 고쳐져셔 너무 좋음
  - 설치: github.com/pyenv
- 네이티브 설치된 파이썬과 속도차이도 없으므로 파이썬 특정 버전만 설치한다해도 pyenv를 쓰는게 훨씬 편함

### 용법

- 현재 세션에서 특정버전 python을 활성화하는 방식
- default 환경설정 가능, 특정 디렉토리 진입시 특정 환경으로 자동 선택가능

### 단점

- ~~활성화시 CLI가 느려지는데, 생각보다 많이 답답~~
- pyenv 2.4 버전대부터 해당 이슈 개선됨
- 그래도 python 설치속도는 anaconda 보다 빠른 듯? python 버전 관리에는 대체제가 딱히 별로 없다.

### pyenv-virtualenv

- pyenv로 파이썬 버전 뿐 아니라 모듈까지 포함해서 총체적으로 개발환경을 관리하려는 것
- `pyenv virtualenv`와 같이 서브커맨드로 사용
- 최근엔 `pyenv 설치시 포함`되며 사실상 pyenv와 구분하는 의미가 없음
- virtualenv를 단독 설치본과는 다르니 헷갈리지 말자

## pipx

python을 가상환경 없이 전역환경에서 쓰고 싶을 때 사용

### 특징

- pip install처럼 `pipx install`로 파이썬 패키지 설치가능
- `pipx로 설치된 각 패키지는 독립된 가상환경에 설치`됨
- but, `각 패키지는 전역처럼 호출`가능
- 굳이 이런 방식을 쓰는 이유
  - python의 전역 환경 사용은 비권장사항이지만, 전역으로 간편히 쓰고싶은 경우가 있음
  - 전역 pip로 패키지 설치시 OS 및 기타 시스템 환경과 충돌 가능성 있음
  - python 활용도가 증가하면서 이런 문제가 많아졌고, python 3.11 부터는 전역에서 pip install시 에러or경고 메시지 출력

### 단점

- -r 옵션 미지원. requirements.txt로 다수 패키지 일괄 설치 미지원
- pipx install시 자동설치된 dependency 외에 세부적인 버전 조정이 힘들 수 있음
- pipx로 추가 dependency를 설치하더라도 별도 격리되기 때문
- `pipx로 설치된 패키지 간 참조불가`. 전역에서만 모든 패키지를 호출가능

### 설치&사용 방법

```sh
# pipx는 내부적으로 pip를 활용하기때문에 사전설치 필요
# 둘 다 다음처럼 전역에 설치하면 됨
sudo apt install -y pip pipx
```

## Conda(+Anaconda, Miniconda)

- **오픈 소스 패키지 관리 및 가상환경 관리 도구**
- Python뿐만 아니라 다른 언어(R, Ruby 등)도 지원
- Anaconda, Miniconda 등은 일종의 배포판 같은 것으로 conda 및 기타 보편적인 데이터 패키지가 함께 설치되어 있음
- 데이터 사이언스, ML 쪽에 특화된 경향

### 단점

- 너무 무겁다.
- 일반적인 파이썬 프로젝트들을 함께 관리하기엔 너무 무겁고 보편성이 떨어진다.
  - 가상환경 하나 생성하는데 한세월이다.
  - 버전 안맞으면 새로 설정해서 또 기다려야 된다...
  - 파이썬이면 스크립트 뚝딱 짜서 즉시 실행하는 맛도 있어야 하는데 그게 안됨
- conda에 특화된 작업, conda로만 주로 배포되는 패키지를 설치해야 할 때 사용하는게 좋음

### 사용법

```bash
# 가상환경 생성
conda create -n myenv python=3.10
conda activate myenv

# 패키지 설치
conda install numpy pandas