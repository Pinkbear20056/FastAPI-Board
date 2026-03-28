# 3회차: 회원가입 + JWT 개념

> 2주차 · 3회차 (2시간)
>
> 목표: 비밀번호를 안전하게 해싱하여 저장하고, JWT의 개념을 이해한다.


## 1. 1주차 복습

### 지금까지 만든 것
- FastAPI + uvicorn 서버 기동
- SQLAlchemy + SQLite DB 연결
- User CRUD API 5개
- 미들웨어 (요청 로깅)
- 에러 핸들러 (통일된 에러 응답)

### 문제점: 비밀번호가 그대로 저장되고 있다!

현재 비밀번호가 **평문(plain text, 변환 없이 원본 그대로)** 으로 DB에 저장되고 있습니다.

```
DB에 저장된 데이터:
id=1, name="홍길동", password="1234"   ← 위험!
```

만약 DB가 해킹당하면? → 모든 사용자의 비밀번호가 그대로 노출됩니다.
이것을 해결하기 위해 **해싱(Hashing)** 을 사용합니다.


## 2. 비밀번호 해싱(bcrypt)

### 해싱이란?

해싱은 **원본 데이터를 복원할 수 없는 형태로 변환하는 것**입니다.

```
비유: 종이 문서를 파쇄기에 넣는 것
  → 원본을 알아볼 수 없게 잘게 쪼개짐
  → 잘린 종이를 다시 원본으로 되돌릴 수 없음
  → 하지만 같은 문서를 넣으면 같은 결과가 나옴 (검증 가능)

원본              해싱 함수           해시값
"1234"    →    bcrypt()    →    "$2b$12$LJ3m5Kx7..."

특징:
- 단방향: 해시값 → 원본 복원 불가능 (파쇄된 종이를 되돌릴 수 없듯이)
- 같은 입력 → 매번 다른 해시값 (salt라는 랜덤 값을 섞기 때문)
- 검증은 가능: "이 비밀번호가 맞는지" 확인할 수 있음
```

### salt(소금)란?

```
같은 비밀번호 "1234"를 여러 명이 쓰더라도,
각각 다른 해시값이 만들어지게 하는 랜덤 값입니다.

비유: 같은 레시피로 요리해도 소금을 다르게 넣으면 맛이 달라지듯이

유저 A: "1234" + salt_A → "$2b$12$ABC..."  (다름!)
유저 B: "1234" + salt_B → "$2b$12$XYZ..."  (다름!)

→ 해커가 "1234"의 해시값을 알아도, 다른 사용자의 비밀번호를 찾을 수 없음
```

### 왜 bcrypt인가?

| 방식 | 안전성 | 설명 |
|------|--------|------|
| 평문 저장 | X | DB 유출 시 비밀번호 즉시 노출 |
| MD5/SHA256 | 보통 | 빠른 연산 → 해커가 초당 수억 번 대입 가능 |
| **bcrypt** | **안전** | **의도적으로 느린 연산 + salt → 대입 공격에 강함** |


## 3. auth 모듈 구조

User 모듈처럼 auth도 **3티어 구조**로 만듭니다.

```
app/auth/
├── __init__.py
├── auth_utils.py       ← 비밀번호 해싱 + JWT 토큰 생성/검증 (유틸 함수)
├── auth_schema.py      ← 요청/응답 DTO (SignupRequest, LoginRequest 등)
├── auth_service.py     ← 비즈니스 로직 (회원가입, 로그인)
└── auth_router.py      ← API 엔드포인트 (/signup, /login)
```

### 왜 auth는 repository가 없나요?

auth 모듈은 **User 테이블을 그대로 사용**합니다.
새로운 테이블이 필요 없으므로 `UserRepository`를 재사용합니다.

```
[auth_router] → [auth_service] → [user_repository] → [DB]
                                    ↑ 재사용!
[user_router] → [user_service] → [user_repository] → [DB]
```


## 4. 비밀번호 해싱 유틸

### app/auth/auth_utils.py

```python
from datetime import datetime, timedelta

import bcrypt
from jose import jwt       # JWT 토큰을 만들고 검증하는 라이브러리

# ── 설정값 ──
SECRET_KEY = "your-secret-key-change-in-production"
# SECRET_KEY: JWT 토큰을 만들 때 사용하는 비밀 열쇠.
# 이 열쇠를 아는 사람만 토큰을 만들고 검증할 수 있습니다.
# 실제 서비스에서는 절대 코드에 직접 쓰지 않고, 환경변수로 관리합니다.

ALGORITHM = "HS256"
# 토큰 서명에 사용할 알고리즘 (수업에서는 이 값을 고정해서 사용)

ACCESS_TOKEN_EXPIRE_MINUTES = 60
# 토큰 유효 시간 (60분 후 만료)


# ── 비밀번호 해싱 ──

def hash_password(password: str) -> str:
    """비밀번호를 bcrypt로 해싱하여 반환"""
    return bcrypt.hashpw(
        password.encode("utf-8"),   # 문자열 → 바이트로 변환 (bcrypt가 바이트를 요구)
        bcrypt.gensalt(),           # 랜덤 salt 생성
    ).decode("utf-8")              # 바이트 → 문자열로 변환 (DB에 저장하기 위해)

    # .encode("utf-8"): 문자열("1234")을 컴퓨터가 처리할 수 있는 바이트(b"1234")로 변환
    # .decode("utf-8"): 바이트를 다시 문자열로 변환
    # 왜? bcrypt 라이브러리가 바이트 형태로 입력을 받기 때문


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """입력된 비밀번호가 해시값과 일치하는지 확인"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )
    # True: 비밀번호 일치
    # False: 비밀번호 불일치
```

### 해싱 동작 확인

```python
hashed = hash_password("1234")
print(hashed)
# "$2b$12$LJ3m5Kx7Q..."  (매번 실행할 때마다 다른 값!)

print(verify_password("1234", hashed))   # True  (원본과 일치)
print(verify_password("5678", hashed))   # False (원본과 불일치)
```


## 5. 회원가입 스키마

### app/auth/auth_schema.py

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime


class SignupRequest(BaseModel):
    """회원가입 요청"""
    name: str
    email: EmailStr
    password: str


class SignupResponse(BaseModel):
    """회원가입 응답 (비밀번호는 절대 응답에 포함하지 않음!)"""
    id: int
    name: str
    email: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
```


## 6. 회원가입 서비스

### app/auth/auth_service.py

```python
from app.user.user_model import User
from app.user.user_repository import UserRepository
from app.auth.auth_utils import hash_password
from app.auth.auth_schema import SignupRequest


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def signup(self, request: SignupRequest) -> User:
        """회원가입: 이메일 중복 체크 + 비밀번호 해싱 후 저장"""
        # 1. 이메일 중복 체크
        if self.user_repository.find_by_email(request.email):
            raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

        # 2. 비밀번호 해싱 (평문이 아닌 해시값을 저장!)
        hashed = hash_password(request.password)
        #   "1234" → "$2b$12$LJ3m..."

        # 3. 유저 생성 및 저장
        user = User(name=request.name, email=request.email, password=hashed)
        saved = self.user_repository.save(user)
        return saved
```

### User 모듈과의 차이

```
[UserService.create_user]     → 비밀번호를 평문 그대로 저장
[AuthService.signup]          → 비밀번호를 bcrypt로 해싱 후 저장

→ 회원가입은 AuthService.signup을 사용해야 안전!
```


## 7. 회원가입 라우터

### app/auth/auth_router.py

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.user.user_repository import UserRepository
from app.auth.auth_schema import SignupRequest, SignupResponse
from app.auth.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


# 의존성 조립: DB 세션 → UserRepository → AuthService
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/signup", response_model=SignupResponse, status_code=201)
def signup(request: SignupRequest, auth_service: AuthService = Depends(get_auth_service)):
    """회원가입"""
    return auth_service.signup(request)
```

### 의존성 조립 흐름

```
요청 도착
  │
  ├─ Depends(get_db)           → DB 세션 생성
  ├─ Depends(get_auth_service) → UserRepository(db) → AuthService(user_repository)
  │
  ▼
  signup(request, auth_service) 실행
```

User 모듈과 동일한 패턴입니다. auth_service가 user_repository를 재사용하는 것이 핵심!

### main.py에 라우터 등록

```python
from app.auth.auth_router import router as auth_router
from app.user.user_router import router as user_router

app.include_router(auth_router)
app.include_router(user_router)
```


## 8. JWT 토큰 개념

비밀번호를 안전하게 저장했습니다. 이제 다음 질문:
**"로그인한 사용자를 어떻게 기억하지?"**

### 인증(Authentication)이란?

```
"이 요청을 보낸 사람이 누구인지 확인하는 것"

비유: 놀이공원
  - 입장할 때 팔찌(토큰)를 받음
  - 놀이기구 탈 때마다 팔찌를 보여줌
  - 팔찌가 없으면 탈 수 없음
  - 팔찌에 만료 시간이 있어서, 지나면 재입장 필요
```

### 세션 방식 vs 토큰(JWT) 방식

```
[세션 방식] - 전통적인 방법
  1. 로그인 → 서버가 "로그인 기록"을 메모리에 저장
  2. 매 요청마다 → 서버가 저장된 기록과 비교
  문제: 서버가 모든 사용자의 상태를 기억해야 함 (서버 부담 큼)

[JWT 방식] - 우리가 사용할 방법
  1. 로그인 → 서버가 "토큰(팔찌)"를 발급
  2. 매 요청마다 → 클라이언트가 토큰을 보냄 → 서버가 토큰 자체를 검증
  장점: 서버가 아무것도 기억할 필요 없음! (토큰에 정보가 담겨 있음)
```

### JWT(JSON Web Token)의 구조

JWT 토큰은 점(.)으로 구분된 3개 부분으로 이루어져 있습니다.

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzA5...}.SflKxwRJSMe...
 \_____________________/ \________________________________/ \______________/
       Header                     Payload                     Signature
   (어떤 알고리즘?)            (누구의 토큰?)              (위조 방지 서명)
```

| 부분 | 내용 | 비유 |
|------|------|------|
| Header | 알고리즘 정보 (HS256) | 팔찌의 재질 |
| Payload | 사용자 정보 (user_id, 만료시간) | 팔찌에 적힌 이름과 유효기간 |
| Signature | 비밀키로 만든 서명 | 위조 방지 홀로그램 |

### JWT의 핵심 동작

```
1. 서버가 비밀키(SECRET_KEY)로 토큰을 만든다 (서명)
2. 클라이언트가 토큰을 저장하고, 매 요청마다 보낸다
3. 서버가 비밀키로 토큰이 변조되지 않았는지 확인한다 (검증)

→ 비밀키를 아는 것은 서버뿐 → 위조 불가능
→ 토큰 자체에 user_id가 담겨 있음 → DB 조회 없이도 "누구인지" 알 수 있음
```

### 토큰 생성 함수 (auth_utils.py에 포함)

```python
def create_access_token(user_id: int) -> str:
    """JWT 액세스 토큰 생성"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 현재 시간 + 60분 = 만료 시간

    payload = {
        "sub": str(user_id),  # sub(subject): 토큰의 주인이 누구인지 (JWT 표준 필드)
        "exp": expire,        # exp(expiration): 언제 만료되는지 (JWT 표준 필드)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    # payload + SECRET_KEY → 토큰 문자열 생성
```


## 9. 트랜잭션 개념

회원가입처럼 DB에 데이터를 저장할 때, **트랜잭션**이라는 중요한 개념이 있습니다.

### 트랜잭션이란?

```
여러 DB 작업을 "하나의 묶음"으로 처리하는 것.
전부 성공하면 확정(commit), 하나라도 실패하면 전부 취소(rollback)

비유: ATM 송금
  1단계: 내 계좌에서 10만원 차감
  2단계: 상대 계좌에 10만원 추가

  만약 1단계는 됐는데 2단계에서 에러가 나면?
  → 내 돈만 사라짐! (큰일!)
  → 트랜잭션: 2단계가 실패하면 1단계도 취소 (원래 상태로 되돌림)
```

### 코드에서 트랜잭션

```python
# UserRepository.save()에서 트랜잭션이 동작하는 방식:

def save(self, user: User) -> User:
    self.db.add(user)       # 1. "추가" 예약    ← 아직 DB에 반영 안 됨
    self.db.commit()        # 2. "확정!" 실행   ← 여기서 DB에 실제 반영
    self.db.refresh(user)   # 3. DB에서 최신 상태 다시 읽기
    return user

# 만약 commit() 전에 에러가 발생하면?
# → 자동으로 rollback (모든 작업 취소, 원래 상태로 복원)
```

현재 우리 코드에서는 `get_db()` 함수가 세션의 생명주기(열기/닫기)를 자동 관리합니다.


## 실습 과제

1. Swagger에서 회원가입 API를 호출해보세요.
2. 같은 이메일로 다시 가입 시도 → 400 에러 확인
3. (선택) DB를 직접 열어서 비밀번호가 `$2b$12$...` 형태로 해싱되어 저장되었는지 확인


## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| 해싱 | 원본을 복원할 수 없게 변환 (비밀번호 보호) |
| bcrypt | 느리고 안전한 해싱 알고리즘 (비밀번호 전용) |
| salt | 해싱에 섞는 랜덤 값 (같은 비밀번호 → 다른 해시) |
| .encode()/.decode() | 문자열 ↔ 바이트 변환 (라이브러리가 바이트를 요구할 때 사용) |
| JWT | 서버가 발급하는 인증 토큰 (놀이공원 팔찌) |
| SECRET_KEY | 토큰을 만들고 검증하는 비밀 열쇠 |
| Payload | 토큰에 담긴 데이터 (sub=누구, exp=만료시간) |
| 트랜잭션 | 여러 DB 작업을 하나로 묶어, 실패 시 전부 취소 |
| commit | 확정! (DB에 반영) |
| rollback | 취소! (실패 시 원래 상태로) |
