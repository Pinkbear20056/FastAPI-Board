# Board-with-FastAPI
### 설명
FastAPI를 사용해 CRUD를 만족하는 게시판을 만들기
- Create: 게시글 작성
- Read: 게시글 조회 / 검색
- Upadate: 게시글 수정
- Delete: 게시글 삭제

User CRUD가 이미 존재하는 상태에서 **게시판만을** 추가하는 프로젝트입니다. 

### 설치 순서

```bash
# 1. 프로젝트 폴더로 이동
cd Board-with-FastAPI

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


### 서버 실행 확인

```bash
uvicorn app.main:app --reload
```

이 명령어의 의미:
- `uvicorn` → 서버 실행 프로그램
- `app.main` → `app` 폴더 안의 `main.py` 파일
- `:app` → 그 파일 안에 있는 `app` 이라는 변수
- `--reload` → 코드를 수정하면 자동으로 서버 재시작

브라우저에서 http://127.0.0.1:8000/docs 접속 → Swagger UI(API 테스트 화면)가 보이면 성공!

