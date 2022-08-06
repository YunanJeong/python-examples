# pyodbc-vs.-pymssql
- How to establish db connection for python.
- Difference between pyodbc and pymssql when using SQL Server
- Practice

# pymssql
- `$ pip install pymmssql` 만으로 간편히 다운로드 받을 수 있다.
    - 즉, 자동화에 유리하다.
- 패키지 자체가 deprecated라서 장기 시스템에 사용이 꺼려진다.

# pyodbc
- 보편적인 DB 연결에 사용할 수 있다.
- 파이썬 패키지 설치전, 데비안 패키지 설치(sudo apt install)가 필요하다.
- 데비안 패키지 설치 전, 별도 odbc driver를 설치해야한다.(이건 자동설치도 아니다.)


