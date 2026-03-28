# 사전 세팅: 개발 환경 설정

> 수업 시작 전에 아래 환경을 미리 준비해주세요.


## 0. 터미널(Terminal) 열기

터미널은 컴퓨터에게 텍스트로 명령을 내리는 프로그램입니다.
이 수업에서 모든 명령어는 터미널에서 실행합니다.

| OS | 여는 방법 |
|----|----------|
| macOS | `Cmd + Space` → "터미널" 검색 → 실행 |
| Windows | `Win키` → "cmd" 또는 "PowerShell" 검색 → 실행 |

### 자주 쓰는 터미널 명령어

| 명령어 | 의미 | 예시 |
|--------|------|------|
| `cd 폴더이름` | 해당 폴더로 이동 (Change Directory) | `cd Desktop` |
| `ls` (macOS) / `dir` (Windows) | 현재 위치의 파일 목록 보기 | `ls` |
| `python --version` | Python 버전 확인 | |


## 1. Python 3.11 설치

> Python 3.10 이상이면 수업 진행 가능합니다. 3.11을 권장합니다.

### macOS

macOS에서는 **Homebrew**라는 패키지 관리자를 사용합니다.
Homebrew가 없다면 먼저 설치하세요:

```bash
# Homebrew 설치 (이미 있으면 생략)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 설치
brew install python@3.11
```

### Windows

1. https://www.python.org/downloads/ 에서 3.11.x 다운로드
2. 설치 시 **"Add Python to PATH"** 반드시 체크!
   - PATH란? → 터미널에서 `python`이라고 입력했을 때 컴퓨터가 Python을 찾을 수 있게 해주는 설정입니다.
   - 이걸 체크하지 않으면 터미널에서 `python` 명령이 동작하지 않습니다.

### 설치 확인

```bash
python --version
# Python 3.11.x 이 나오면 성공!
```


## 2. IDE 설치

IDE(통합 개발 환경)는 코드를 작성하는 프로그램입니다.
메모장으로도 코드를 쓸 수 있지만, IDE는 자동완성, 오류 표시 등 편리한 기능을 제공합니다.

아래 중 하나를 선택합니다. **VSCode를 추천합니다.**

| IDE | 다운로드 |
|-----|----------|
| VSCode (추천) | https://code.visualstudio.com/ |
| PyCharm | https://www.jetbrains.com/pycharm/ |

VSCode를 사용할 경우, 설치 후 왼쪽 Extensions 탭에서 **"Python"** 을 검색하여 설치하세요.


## 3. 가상환경 생성 및 패키지 설치

### 가상환경이란?

프로젝트마다 독립된 Python 환경을 만드는 것입니다.

```
왜 필요할까?

프로젝트 A는 fastapi 버전 1.0이 필요
프로젝트 B는 fastapi 버전 2.0이 필요

→ 하나의 Python에 둘 다 설치하면 충돌!
→ 프로젝트마다 가상환경을 만들면 각각 독립적으로 관리 가능
```

### 설치 순서

```bash
# 1. 프로젝트 폴더로 이동
cd syj

# 2. 가상환경 생성
#    python -m venv venv
#    → "venv라는 이름의 가상환경을 만들어라"
python -m venv venv

# 3. 가상환경 활성화 (매번 터미널을 열 때마다 실행!)
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 활성화되면 터미널 앞에 (venv) 가 붙습니다:
# (venv) $ ← 이렇게 보이면 성공!

# 4. 패키지(라이브러리) 설치
#    pip = Python 패키지 관리 도구 (앱스토어 같은 것)
pip install -r requirements.txt
```

### requirements.txt 내용

이 파일은 프로젝트에 필요한 패키지 목록입니다.

```
fastapi                      # 웹 API를 만드는 프레임워크
uvicorn[standard]            # FastAPI를 실행해주는 서버
sqlalchemy                   # 데이터베이스를 Python 코드로 다루는 도구
bcrypt                       # 비밀번호를 안전하게 암호화
python-jose[cryptography]    # JWT 토큰 생성/검증
```

> `[standard]`, `[cryptography]`는 "추가 기능도 함께 설치해라"라는 뜻입니다.


## 4. 서버 실행 확인

```bash
uvicorn app.main:app --reload
```

이 명령어의 의미:
- `uvicorn` → 서버 실행 프로그램
- `app.main` → `app` 폴더 안의 `main.py` 파일
- `:app` → 그 파일 안에 있는 `app` 이라는 변수
- `--reload` → 코드를 수정하면 자동으로 서버 재시작

브라우저에서 http://127.0.0.1:8000/docs 접속 → Swagger UI(API 테스트 화면)가 보이면 성공!


## 프로젝트 구조 (최종)

수업이 끝나면 아래와 같은 구조가 됩니다.
**도메인별 패키지 구조**로, 관련 코드를 한 폴더에 모아서 관리합니다.

```
syj/
├── app/                       # 소스 코드 폴더
│   ├── __init__.py            # "이 폴더는 Python 패키지입니다" 표시 (빈 파일)
│   ├── main.py                # FastAPI 앱 시작점 (미들웨어, 에러 핸들러, 라우터 등록)
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

> **도메인별 구조란?** 기능별(routers/, services/)이 아니라, 관련 코드를 도메인(user/, post/)으로 묶는 방식입니다.
> user 관련 코드를 보려면 `app/user/` 폴더만 보면 됩니다. (자세한 설명은 2회차 문서 참고)


## 용어 사전

이 수업에서 자주 나오는 용어입니다. 모르는 단어가 나오면 여기를 참고하세요.

| 용어 | 설명 |
|------|------|
| API | 프로그램끼리 데이터를 주고받는 규칙/통로 |
| 서버 | 요청을 받아서 처리하고 응답을 돌려주는 프로그램 |
| 클라이언트 | 서버에 요청을 보내는 쪽 (브라우저, 앱 등) |
| DB (Database) | 데이터를 저장하는 저장소 |
| ORM | 데이터베이스를 SQL 대신 Python 코드로 다루는 기술 |
| CRUD | Create(생성), Read(조회), Update(수정), Delete(삭제) |
| JWT | 로그인 상태를 유지하기 위한 토큰(인증표) |
| DTO / 스키마 | API로 주고받는 데이터의 형식을 정의한 것 |
| 라우터 (Router) | 특정 URL에 대한 API들을 모아놓은 모듈 |
| 의존성 주입 (DI) | 함수가 필요한 것을 자동으로 넣어주는 패턴 |
| 해싱 (Hashing) | 원본을 복원할 수 없게 변환하는 것 (비밀번호 보호용) |
| 미들웨어 | 모든 요청/응답에 공통으로 적용되는 처리 |
