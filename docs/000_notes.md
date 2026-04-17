### 고민들
1. 어디 파일에 만들지??
2. 파일을 몇개를 만들지??
3. 3 tier 아키텍쳐 구축 방법

### DB 테이블
이름 : Post 
#### Post 안에는 뭐가 있어야 하는 것
- 게시글 번호   -> id         Int 숫자 (1씩 자동으로 증가하는 숫자)
- 게시글 제목    -> title         Str 문자 (숫자,영어, 특수문자 등)
- 게시글 내용    -> content      Str 문자 (숫자,영어, 특수문자 등)
- 작성자       -> writer       Int 숫자  
- 시간         -> created_at    Date 타입 (날짜타입)
- 수정시간    -> updated_at    Date 타입 (날짜타입)

#### 어떤걸 해야할지 고민 (시나리오 / 정책들 고민)
- 로그인한 유저만 글을 쓸수있다. 
- 내 게시글은 나만 수정/삭제 할 수 있다.
- 모든 게시글은 모두가 볼수있다. (단 로그인을 했을때만 조회 가능)

#### 게시판의 CRUD
Create: 게시글 작성
Read: 게시글 조회 / 검색
Upadate: 게시글 수정
Delete: 게시글 삭제

## 3/29 일 - 궁금한 것들 정리

### 구조
```
syj/
├── app/                       # 소스 코드 폴더
│   ├── __init__.py          
│   ├── main.py                # FastAPI 앱 시작점 
│   ├── database.py            # 데이터베이스 연결 설정
│   ├── auth/                  # 인증 도메인
│   │   ├── __init__.py
│   │   ├── service.py         # 비밀번호 해싱, JWT 토큰 생성/검증
│   │   ├── router.py          # 회원가입, 로그인 API
│   │   └── schema.py          # 로그인 요청/응답 형식
│   ├── user/                  # 유저 도메인
│   │   ├── __init__.py
│   │   ├── model.py           # DB 테이블 정의
│   │   ├── schema.py          # API 입출력 데이터 형식 (DTO)
│   │   ├── repository.py      # DB 접근 (조회, 저장, 삭제)
│   │   ├── service.py         # 비즈니스 로직 (검증, 판단)
│   │   └── router.py          # API 엔드포인트
│   └── post/                  # 게시글 도메인
│       ├── __init__.py
│       ├── model.py
│       ├── schema.py
│       ├── repository.py
│       ├── service.py
│       └── router.py
├── docs/                      # 수업 문서
├── requirements.txt           # 필요한 패키지 목록
└── venv/                      # 가상환경 (직접 수정하지 않음)

```

#### post / user / auth가 같은 계층인 이유??
계층이 아니라 도메인을 기준으로 나눈 것임
도메인(Domain): 서비스에서 의미있는 기능 단위
- user: 사용자 관리
- auth: 로그인/인증
- post: 게시글

#### user를 가장 많이 쓰고 기반이 되는 것이니깐 상위 폴더에 둬야하지 않을까??
그렇게 생각한 이유는 
- post는 작성자가 누구인지 알아야 해서 user를 참조
- auth도 로그인한 사용자를 확인하려고 user를 참조

하지만 지금 사용하는 구조는 상속 및 포함 관계가 아니라 기능별로 묶음.

```
app/
 ├── user/
 │   └── post/
 │   └── auth/
```
이러면 post와 auth 둘다 user의 하위 기능처럼 

하지만 실제로는 
- user: 사용자 관리
- auth: 로그인/인증
- post: 게시글
=> 서로 다른 관심사
-> post가 user를 사용하더라도 post가 user의 일부는 아님.

각각은 기능은 독립적이고 필요할 때 user의 정보를 사용하는 것일 뿐

### __pycache__ 가 멀까??
파이썬이 자동으로 만드는 캐시 폴더

#### 생기는 이유?
파이썬은 실행 속도를 빠르게 하려고 .py 파일을 미리 컴파일해서 저장해둠
```
user/
 ├── service.py
 └── __pycache__/
      └── service.cpython-311.pyc
```
.pyc 파일이 바로 컴파일된 결과(bytecode)
- .py: 우리가 작성한 코드
- .pyc: 파이썬이 빠르게 실행하려고 만든 중간 결과
- pycache: 그걸 저장하는 폴더

#### 깃허브에 올려도 됨?
ㄴㄴ
이유
- 컴퓨터마다 다름
- 필요 없는 파일
- 충돌만 생김

.gitignore 파일 작성 규칙
- '#'로 시작하는 라인은 무시한다.
- 표준 Glob 패턴을 사용한다.
- 슬래시(/)로 시작하면 하위 디렉터리에 적용되지(recursivity) 않는다.
- 디렉터리는 슬래시(/)를 끝에 사용하는 것으로 표현한다.
- 느낌표(!)로 시작하는 패턴의 파일은 무시하지 않는다.

pycache가 이미 올라가 있을 때 삭제 방법
```bash
git rm -r --cached __pycache__
```

## 3/30 월 - .gitignore 수정하기

### .gitignore 파일 수정하기
목표: 보안 개인 정보 안 올리게 하기
1. ```.DS_Store``` 삭제하기
```.DS_Store```: 맥(macOS)이 자동으로 만드는 숨김 파일
이유: 안에 폴더 구조 정보와 숨겨진 파일 이름이 존재

## 3/31 화 - 3-tier 아키텍쳐 설계하기 1차
### 구조
```
│   └── post/                  # 게시글 도메인
│       ├── __init__.py
│       ├── model.py
│       ├── schema.py
│       ├── repository.py
│       ├── service.py
│       └── router.py
```
#### model, schema? router??
모델 (Model): 데이터베이스(DB)에 어떻게 저장할 지?
- 데이터를 어디에 어떻게 저장할지

스키마 (Schema): API에서 주고받는 데이터 형태 (사용자랑 어떻게 주고받을지?)
- 클라이언트랑 어떤 형태로 데이터를 주고받을지
- 주로 pydantic으로 작성함 -> 데이터 검증, 구조 잡아주는 라이브러리 

둘을 나누는 이유? 
- 비밀번호 같은 걸 그대로 응답에 포함될 수 있음
- DB 구조가 API에 그대로 노출됨
- 보안 위험

이 post에 db 정보 예를 들면 게시글 제목, 게시판 날짜 등의 정보가 존재하기 때문에 

스키마 vs 라우터
스키마: 들어오고 나가는 데이터 형식
예) 요청 body에 어떤 값이 들어와야 하는지
라우터: 어떤 URL로 요청이 왔을 때 어떤 함수를 실행할지2

## 4/1 수 - model.py 만들기
### 1. 모델
- SQLAlchemy로 만듦
- 데이터베이스 테이블의 정의
- 실제 저장 구조 
```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```
SQLlite: 간단한 데이터베이스
SQLAlchemy: DB를 파이썬 코드로 다루게 해주는 라이브러리
Base:
```python
from sqlalchemy.orm import sessionmaker, declarative_base
# SQLAlchemy의 기능 가져오기
Base = declarative_base()
# 중요!! 모든 모델의 기준(Base) 생성

# user/model.py
class User(Base):
# post/model.py
class Post(Base):
# 이렇게 각각 DB 테이블 구조가 하나에 추가됨
```
- 흐름
      1. Base 생성
      2. 모델 정의 (User, Post)
      3. create_all() 실행
      4. DB에 테이블 생성됨

파이썬에서 클래스와 테이블 이름은 겹치면 안됨
Column(데이터타입, 옵션1, 옵션2, ...)

1. primary_key: 각 행을 유일하게 구분하는 키
```
id | name   | email
------------------------
1  | 김철수 | a@test.com
2  | 이영희 | b@test.com
3  | 김철수 | c@test.com
```
name은 겹칠 수 있지만 id는 겹치면 안됨 이런거

2. Nullable: NULL 허용 여부
3. unique: 중복 허용 안함
4. index: 검색 속도 빠르게 하는 옵션 (자주 조회하는 칼럼)
- 기본 =  false
5. default: python에 값 생성
6. server_default: db에 값 생성
      - ```server_default=func.now()``` 
      - 값을 안 넣으면 DB가 자동으로 현재 시간 넣어라
      - DB 기준이라 안정성이 높음
7. onupdate: 데이터 수정 시 자동실행
      - ```updated_at = Column(DateTime, onupdate=func.now())```
      - 처음 생성 → created_at 저장
      - 수정됨 → updated_at 자동 변경


### 2. 스키마
#### FastAPI에서는 Pydantic을 사용
#### 크게 2가지 역할
1. 데이터 형식 정의: 데이터는 이렇게 생겨야 한다
```python
class UserCreate(BaseModel):
    name: str
    email: str
```
이라는 코드면 클라이언트는 반드시 아래의 형식으로 보내야함.
```JSON
{
  "name": "kim",
  "email": "test@test.com"
}
```
2. 데이터 검증: 데이터가 올바른지 자동 검사
```python
class UserCreate(BaseModel):
    name: str
    age: int
```
이라는 코드에서 아래와 같은 요청을 보내면 에러가 발생
```JSON
{
  "name": "kim",
  "age": "스무살"
}
```

#### 기본구조
```python
from pydantic import BaseModel

class 클래스이름(BaseModel):
    필드이름: 타입

# 예)
class User(BaseModel):
    name: str
    age: int
```

#### 요청용 스키마 - 클라이언트가 보낼 때
클라이언트가 보낼 때
```python
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
```
FastAPI에서 사용
```python
@app.post("/users")
def create_user(user: UserCreate):
    return user
```

#### 응답용 스키마 
서버가 보낼 데이터
```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```
FastAPI에서 사용
```python
@app.get("/users/{id}", response_model=UserResponse)
def get_user():
    return user
```

#### 전체 흐름
```
클라이언트 → Schema → FastAPI → DB(Model)
                          ↓
                     Schema → 응답
```

#### 일반 구조
- UserCreate → 생성용
- UserUpdate → 수정용
- UserResponse → 응답용

#### Base vs BaseModel
1. Base
- SQLAlchemy
- DB 테이블을 만드는 설계도
- 대상: 서버 내부

2. BaseModel
- Pydantic
- API 데이터 형식 + 검증
- 대상: 클라이언드 (서버에 요청을 보내는 쪽)
      - 클라이언트가 서버에 어떤 형식으로 보내야 하는지
      - 서버가 클라이언트에게 어떤 형식으로 돌려줘야 하는지

### ORM 연동이 뭐냐? - 간단하게 필기만 해봄.
DB 모델(SQLAlchemy 객체)을 Schema(BaseModel)로 변환하는 것

## 4/2 목 - post_schema.py 와 post의 3-tier architecture 만들기
### post_schema.py 만들기
#### 특징
model에 있는 데이터를 기반으로 schema를 만듦.
-> DB(여기서는 model)에 없는 데이터는 저장하거나 조회할 수 없기 때문

### model_config = {"from_attributes": True} 란??
#### 필요한 상황
ORM 객체(SQLAlchemy)를 → schema(BaseModel)로 변환할 때 필요
- ORM: DB를 파이썬 객체처럼 다루게 해주는 도구

### Base vs Basemodel 차이
- Base: DB에 어떻게 저장할까?
- BaseModel: 사용자에게 무엇을 보여줄까?

### FastAPI의 역할
```
<요청할 때>
클라이언트 JSON
→ FastAPI
→ BaseModel
→ 개발자가 ORM 객체 생성
→ DB 저장

<응답할 때>
DB
→ ORM 객체
→ FastAPI
→ BaseModel
→ JSON 응답
```

## 4/3 금 - 3티어 아키텍쳐 만들기 1차

### 3 tier architecture란? 
1. 라우터 Router
2. 서비스 Service
3. 리포지토리 Repository

### REST API란?
Create - POST       생성
Read - GET          조회
Update - PUT PATCH  수정
Delete - DELETE     삭제

## 4/6 월 - 3티어 아키텍쳐 이해하기, 3티어 없이 만들기, 3티어로 나누기
### 내가 3티어 아키텍쳐 부분 코딩을 시작하기 어려웠을까?
#### 0. restapi 즉 get post 등등 먼지 몰랐음 
-> 공부함, 바로 위에 있음
#### 1. from 어쩌고저쩌고 import를 멀 해야할 지 몰랐음
#### 2.  `router = APIRouter(prefix="/api/v1/users", tags=["Users"])` 먼말인지 몰랐음 하지만 중요해보임
```python
router = APIRouter(prefix="/api/v1/users", tags=["Users"])
```
- APIRouter: API들을 묶는 미니 서버
    - 여러 endpoint들을 하나로 묶어서 관리 (user 관련 API, auth 관련 API) 
    - 즉, 여기선 "유저 관련 API 묶음"을 하나 만듦
- prefix: 모든 URL 앞에 자동으로 붙는 경로
- tags=["Users"] : Swagger 문서에서 그룹 이름

#### 3. fastapi 코드를 아키텍쳐 없이도 어떻게 작성해야 하는 지 모르겠음.
모르겠는 것들: fastapi 코드의 큰 틀, 왜 함수를 쓰는 지, 매개 변수들이 먼지, 비즈니스 로직을 어떻게 작성해야하는 지 무슨 문법을 쓰는 지 몰랐음. 그리고 db 연결 문법이랑 어떻게 하는 지 방식을 몰랐음.
##### 분석할 코드 
```python
@router.post("", response_model=UserResponse, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """유저 생성"""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    user = User(
        name=user_in.name,
        email=user_in.email,
        password=user_in.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```
##### fastapi 코드의 큰 틀 
순서
1. 요청 받기
2. 데이터 확인하기  ← (지금 질문)
3. DB에 저장하기
4. 결과 반환하기

##### 왜 함수를 쓰는 지, 매개 변수들이 먼 지
클라이언트가 유저 생성 요청을 보내면, DB에 유저를 저장하고 그 결과를 돌려주는 API
- API: 요청 보내면 → 응답을 주는 규칙
```python
@router.post("")
def create_user(...):
```
- 클라이언트가 요청을 보내면, 서버가 응답을 주는 통로
    - 클라이언트(프론트)가 URL로 "요청을 보내고", 그 요청 안에 JSON 데이터를 담아서 서버로 보냄.
    - 어디로 보낼지 -> URL + 요청 방식
    ```http
    POST /api/v1/users
    ```
    - 무엇을 보낼지
    ```JSON
    {
  "name": "kim",
  "email": "kim@test.com",
  "password": "1234"
    }
    ```
    - 즉, from 클라이언트 to 서버 : “/api/v1/users 주소로 POST 요청을 이 데이터와 같이 보낼게

---

```python
@router.post("", response_model=UserResponse, status_code=201)
```
- 코드 설명: /api/v1/users로 POST 요청이 들어오면 실행되는 함수
    - ()안에 -> 경로, 응답 형식, 성공 시 상태코드 201 반환

--- 

```python
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
```
- 코드 설명: 실제로 요청이 들어왔을 때 실행되는 처리 로직
    - FastAPI에서는 함수 매개변수에 따라 이 값은 어디서 가져와야 하는 지를 자동으로 판단함.
    - `user_in: UserCreate`: 클라이언트가 보낸 요청 body를 의미함.
    - `Usercreate`
    ```python
    class UserCreate(BaseModel):
        name: str
        email: str
        password: str
    ```
    - 이러면 FastAPI가 이 JSON을 읽어서 UserCreate 스키마에 맞게 검사한 뒤 `user_in`에 넣어줌
    ```python
    user_in.name
    user_in.email
    user_in.password
    ```
    - `db: Session = Depends(get_db)`: DB 세션을 주입받는 것
        - 이 함수 실행 전에 get_db()를 실행해서 DB 연결 객체를 db에 넣어줘 = 이 함수 안에서 DB를 쓰고 싶으니까, get_db()를 통해 DB 연결 객체를 가져와라
        ```python
        def get_db():
            db = SessionLocal()   # DB 연결 생성
            try:
                yield db          # 여기서 API 함수로 넘김
            finally:
                db.close()        # 사용 끝나면 닫기,함수 끝나고 실행됨
        ```
        - API 실행 중에는 db 사용 가능하고 끝나면 자동으로 닫힘
        - `db: Session = Depends(get_db)`의 FastAPI식 해석
            1. get_db() 실행
            2. db 객체 받아오기
            3. create_user 함수에 넣어주기
            - 내부적으로는 FastAPI에 대신 해주는 일
            ```python
            db = get_db()  # (실제로는 yield 구조)
            create_user(user_in, db)
            ```
            - FastAPI가 자동으로 이렇게 실행해줌. -> 우리는 함수 정의만 하고, 실행은 FastAPI가 함. 
            ```python
            create_user(
                user_in=요청에서 받은 데이터,
                db=Depends(get_db)로 만든 DB 객체
            )
            ```
            - `create_user`는 FastAPI가 대신 호출하고, 요청이 오면 자동 실행되는 함수
        - db를 모든 함수가 공유하는 게 아니라고???
            - 절대 공유하지 않음!!! -> 요청마다 새로운 db가 만들어짐.
        - db 객체 (Session)
            - `db: Session`
            - DB에 접근하기 위한 "통로", 일종의 "연결 객체"
        - 실제 DB (SQLlite)
            - 데이터가 실제로 저장되는 장소
            - 파일 or 서버
            - 예) sql_app.db  ← SQLite 파일
            ```md
            <요청1>
            get_db() → db1 생성
            db1 → SQLite 접근
            데이터 저장
            db1.close()

            <요청2>
            get_db() → db2 생성
            db2 → SQLite 접근
            데이터 저장
            db2.close()

                [SQLite DB 파일]
                     ↑
            ┌────────┼────────┐
            │        │        │
            db1      db2      db3
            ↑        ↑        ↑
            요청1     요청2     요청3
            ```
            - db1 ≠ db2, 하지만 둘 다 같은 SQLite 파일을 사용
            - db(Session)는 “접속 객체”이고 SQLite는 “실제 데이터 저장소”입니다
            - db 객체: 요청마다 새로 생성됨, 서로 공유 안 함
            - SQLite: 하나, 모든 db 객체가 여기에 연결됨

        - Dependency 의존성
            - ❌ Depends 없이 - 모든 사람이 같은 계좌 공유 → 위험
            - ✅ Depends 사용 - 요청마다: 계좌 열고 거래하고 닫기
            - `Depends(get_db)`: 요청마다 DB 연결을 안전하게 주입해주는 시스템
---
```python
existing = db.query(User).filter(User.email == user_in.email).first()
```
코드 설명: 중복 이메일 확인
- `user_in`: FastAPI가 요청(JSON)을 Python 객체로 바꾼 것
    - `def create_user(user_in: UserCreate, db: Session = Depends(get_db)):`에서
        1. 클라이언트가 서버에 JSON 보냄
        ```JSON
        {
            "name": "kim",
            "email": "kim@test.com",
            "password": "1234"
        }
        ```
        2. FastAPI가 자동으로 
        ```python
        user_in = UserCreate(
            name="kim",
            email="kim@test.com",
            password="1234"
        )
        ```
- `db.query(User)`: User 테이블을 조회할 준비
    - SQLAlchemy ORM 문법
    - db = DB 연결(Session)
    - query = `User`조회 시작
- `filter(User.email == user_in.email)` 
    - 여기까지 공부했음 컴공이라면 이해 가능..
- `first()`: 결과 중 “첫 번째 하나만 가져오기”
    - first() 쓰면
        - 있으면 → 객체 하나
        - 없으면 → None

- `existing = db.query(User).filter(User.email == user_in.email).first()` 전체 흐름
    - 실제로 SQL 문법 - 왜냠 DB에 접근하는 데 DB는 SQL 문법이라서
    ``` SQL
    SELECT * FROM users
    WHERE email = 'kim@test.com'
    LIMIT 1;
    ```
    - 실제 흐름
    ```
    Python 코드 작성
        ↓
    SQLAlchemy가 SQL로 변환
        ↓
    SQLite(DB)에 전달
        ↓
    DB가 실행
        ↓
    결과 반환 ---- (1, "kim", "kim@test.com")
        ↓
    Python 객체로 다시 변환 --- User(id=1, name="kim", email="kim@test.com")
    ```
    - ORM의 역할
        ```
        너: "유저 가져와"
            ↓
        ORM: "SELECT * FROM users"
            ↓
        DB 실행
            ↓
        ORM: 결과를 다시 Python 객체로 번역
        ```
        - ORM: DB(테이블)를 파이썬 객체처럼 다루게 해주는 방식
        - SQLAlchemy: Python에서 ORM을 사용할 수 있게 해주는 도구(라이브러리)
---
```python
if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
```
코드 설명: 이미 있는 이메일이면 에러 발생 

---
```python
    user = User(
        name=user_in.name,
        email=user_in.email,
        password=user_in.password,
    )
```
코드 설명: 새 User 객체 만들기
- User는 보통 SQLAlchemy 모델
- DB 테이블에 넣을 ORM 객체 만드는 것
    - `user_in`은 요청 데이터용 스키마
    -  `User(...)`는 DB 저장용 모델
- 클라이언트가 보낸 데이터는 UserCreate
- DB에 넣을 객체는 User

---
```python
    db.add(user)
    db.commit()
    db.refresh(user)
```
코드 설명
- `db.add(user)`: 새로 만든 user 객체를 DB 세션에 올리는 것
    - 진짜 DB에 저장이 완료된 건 아님
    - 저장할 준비 목록에 올려둠
- `db.commit()`: 이제 진짜 DB에 반영
- `db.refresh(user)`: DB에 저장된 뒤의 최신 상태를 다시 객체에 반영
    - 예시
    ```python
    # 저장 전
    user.name = "kim"
    user.email = "kim@example.com"
    user.id = 없음

    # 저장 후 refresh
    user.id = 1
    user.name = "kim"
    user.email = "kim@example.com"
    ```

---
```python
return user
```
코드 설명: 이걸 반환하면 FastAPI가 response_model=UserResponse에 맞춰서 위에서 db.refresh(user)가 반영된 응답을 만들어줌
- 예) 
```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```
```JSON
{
  "id": 1,
  "name": "kim",
  "email": "kim@example.com"
}
```
!!! 이때, 비밀번호는 UserResponse에 없으면 응답에 안 나감!
=> 보통 password는 응답 스키마에 넣지 않음


###### 추가1 - user_in vs User(...) 차이
- `def create_user(user_in: UserCreate):` 이 줄로 인해 JSON이 파이썬 객체로 바뀜
```JSON
{
  "name": "kim",
  "email": "kim@test.com",
  "password": "1234"
}
```
```python
user_in = UserCreate(
    name="kim",
    email="kim@test.com",
    password="1234"
)
```
- 그리고 이 코드는 DB에 저장될 구조임, SQLAlchemy ORM 객체
```python
    user = User(
        name=user_in.name,
        email=user_in.email,
        password=user_in.password,
    )
```
- User <-> users 테이블
- DB에 넣을 객체임
- `User`란 이름: 개발자가 `user_model.py`에서 정한 파이썬 클래스 이름.
- `users`란 이름: 실제 DB 테이블 이름
```python
class User(Base):
    __tablename__ = "users"
```
- User는 코드용 이름이고, 실제 DB 이름은 __tablename__으로 따로 정함!!

###### 추가2 - commit vs refresh
- commit: DB 저장
- refresh: “DB가 만든 값”을 다시 가져오는 역할
- 필요한 경우
    - 경우 1: 필요함
        - id 자동 생성, timestamp 자동 생성,default 값 있음
        - refresh 필요

    - 경우 2: 필요 없음
        - 모든 값 직접 넣음, DB에서 자동 생성 없음
        -  refresh 없어도 됨


#### 4. 어떻게 나눠야 하는 지 몰랐음 


### 참고한 코드 - 3티어 아키텍쳐 존재하지 않음
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.post("", response_model=UserResponse, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """유저 생성"""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    user = User(
        name=user_in.name,
        email=user_in.email,
        password=user_in.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """전체 유저 조회"""
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """단건 유저 조회"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    """유저 수정"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    if user_in.name is not None:
        user.name = user_in.name
    if user_in.email is not None:
        user.email = user_in.email

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """유저 삭제"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    db.delete(user)
    db.commit()
```
## 4/8 수 - 3티어 아키텍쳐 없는 버전, 있는 버전 만들기

## 4/11 토 - 3티어 아키텍쳐 없는 버전, 있는 버전 만들기 2차
### 3티어 아키텍쳐 없는 버전 하기
```python
# 단건 조회
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db))
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post:
    raise HTTPException(status_code=404, details="게시물을 찾을 수 없습니다.")
  return post
# user_in 은 작성자 혹은 게시글임
```
- post_id가 db와 연결이 되는 지 어케 앎?
    - 아래 orm으로 db와 연결함.
    - 위의 2줄까지의 이해: URL에 있는 post_id 값을 받아서 함수에 넣어라 
- 전체 조회 함수 이름 get_posts vs 단건 조회 함수 이름 get_post
- 작성자, 게시글 검색 내용은 어떻게 나타냄?

```python
  if user_in.title is not None: 
    post.title = user_in.title
  if user_in.content is not None:
    post.content = user_in.content
```
- `user_in.` : 클라이언트에게 받은 값
- `post.` : 내가 함수안에서 db에서 받아온 값, db와 연결된 값

```python
@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)): #받는 정보는 id임
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post: 
    raise HTTPException(status_code=404, details="게시물을 찾을 수 없습니다.")
  
  db.delete(post)
  db.commit
```
- 클라이언트에게 돌려주는 것에 `status_code=204`를 넣는 이유는?
    - 204 No Content 의미
        - 삭제 성공 
        - 하지만 응답 바디는 없음 (return 없음)
- db에서 불러온 post를 지우는 방법
    - `db.delete(post)` 간단함.

### 3티어 아키텍쳐 없는 버전 Swagger UI로 확인하기
확인 완료

### 3티어 아키텍쳐 만들기
#### 현재 코드 예시
```python
@router.post("", response_model=UserResponse, status_code=201)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    # 1. 비즈니스 로직: 이메일 중복 체크
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    # 2. DB 접근: 유저 생성 및 저장
    user = User(name=request.name, email=request.email, password=request.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # 3. 응답 처리
    return user
```
#### 역할별로 분리 - 3티어 아키텍쳐의 시작
**3티어(3-Layer) 아키텍처**는 코드를 역할에 따라 3개 층으로 나누는 패턴입니다.

```
비유: 식당의 역할 분담

  손님(클라이언트) → 홀 직원(Router) → 주방장(Service) → 냉장고(Repository) → DB

  홀 직원: 주문을 받고, 요리를 전달 (요청/응답 처리만)
  주방장:  레시피대로 요리 (비즈니스 로직)
  냉장고:  재료 보관/꺼내기 (데이터 저장/조회)

  → 각자 자기 역할만 하고, 다른 역할에 간섭하지 않음!
```
```
요청 흐름:

[클라이언트]
    │  POST /api/v1/users { name, email, password }
    ▼
[Router]  router.py
    │  "요청 받았다, 서비스한테 넘기자"
    │  return user_service.create_user(request)
    ▼
[Service]  service.py
    │  "이메일 중복인지 확인하고, 유저를 만들자"
    │  if repo.find_by_email(email): 에러!
    │  return repo.save(user)
    ▼
[Repository]  repository.py
    │  "DB에 저장하고 결과를 돌려주자"
    │  db.add(user) → db.commit() → db.refresh(user)
    ▼
[DB]
```
#### 추가 지식들
##### 파이썬 클래스 설명
클래스
- 비슷한 데이터와 기능을 하나로 묶어서 관리하려고 쓰는 것
- 설계도 틀 예) 붕어빵 틀
객체
- 그 설계도로 실제로 만든 것 예) 실제로 만들어진 붕어빵

클래스 문법
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"안녕하세요. 제 이름은 {self.name}이고, 나이는 {self.age}살입니다.")
```
- `__init__` 생성자: 객체를 만들 때 자동으로 실행되는 함수
- 사용법
```python
p1 = Person("철수", 20)
p2 = Person("영희", 22)

print(p1.name)
print(p2.age)

p1.introduce()
p2.introduce()
```
#### 코드 다시 헷갈리는 부분 설명
```python
@router.post("", response_model=PostResponse, status_code=201)
def create_post(user_in: PostCreate, db: Session = Depends(get_db)):
  post = Post(
    title = user_in.title,
    content = user_in.content,
    writer = user_in.writer,
  )
  db.add(post)
  db.commit()
  db.refresh(post)
  return post
```
여기서
```python
post = Post(
    title = user_in.title,
    content = user_in.content,
    writer = user_in.writer,
  )
```
- 요청으로 받은 데이터를 ORM 모델 객체(Post)로 만드는 것
    - 여기 post 기능에서 클라이언트의 정보를 내가 쓰는 db로 넣으려는 준비
    - 즉, ORM 객체로 변환하는 단계
- 비즈니스 로직은 아닌데 위치상 service에 넣기

#### Repository: DB 접근만 담당
- db에 저장, 삭제 정보를 클래스로 작성함
- Repository는 **"어떻게 저장하는가"** 만 알고, **"왜 저장하는가"** (비즈니스 이유)는 모릅니다.

예시 코드)
```python
# app/user/repository.py

from sqlalchemy.orm import Session
from app.user.model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def find_all(self) -> list[User]:
        return self.db.query(User).all()

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
```
repository- `db:Session` vs router- `db:Session = Depends(get_db)`
- 흐름
```
[클라이언트 요청]
        ↓
Router 실행 (FastAPI가 관리)
        ↓
Depends(get_db) 실행 → DB Session 생성
        ↓
db가 Router 함수에 전달됨
        ↓
Service로 전달
        ↓
Repository로 전달
        ↓
DB 사용
```
- 결론
    1. Router에서 Depends(get_db)로 DB 세션을 “한 번 생성”
    2. 그걸 Service → Repository로 계속 전달해서 재사용하는 구조

##### 항상 궁금했던 거! Session이란?
- DB와 대화하는 창구 (연결 + 작업 관리자)
    - 은행 창구 비유
        - DB = 은행
        - Session = 창구 직원
- 흐름
```
Session에게 요청 → Session이 DB에 전달 → 결과 받아옴
```
- 쿼리를 보내고, 결과를 받고, commit/rollback을 관리하는 객체
- Session이 하는 일 
    1. 조회 (SELECT): `db.query(User).all()` DB에서 데이터 가져옴
    2. 변경 관리 (INSERT / UPDATE / DELETE 준비): `db.add(user)` “이거 저장할 거야”라고 예약
    3. commit (진짜 DB 반영): `db.commit()` 실제 DB에 반영
    4. rollback (문제 생기면 취소): `db.rollback()` 작업 취소

- Session이 필요한 이유?
DB를 직접 건드리는 게 아니라 Session을 통해서만 작업하도록 설계됨

- db 코드
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
    1. Session 생성
    2. Router에 전달
    3. 요청 끝나면 자동 종료

##### 화살표란? 
이 함수가 어떤 타입을 반환하는지 알려주는 표시
예)
```python
def find_by_id(self, user_id: int) -> User | None:
```
뜻: User 객체를 반환하거나 없으면 None을 반환함

##### 클래스에서 사용한 self란?
self: 이 객체 자기 자신
- 객체마다 다른 데이터를 가지게 하려고


#### Service: 비즈니스 로직 담당
- Service는 **"무엇을 해야 하는가"** (판단, 검증)를 담당
- 실제 DB 작업은 Repository에게 시킴
- 규칙, 조건, 정책이 들어가야 비즈니스 로직임

## 4/16 목 - post_repository 마무리



#### Router: 