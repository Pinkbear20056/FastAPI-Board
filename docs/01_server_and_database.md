# 1회차: WAS + 서버 기동 + DB 연결

> 1주차 · 1회차 (2시간)
>
> 목표: FastAPI 서버를 실행하고, SQLite 데이터베이스에 연결한다.


## 1. WAS(Web Application Server)란?

웹 서비스가 동작하는 구조를 식당에 비유해보겠습니다.

```
식당 비유                              실제 웹 서비스
──────                                ──────────────

손님이 메뉴를 주문한다          →    브라우저가 서버에 요청을 보낸다
홀 직원이 주문을 받는다          →    웹 서버(Nginx)가 요청을 받는다
주방장이 요리를 만든다           →    WAS(uvicorn)가 로직을 실행한다
냉장고에서 재료를 꺼낸다         →    데이터베이스에서 데이터를 가져온다
완성된 요리를 손님에게 전달      →    응답을 브라우저에 돌려준다
```

### 웹 서버 vs WAS

```
[클라이언트(브라우저)]
        │
        ▼
[웹 서버 (Nginx, Apache)]       ← 정적 파일(HTML, CSS, 이미지) 전달
        │
        ▼
[WAS (uvicorn + FastAPI)]       ← 동적 처리(비즈니스 로직, DB 조회)
        │
        ▼
[데이터베이스 (SQLite)]
```

| 구분 | 웹 서버 | WAS |
|------|---------|-----|
| 역할 | 정적 파일 전달 | 비즈니스 로직 실행 |
| 예시 | Nginx, Apache | uvicorn, Gunicorn, Tomcat |
| 처리 | HTML, CSS, 이미지 | API 요청, DB 조회, 인증 |

우리 수업에서는 **uvicorn**(WAS) + **FastAPI**(웹 프레임워크) 조합을 사용합니다.

> **uvicorn**은 FastAPI 코드를 실행해주는 서버 프로그램입니다.
> FastAPI 혼자서는 실행될 수 없고, uvicorn이 있어야 요청을 받을 수 있습니다.


## 2. 웹의 기본: 요청(Request)과 응답(Response)

웹은 결국 **"질문과 답변"** 입니다.

```
클라이언트(브라우저):  "id가 1인 유저 정보 주세요"  → 요청(Request)
서버:                 "여기 있습니다: 홍길동"       → 응답(Response)
```

### HTTP 요청의 구조

```
POST /api/v1/users HTTP/1.1       ← 메서드 + 경로 (무엇을 할지)
Host: localhost:8000              ← 헤더 (부가 정보)
Content-Type: application/json

{                                 ← 바디 (보내는 데이터)
  "name": "홍길동",
  "email": "hong@example.com"
}
```

### HTTP 응답의 구조

```
HTTP/1.1 200 OK                   ← 상태 코드 (성공/실패 여부)
Content-Type: application/json

{                                 ← 바디 (돌려주는 데이터)
  "id": 1,
  "name": "홍길동",
  "email": "hong@example.com"
}
```

### 주요 HTTP 메서드

| 메서드 | 용도 | 비유 | 예시 |
|--------|------|------|------|
| GET | 조회 | "보여줘" | 유저 목록 가져오기 |
| POST | 생성 | "만들어줘" | 새 유저 만들기 |
| PUT | 수정 | "바꿔줘" | 유저 정보 변경 |
| DELETE | 삭제 | "지워줘" | 유저 삭제 |

### 주요 상태 코드

| 코드 | 의미 | 쉬운 설명 |
|------|------|----------|
| 200 | OK | 성공! |
| 201 | Created | 새로 만들었어! |
| 400 | Bad Request | 요청이 잘못됐어 (입력값 오류) |
| 401 | Unauthorized | 로그인 안 했어 / 토큰이 없어 |
| 403 | Forbidden | 로그인은 했는데 권한이 없어 |
| 404 | Not Found | 요청한 데이터가 없어 |
| 500 | Internal Server Error | 서버가 고장났어 |


## 3. FastAPI + uvicorn으로 서버 기동

### app/main.py

```python
from fastapi import FastAPI

# FastAPI 앱을 만듭니다.
# title은 Swagger UI에 표시되는 이름입니다.
app = FastAPI(title="SYJ API")


# @app.get("/health") 는 "데코레이터"라고 합니다.
# 뜻: "GET 방식으로 /health 경로에 요청이 오면, 아래 함수를 실행해라"
#
# 쉽게 말해, URL과 함수를 연결해주는 표시입니다.
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

> **데코레이터(@)란?** 함수 위에 `@`로 시작하는 줄입니다.
> "이 함수에 특별한 기능을 추가해라"라는 뜻입니다.
> `@app.get("/health")` = "GET /health 요청이 오면 이 함수를 실행해라"

### 서버 실행

```bash
uvicorn app.main:app --reload
```

- `app.main` → `app/main.py` 파일
- `:app` → 그 안의 `app` 변수 (FastAPI 인스턴스)
- `--reload` → 코드 수정 시 자동 재시작

### 확인

- http://127.0.0.1:8000/health → `{"status": "ok"}`
- http://127.0.0.1:8000/docs → Swagger UI


## 4. Swagger UI 살펴보기

Swagger UI는 FastAPI가 자동으로 만들어주는 **API 문서 + 테스트 도구**입니다.
코드를 작성하면 별도 작업 없이 자동으로 생성됩니다!

- `/docs` → Swagger UI (직접 API를 호출해볼 수 있음)
- `/redoc` → ReDoc (읽기 전용 문서)

Swagger에서 할 수 있는 것:
1. API 목록 확인
2. 각 API의 요청/응답 형식 확인
3. **"Try it out"** 버튼으로 직접 API 호출 테스트 (Postman 같은 외부 도구 필요 없음!)


## 5. SQLAlchemy + SQLite 개념

### 데이터베이스란?

데이터를 체계적으로 저장하는 프로그램입니다. 엑셀 표를 떠올리면 쉽습니다.

```
users 테이블 (엑셀의 시트와 비슷)
┌────┬────────┬──────────────────┐
│ id │ name   │ email            │
├────┼────────┼──────────────────┤
│ 1  │ 홍길동  │ hong@example.com │
│ 2  │ 김철수  │ kim@example.com  │
└────┴────────┴──────────────────┘
```

### SQL이란?

데이터베이스에 명령을 내리는 언어입니다.

```sql
-- "모든 유저를 보여줘"
SELECT * FROM users;

-- "홍길동을 추가해줘"
INSERT INTO users (name, email) VALUES ('홍길동', 'hong@example.com');
```

### SQLAlchemy란? (ORM)

ORM(Object Relational Mapping)은 **SQL을 직접 쓰지 않고, Python 코드로 DB를 다루는 기술**입니다.

```
SQL 직접 작성 (어려움)           Python 코드 (쉬움)
────────────────────            ──────────────────
INSERT INTO users               user = User(name="홍길동")
(name) VALUES ('홍길동')    →    db.add(user)

SELECT * FROM users         →    db.query(User).all()
```

SQLAlchemy는 Python에서 가장 많이 쓰이는 ORM 라이브러리입니다.

### SQLite란?

- 파일 하나(`.db`)로 동작하는 가벼운 데이터베이스
- 별도 서버 설치 불필요 → 학습용으로 적합
- 실무에서는 PostgreSQL, MySQL 등을 사용


## 6. database.py 작성

### app/database.py

```python
import logging

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

from app.context import trace_id_ctx

logger = logging.getLogger("uvicorn")

# SQLite 파일 경로 (프로젝트 폴더에 sql_app.db 파일이 생김)
DATABASE_URL = "sqlite:///./sql_app.db"

# Engine: DB와 연결하는 통로
# (비유: DB 서버의 "전화번호"를 등록하는 것)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite에서 필요한 설정
)


# SQL 쿼리 로그: 실행되는 SQL을 한 줄로 출력 (trace_id 포함)
# → API 호출 시 어떤 SQL이 실행되는지 서버 로그에서 확인할 수 있습니다.
@event.listens_for(engine, "before_cursor_execute")
def _log_sql(conn, cursor, statement, parameters, context, executemany):
    trace_id = trace_id_ctx.get()
    sql = " ".join(statement.split())  # 줄바꿈/탭 → 공백 한 칸으로 압축
    logger.info(f"[{trace_id}] SQL: {sql} | params: {parameters}")

# Session: DB에 명령을 보내는 창구
# SessionLocal은 "세션을 만들어주는 공장"입니다.
# (비유: 은행 창구. 볼일이 있을 때 번호표를 뽑고, 끝나면 나옴)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: 모든 테이블 모델의 부모 클래스
# 이걸 상속받아야 SQLAlchemy가 테이블로 인식합니다.
Base = declarative_base()


def get_db():
    """
    요청마다 DB 세션(창구)을 하나 열고, 요청이 끝나면 닫는 함수.

    yield는 return과 비슷하지만,
    함수가 끝나지 않고 "잠시 멈춘" 상태입니다.
    - yield db: db를 빌려줌 (API 함수에서 사용)
    - finally: API 함수가 끝나면 db.close()로 세션 닫기

    쉽게 말해: "DB 연결을 빌려주고, 다 쓰면 자동으로 반납"
    """
    db = SessionLocal()
    try:
        yield db       # db를 빌려줌
    finally:
        db.close()     # 다 쓰면 반납
```

### 핵심 개념 요약

| 개념 | 비유 | 설명 |
|------|------|------|
| Engine | 전화번호 | DB 연결 정보를 가지고 있음 |
| Session | 은행 창구 | 하나의 작업 단위. 명령 실행, 확정, 취소 담당 |
| Base | 설계 도면 틀 | 모든 테이블 모델이 이걸 상속받아야 함 |
| get_db() | 창구 번호표 | 요청마다 세션을 빌려주고, 끝나면 반납 |


## 7. DB 연결 확인

### app/main.py 수정

```python
from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI(title="SYJ API")

# 서버 시작 시 테이블 생성
# → Base를 상속받은 모든 모델을 찾아서 DB에 테이블을 만듦
# ⚠️ 주의: 이미 있는 테이블은 건드리지 않음.
#    나중에 모델을 수정하면 sql_app.db 파일을 삭제하고 서버를 재시작해야 합니다.
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}
```

서버를 실행하면 프로젝트 루트에 `sql_app.db` 파일이 생성됩니다.

> **주의:** 모델(테이블 구조)을 수정한 경우, `sql_app.db` 파일을 삭제하고 서버를 다시 시작하세요.
> `Base.metadata.create_all()`은 새 테이블만 만들고, 기존 테이블은 수정하지 않습니다.


## 8. SQLite 웹 뷰어로 DB 직접 확인하기

API로 데이터를 넣고 나면 "진짜 DB에 들어갔나?" 궁금할 때가 있습니다.
**sqlite-web**을 사용하면 브라우저에서 테이블 구조를 보고, SQL을 직접 실행할 수 있습니다.

### 실행 방법

FastAPI 서버와 **별도 터미널**에서 실행합니다:

```bash
# 가상환경 활성화 후
sqlite_web sql_app.db --port 8080
```

- `sql_app.db` → 조회할 DB 파일
- `--port 8080` → 8080 포트에서 실행 (FastAPI가 8000을 쓰고 있으므로)

브라우저에서 http://127.0.0.1:8080 접속하면 됩니다.

### 할 수 있는 것

| 기능 | 설명 |
|------|------|
| 테이블 목록 | 어떤 테이블이 있는지 한눈에 확인 |
| 테이블 구조 | 컬럼명, 타입, 제약조건 확인 |
| Content 탭 | 저장된 데이터를 엑셀처럼 조회 |
| Query 탭 | SQL을 직접 입력하고 실행 |

### SQL 직접 실행해보기

Query 탭에서 아래 SQL을 입력해보세요:

```sql
-- 모든 유저 조회
SELECT * FROM users;

-- 이름이 '홍길동'인 유저만 조회
SELECT * FROM users WHERE name = '홍길동';

-- 유저 수 세기
SELECT COUNT(*) FROM users;
```

> **팁:** API(Swagger)로 데이터를 추가한 뒤, sqlite-web에서 SELECT를 실행하면
> "API → DB → SQL 조회"의 전체 흐름을 눈으로 확인할 수 있습니다.


## 실습 과제

1. 서버를 실행하고 `/health` API를 Swagger에서 호출해보세요.
2. `sql_app.db` 파일이 생성되었는지 확인하세요.
3. `--reload` 옵션의 효과를 확인해보세요: `health_check`의 응답 메시지를 바꾼 뒤 저장하면 자동으로 반영되는지 확인.
4. sqlite-web을 실행하고 `SELECT * FROM users;`를 Query 탭에서 실행해보세요.


## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| WAS | 동적 요청을 처리하는 서버 (uvicorn) |
| FastAPI | Python 웹 프레임워크 (API 로직 작성) |
| uvicorn | FastAPI를 실행해주는 서버 프로그램 |
| 데코레이터(@) | 함수에 특별한 기능을 추가하는 표시 |
| Request/Response | 클라이언트가 보내는 요청, 서버가 보내는 응답 |
| SQLAlchemy (ORM) | SQL 대신 Python 코드로 DB를 다루는 라이브러리 |
| SQLite | 파일 하나로 동작하는 가벼운 데이터베이스 |
| Session | DB와 대화하는 창구 (작업 단위) |
| yield | "빌려주고, 다 쓰면 반납" 패턴 |
| trace_id | 요청별 고유 ID, 로그에서 같은 요청의 흐름을 추적 |
| sqlite-web | SQLite DB를 브라우저에서 조회하고 SQL을 실행하는 도구 |
