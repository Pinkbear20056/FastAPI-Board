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
3 tier architecture