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
