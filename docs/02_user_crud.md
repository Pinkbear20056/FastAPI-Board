# 2회차: User 도메인 CRUD

> 1주차 · 2회차 (2시간)
>
> 목표: User 테이블을 만들고, 5개의 CRUD API를 완성한다.


## 0. Python 기초 문법 빠른 복습

이번 회차부터 본격적으로 코드를 작성합니다. 자주 나오는 문법을 먼저 정리합니다.

### 클래스(class)

```python
# 클래스 = 설계도 (붕어빵 틀)
# 객체 = 설계도로 만든 실제 물건 (붕어빵)

class User:
    name: str       # 이름 (문자열 타입)
    email: str      # 이메일 (문자열 타입)
    age: int        # 나이 (정수 타입)
```

### 상속

```python
# User는 Base의 기능을 물려받는다
class User(Base):       # ← Base를 상속
    __tablename__ = "users"
```

### 타입 힌트

```python
name: str              # name은 문자열
age: int               # age은 정수
email: str | None      # email은 문자열 또는 없음(None)

def greet(name: str) -> str:    # str을 받아서 str을 돌려줌
    return f"안녕, {name}!"
```

### f-string (문자열 안에 변수 넣기)

```python
name = "홍길동"
print(f"안녕하세요, {name}님!")    # → "안녕하세요, 홍길동님!"
```


## 1. User 모델(테이블) 만들기

**모델 = DB 테이블의 설계도** 입니다. Python 클래스로 테이블 구조를 정의합니다.

### app/models.py

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


# User 모델 = users 테이블의 설계도
# Base를 상속받아야 SQLAlchemy가 "이건 테이블이다"라고 인식합니다.
class User(Base):
    __tablename__ = "users"    # 실제 DB에 만들어질 테이블 이름

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

### 각 옵션의 의미

| 옵션 | 의미 | 쉬운 설명 |
|------|------|----------|
| `primary_key=True` | 기본 키 | 행마다 고유한 번호. 자동으로 1, 2, 3... 증가 |
| `unique=True` | 중복 불가 | 같은 이메일로 두 번 가입 불가 |
| `nullable=False` | 빈 값 불가 | 반드시 입력해야 함 |
| `index=True` | 인덱스 생성 | 책의 목차처럼 검색 속도를 빠르게 함 |
| `server_default=func.now()` | 자동 시간 입력 | 데이터 생성 시 현재 시간 자동 기록 |

### Python 클래스 ↔ DB 테이블 매핑

```
Python 코드                       DB에 만들어지는 테이블
──────────                        ────────────────────
class User                    →   CREATE TABLE users
id = Column(Integer, ...)     →   id 컬럼 (숫자, 기본키)
name = Column(String, ...)    →   name 컬럼 (문자열, 필수)
email = Column(String, ...)   →   email 컬럼 (문자열, 중복불가)
```


## 2. User 스키마(DTO) 만들기

### 모델 vs 스키마: 왜 둘 다 필요한가?

| 구분 | 역할 | 비유 |
|------|------|------|
| 모델 (Model) | DB 테이블 구조 정의 | 창고의 선반 구조 |
| 스키마 (Schema/DTO) | API 입출력 데이터 형식 정의 | 택배 송장 양식 |

```
스키마가 왜 필요할까?

DB에는 비밀번호가 저장되어 있습니다.
하지만 API 응답에 비밀번호를 보내면 안 됩니다!

→ "API로 보내는 데이터"와 "DB에 저장된 데이터"의 형식이 다르기 때문에
→ 스키마로 "어떤 데이터를 주고받을지" 별도로 정의합니다.
```

> **DTO(Data Transfer Object)**: "데이터를 옮기는 상자"라는 뜻입니다.
> 스키마와 같은 의미로 사용합니다.

### app/schemas.py

**Pydantic**은 데이터의 형식을 검증해주는 라이브러리입니다.
`BaseModel`을 상속받으면 자동으로 타입 체크, 에러 메시지 생성 등을 해줍니다.

```python
from pydantic import BaseModel
from datetime import datetime


# ── User 스키마 ──

class UserCreate(BaseModel):
    """회원 생성할 때 클라이언트가 보내는 데이터"""
    name: str           # 필수
    email: str          # 필수
    password: str       # 필수


class UserUpdate(BaseModel):
    """회원 수정할 때 클라이언트가 보내는 데이터"""
    name: str | None = None       # 선택 (안 보내면 None)
    email: str | None = None      # 선택

    # str | None = None 의미:
    # str | None → 문자열 또는 None이 올 수 있다
    # = None    → 안 보내면 기본값이 None


class UserResponse(BaseModel):
    """서버가 클라이언트에게 돌려주는 데이터 (비밀번호 제외!)"""
    id: int
    name: str
    email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    # 이 설정이 있어야 SQLAlchemy 모델 객체를 자동으로 스키마로 변환할 수 있습니다.
    # (기본적으로 Pydantic은 딕셔너리만 받는데, 이 설정으로 객체도 받을 수 있게 됨)
    model_config = {"from_attributes": True}
```

### 왜 스키마를 나누는가?

```
클라이언트 → 서버 (요청)
  UserCreate:  { name, email, password }    ← 비밀번호 포함

서버 → 클라이언트 (응답)
  UserResponse: { id, name, email }         ← 비밀번호 제외!
```


## 3. User CRUD API 작성

### 라우터(Router)란?

관련된 API들을 모아놓은 모듈입니다. 파일을 나눠서 정리하기 위해 사용합니다.

```
main.py: 앱의 시작점 (총괄 매니저)
  ├── routers/users.py: 유저 관련 API 모음
  ├── routers/auth.py:  인증 관련 API 모음
  └── routers/posts.py: 게시글 관련 API 모음
```

### app/routers/users.py

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse

# 라우터 생성
# prefix: 이 라우터의 모든 API 경로 앞에 "/api/v1/users"가 붙음
# tags: Swagger UI에서 그룹 이름으로 표시
router = APIRouter(prefix="/api/v1/users", tags=["Users"])


# ──────────────────────────────────────────────
# CREATE: 유저 생성
# ──────────────────────────────────────────────
@router.post("", response_model=UserResponse, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """유저 생성"""

    # response_model=UserResponse → 응답 데이터를 UserResponse 형식으로 자동 변환
    # status_code=201 → 성공 시 201(Created) 상태 코드 반환
    # Depends(get_db) → DB 세션을 자동으로 받아옴 (의존성 주입, 아래에서 설명)

    # 1. 이메일 중복 체크
    existing = db.query(User).filter(User.email == user_in.email).first()
    # db.query(User)             → users 테이블에서
    # .filter(User.email == ...) → 이메일이 같은 행을 찾아서
    # .first()                   → 첫 번째 결과를 가져옴 (없으면 None)

    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
        # raise → 에러를 발생시킴 (함수 즉시 종료)
        # HTTPException → FastAPI가 제공하는 에러 응답

    # 2. 유저 객체 생성
    user = User(
        name=user_in.name,
        email=user_in.email,
        password=user_in.password,  # 2주차에서 해싱 적용 예정
    )

    # 3. DB에 저장
    db.add(user)       # "이 유저를 추가해줘" (아직 DB에 반영 안 됨)
    db.commit()        # "확정!" (여기서 DB에 실제로 반영)
    db.refresh(user)   # DB에서 최신 정보를 다시 읽어옴 (id, created_at 등이 채워짐)
    return user


# ──────────────────────────────────────────────
# READ: 전체 유저 조회
# ──────────────────────────────────────────────
@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """전체 유저 조회"""
    # list[UserResponse] → UserResponse의 목록(리스트)을 반환
    return db.query(User).all()
    # .all() → 모든 행을 리스트로 가져옴


# ──────────────────────────────────────────────
# READ: 단건 유저 조회
# ──────────────────────────────────────────────
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """단건 유저 조회"""
    # /{user_id} → URL에서 값을 받음
    # 예: GET /api/v1/users/3 → user_id = 3

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return user


# ──────────────────────────────────────────────
# UPDATE: 유저 수정
# ──────────────────────────────────────────────
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    """유저 수정"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    # None이 아닌 것만 수정 (안 보낸 필드는 기존 값 유지)
    if user_in.name is not None:
        user.name = user_in.name
    if user_in.email is not None:
        user.email = user_in.email

    db.commit()
    db.refresh(user)
    return user


# ──────────────────────────────────────────────
# DELETE: 유저 삭제
# ──────────────────────────────────────────────
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """유저 삭제"""
    # status_code=204 → "삭제 성공, 돌려줄 데이터 없음"
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    db.delete(user)
    db.commit()
```

### main.py에 라우터 등록

```python
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users

app = FastAPI(title="SYJ API")

Base.metadata.create_all(bind=engine)

# 라우터를 앱에 연결 → 이제 /api/v1/users 경로가 동작합니다
app.include_router(users.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
```


## 4. Depends 이해하기

### Depends란?

`Depends`는 **"이 함수를 실행하기 전에, 먼저 ~를 준비해줘"** 라는 선언입니다.

```python
def get_users(db: Session = Depends(get_db)):
```

이 한 줄의 의미를 풀어보면:

```
"이 함수는 DB 세션(db)이 필요합니다.
 FastAPI야, get_db() 함수를 실행해서 세션을 만들어서 나한테 전달해줘."

비유: 식당에서 주문하면 물은 자동으로 나옴
  → 매번 "물 주세요"라고 안 해도 됨
  → DB 세션도 마찬가지: Depends를 쓰면 자동으로 전달됨
```

### Depends가 왜 라우터에 있어야 하는가?

FastAPI에는 Spring의 `@Autowired` 같은 자동 DI 컨테이너가 없습니다.
그래서 **라우터에서 직접** "무엇이 필요한지"를 `Depends`로 선언해야 합니다.

```python
# 라우터: "나는 UserService가 필요해"
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

@router.get("")
def get_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_users()
```

라우터가 **유일한 진입점**(요청이 들어오는 곳)이기 때문에,
여기서 "어떤 의존성이 필요한지" 선언하는 것이 자연스럽습니다.

### Depends 없이 직접 하면?

```python
# ❌ Depends 없이: 매번 try/finally를 직접 써야 함
@router.get("")
def get_users():
    db = SessionLocal()
    try:
        service = UserService(UserRepository(db))
        return service.get_users()
    finally:
        db.close()  # ← 빠뜨리면 DB 연결이 쌓여서 서버가 죽을 수 있음!

# ❌ 모든 API마다 같은 코드를 반복해야 함
@router.get("/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    try:
        service = UserService(UserRepository(db))
        return service.get_user(user_id)
    finally:
        db.close()
```

```python
# ✅ Depends 사용: try/finally 자동 처리 + 중복 제거
@router.get("")
def get_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_users()

@router.get("/{user_id}")
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user(user_id)
```

### 조립 순서: DB → Repository → Service

```python
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))
```

이 한 줄을 풀어보면:

```
1. Depends(get_db) → DB 세션(db) 생성
2. UserRepository(db) → DB 접근 담당 객체 생성
3. UserService(repo)  → 비즈니스 로직 담당 객체 생성
4. 완성된 UserService를 라우터 함수에 전달

비유: 레고 조립
  바닥판(DB 세션) → 1층 블록(Repository) → 2층 블록(Service) → 완성!
```

### 동작 흐름

```
1. 요청이 들어온다
2. FastAPI가 Depends 체인을 실행:
   get_db() → DB 세션 생성
   get_user_service(db) → Repository → Service 조립
3. 완성된 Service를 라우터 함수에 전달
4. 라우터 함수 실행
5. 함수 종료 후 get_db()의 finally → 세션 자동 닫기
```

### Depends는 용도에 따라 다양하게 쓰인다

| 용도 | Depends 대상 | 역할 |
|------|-------------|------|
| DB 세션 | `get_db()` | 세션 열고, 끝나면 자동 닫기 |
| 서비스 조립 | `get_user_service()` | DB → Repo → Service 조립 |
| 인증 체크 | `get_current_user()` | JWT 토큰 검증, 미인증 시 401 (3회차에서 다룸) |

전부 같은 `Depends` 메커니즘이고, **넣은 함수가 뭘 하느냐**에 따라 역할이 달라집니다.

```
Spring과 비교:
  @Autowired (의존성 주입)        →  Depends(get_user_service)
  @PreAuthorize (인증/인가 체크)  →  Depends(get_current_user)
  Filter/Interceptor (전처리)     →  Depends(어떤_전처리_함수)

  → FastAPI에서는 Depends 하나로 이 모든 역할을 합니다.
```


## 5. Swagger UI에서 테스트

서버 실행 후 http://127.0.0.1:8000/docs 에서:

### 1) 유저 생성 (POST /api/v1/users)
```json
{
  "name": "홍길동",
  "email": "hong@example.com",
  "password": "1234"
}
```

### 2) 전체 조회 (GET /api/v1/users)
→ 방금 만든 유저가 목록에 보이는지 확인

### 3) 단건 조회 (GET /api/v1/users/1)
→ id=1인 유저 정보 확인

### 4) 수정 (PUT /api/v1/users/1)
```json
{
  "name": "홍길동2"
}
```

### 5) 삭제 (DELETE /api/v1/users/1)
→ 204 No Content 응답 확인 (삭제 성공, 돌려줄 데이터 없음)


## 공통 기능: 미들웨어

### 미들웨어란?

모든 요청/응답에 공통으로 적용되는 처리 로직입니다.

```
비유: 건물 출입구의 보안 검색대
  → 모든 사람이 출입할 때 통과해야 함
  → 들어올 때: 요청 기록
  → 나갈 때: 응답 기록 + 걸린 시간 측정

[요청] → [미들웨어] → [API 함수] → [미들웨어] → [응답]
```

### app/context.py — 요청별 고유 ID

먼저, 요청을 추적하기 위한 `trace_id`를 저장할 공간을 만듭니다.

```python
from contextvars import ContextVar

# 요청별 고유 ID — 같은 요청 안에서 미들웨어 로그와 SQL 로그를 묶어서 추적
trace_id_ctx: ContextVar[str] = ContextVar("trace_id", default="-")
```

> **contextvars란?** 같은 요청 안에서 여러 함수가 값을 공유할 수 있게 해주는 Python 표준 기능입니다.
> 미들웨어에서 trace_id를 설정하면, 서비스·DB 계층에서도 같은 값을 읽을 수 있습니다.

### app/main.py에 미들웨어 추가

```python
import time
import uuid
import logging

from fastapi import FastAPI, Request
from app.context import trace_id_ctx

logger = logging.getLogger("uvicorn")

app = FastAPI(title="SYJ API")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """모든 요청에 trace_id를 부여하고, 시작/종료 로그를 기록하는 미들웨어"""
    trace_id = uuid.uuid4().hex[:8]       # 요청마다 8자리 고유 ID 생성
    trace_id_ctx.set(trace_id)            # 이 요청 안에서 어디서든 읽을 수 있게 저장
    logger.info(f"[{trace_id}] {request.method} {request.url.path} ← 요청 시작")
    start = time.time()                    # 시작 시간 기록
    response = await call_next(request)    # 실제 API 함수 실행
    duration = time.time() - start         # 걸린 시간 계산
    logger.info(f"[{trace_id}] {request.method} {request.url.path} → {response.status_code} ({duration:.3f}s)")
    return response

    # async / await 는 "비동기" 문법입니다.
    # 지금은 "미들웨어를 만들 때 쓰는 양식"으로 이해하면 됩니다.
    # call_next(request) = "다음 단계(API 함수)를 실행하고 기다려라"
```

### trace_id가 왜 필요한가?

```
trace_id 없이:
  INFO: POST /api/v1/users ← 요청 시작
  INFO: SQL: SELECT ... FROM users WHERE email = ?
  INFO: GET /api/v1/users ← 요청 시작        ← 다른 요청이 끼어들면?
  INFO: SQL: INSERT INTO users ...            ← 이 SQL이 어느 요청인지 모름!

trace_id 있으면:
  INFO: [a3f1b2c4] POST /api/v1/users ← 요청 시작
  INFO: [a3f1b2c4] SQL: SELECT ... FROM users WHERE email = ?
  INFO: [7e2d9f01] GET /api/v1/users ← 요청 시작
  INFO: [a3f1b2c4] SQL: INSERT INTO users ...   ← a3f1b2c4 요청의 SQL!
```

서버 로그 예시:
```
INFO: [a3f1b2c4] POST /api/v1/users ← 요청 시작
INFO: [a3f1b2c4] 유저 생성 요청: email=hong@example.com
INFO: [a3f1b2c4] SQL: SELECT ... FROM users WHERE users.email = ? | params: ('hong@example.com',)
INFO: [a3f1b2c4] SQL: INSERT INTO users ... | params: ('홍길동', 'hong@example.com', '1234')
INFO: [a3f1b2c4] 유저 생성 완료: id=1
INFO: [a3f1b2c4] POST /api/v1/users → 201 (0.012s)
```


## 공통 기능: 에러 핸들러

### 통일된 에러 응답 형식

기본 FastAPI 에러 응답:
```json
{"detail": "유저를 찾을 수 없습니다."}
```

커스텀 에러 응답으로 통일 (프론트엔드 개발자가 처리하기 편함):
```json
{
  "error": {
    "code": 404,
    "message": "유저를 찾을 수 없습니다."
  }
}
```

### app/main.py에 에러 핸들러 추가

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


# HTTPException이 발생하면 이 함수가 대신 응답을 만듭니다
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.status_code, "message": exc.detail}},
    )


# 입력값이 잘못되면 (예: 숫자 자리에 문자를 보냄) 이 함수가 응답을 만듭니다
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": {"code": 400, "message": "입력값이 올바르지 않습니다.", "details": str(exc)}},
    )
```


## 6. 코드 구조 개선: 3티어 아키텍처

### 지금 코드의 문제점

지금까지 작성한 라우터를 다시 살펴보세요.
**하나의 함수 안에 모든 것이 섞여 있습니다.**

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

지금은 API가 5개뿐이라 괜찮아 보입니다.
하지만 실제 서비스에서는 어떨까요?

```
문제 1: 코드가 비대해진다
  → 유저 관련 로직이 복잡해지면 (가입 시 이메일 발송, 포인트 지급, 알림 등)
  → 라우터 함수 하나가 수백 줄이 됩니다

문제 2: 같은 로직을 여러 곳에서 써야 할 때
  → "이메일로 유저 찾기" 로직이 회원가입, 로그인, 비밀번호 찾기에서 모두 필요
  → 라우터에 있으면 복사-붙여넣기 해야 함 (코드 중복!)

문제 3: 테스트가 어렵다
  → DB를 직접 다루는 코드와 비즈니스 로직이 섞여 있어서
  → 비즈니스 로직만 따로 테스트할 수 없음
```

### 해결: 역할별로 코드를 분리하자

**3티어(3-Layer) 아키텍처**는 코드를 역할에 따라 3개 층으로 나누는 패턴입니다.

```
비유: 식당의 역할 분담

  손님(클라이언트) → 홀 직원(Router) → 주방장(Service) → 냉장고(Repository) → DB

  홀 직원: 주문을 받고, 요리를 전달 (요청/응답 처리만)
  주방장:  레시피대로 요리 (비즈니스 로직)
  냉장고:  재료 보관/꺼내기 (데이터 저장/조회)

  → 각자 자기 역할만 하고, 다른 역할에 간섭하지 않음!
```

| 계층 | 역할 | 비유 | 파일 |
|------|------|------|------|
| **Router** (라우터) | 요청을 받고 응답을 돌려줌 | 홀 직원 | `router.py` |
| **Service** (서비스) | 비즈니스 로직 (검증, 판단, 처리) | 주방장 | `service.py` |
| **Repository** (레포지토리) | DB 접근 (조회, 저장, 삭제) | 냉장고 | `repository.py` |

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

### 프로젝트 구조: 도메인별 패키지

기능별(routers/, services/, repositories/)이 아니라,
**도메인별(user/, board/)** 로 묶으면 관련 코드를 한눈에 볼 수 있습니다.

```
❌ 기능별 구조 (파일이 흩어짐)
app/
├── routers/
│   ├── users.py
│   └── posts.py
├── services/
│   ├── user_service.py
│   └── post_service.py
└── repositories/
    ├── user_repository.py
    └── post_repository.py

→ user 관련 코드를 보려면 3개 폴더를 왔다갔다 해야 함


✅ 도메인별 구조 (관련 코드가 한 곳에!)
app/
├── user/
│   ├── model.py          # 테이블 정의
│   ├── schema.py         # DTO (입출력 형식)
│   ├── repository.py     # DB 접근
│   ├── service.py        # 비즈니스 로직
│   └── router.py         # API 엔드포인트
├── board/
│   ├── model.py
│   ├── schema.py
│   ├── repository.py
│   ├── service.py
│   └── router.py
├── main.py
└── database.py

→ user 관련 코드는 user/ 폴더만 보면 됨!
```

### Repository: DB 접근만 담당

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

> Repository는 **"어떻게 저장하는가"** 만 알고,
> **"왜 저장하는가"** (비즈니스 이유)는 모릅니다.

### Service: 비즈니스 로직 담당

```python
# app/user/service.py

from fastapi import HTTPException
from app.user.model import User
from app.user.schema import UserCreate, UserUpdate
from app.user.repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, request: UserCreate) -> User:
        # 비즈니스 로직: 이메일 중복 체크
        if self.repo.find_by_email(request.email):
            raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

        user = User(
            name=request.name,
            email=request.email,
            password=request.password,
        )
        return self.repo.save(user)

    def get_users(self) -> list[User]:
        return self.repo.find_all()

    def get_user(self, user_id: int) -> User:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        return user

    def update_user(self, user_id: int, request: UserUpdate) -> User:
        user = self.get_user(user_id)

        if request.name is not None:
            user.name = request.name
        if request.email is not None:
            user.email = request.email

        return self.repo.save(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repo.delete(user)
```

> Service는 **"무엇을 해야 하는가"** (판단, 검증)를 담당하고,
> 실제 DB 작업은 Repository에게 시킵니다.

### Router: 요청/응답 처리만 담당

```python
# app/user/router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.user.schema import UserCreate, UserUpdate, UserResponse
from app.user.repository import UserRepository
from app.user.service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """DB 세션 → Repository → Service 순서로 조립하여 전달"""
    return UserService(UserRepository(db))


@router.post("", response_model=UserResponse, status_code=201)
def create_user(request: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(request)


@router.get("", response_model=list[UserResponse])
def get_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, request: UserUpdate, user_service: UserService = Depends(get_user_service)):
    return user_service.update_user(user_id, request)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user_service.delete_user(user_id)
```

> Router는 **깔끔합니다.** 요청을 받고 서비스에 넘기고 결과를 돌려줄 뿐.
> DB 코드(`db.query`, `db.add`)가 하나도 없습니다!

### main.py 변경점

```python
# 변경 전 (routers 폴더 구조)
from app.routers import users
app.include_router(users.router)

# 변경 후 (도메인 패키지 구조)
from app.user.router import router as user_router
app.include_router(user_router)
```

### 의존성 조립 흐름

```python
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))
```

이 함수가 하는 일을 풀어보면:

```
1. FastAPI가 get_db()를 호출 → DB 세션(db) 생성
2. db를 넣어서 UserRepository(db) 생성   ← DB 접근 담당
3. repo를 넣어서 UserService(repo) 생성  ← 비즈니스 로직 담당
4. 완성된 UserService를 라우터 함수에 전달

비유: 레고 조립
  바닥판(DB 세션) → 1층 블록(Repository) → 2층 블록(Service) → 완성!
```

### Before / After 비교

```python
# ❌ Before: 라우터에 모든 것이 섞여 있음 (통짜)
@router.post("")
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == request.email).first()  # DB 접근
    if existing:                                                            # 비즈니스 로직
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    user = User(name=request.name, email=request.email, password=request.password)
    db.add(user)                                                           # DB 접근
    db.commit()                                                            # DB 접근
    db.refresh(user)                                                       # DB 접근
    return user

# ✅ After: 라우터는 서비스에 위임만 함 (깔끔!)
@router.post("")
def create_user(request: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(request)
```

### 정리: 왜 분리하는가?

| 문제 | 통짜 코드 | 3티어 분리 |
|------|----------|-----------|
| 코드가 길어짐 | 라우터 함수가 수백 줄 | 각 계층이 짧고 명확 |
| 코드 중복 | 같은 DB 조회를 여러 라우터에 복붙 | Repository 메서드 하나를 재사용 |
| 역할 파악 | "이 줄이 DB 접근인지 로직인지?" | 파일명만 봐도 역할을 알 수 있음 |
| 테스트 | 전체를 통으로 테스트 | 서비스 로직만 따로 테스트 가능 |
| 유지보수 | DB 변경 시 라우터 전체 수정 | Repository만 수정하면 끝 |


## 실습 과제

1. 유저 3명을 생성해보세요.
2. 같은 이메일로 생성 시도 → 400 에러 확인
3. 존재하지 않는 id(예: 999)로 조회 → 404 에러 확인
4. 유저 이름을 수정하고 다시 조회해서 반영 확인
5. 유저 삭제 후 목록 조회해서 사라졌는지 확인


## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| Model | DB 테이블의 설계도 (SQLAlchemy) |
| Schema/DTO | API로 주고받는 데이터의 형식 정의 (Pydantic) |
| Router | 요청을 받고 응답을 돌려주는 계층 (홀 직원) |
| Service | 비즈니스 로직을 처리하는 계층 (주방장) |
| Repository | DB에 접근하는 계층 (냉장고) |
| 3티어 아키텍처 | Router → Service → Repository 로 역할을 분리하는 패턴 |
| 도메인별 패키지 | 관련 코드를 한 폴더에 모음 (app/user/, app/board/) |
| Depends | 함수에 필요한 것을 자동으로 전달 (의존성 주입) |
| CRUD | Create(생성), Read(조회), Update(수정), Delete(삭제) |
| `db.add()` | "이것 저장해줘" 예약 (아직 반영 안 됨) |
| `db.commit()` | "확정!" (DB에 실제 반영) |
| `db.refresh()` | DB에서 최신 정보 다시 읽기 (id 등 자동생성 값 확인) |
| 미들웨어 | 모든 요청/응답에 공통으로 적용되는 처리 |
| 에러 핸들러 | 에러 발생 시 통일된 응답 형식으로 변환 |
