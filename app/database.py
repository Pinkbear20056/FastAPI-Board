import logging

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger("uvicorn")

# sqlite:/// (슬래시 3개) + 파일 경로 → 파일 기반 영구 저장
# sqlite:// (슬래시 2개, 경로 없음) → 메모리 DB (서버 종료 시 데이터 소멸)
DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    DATABASE_URL,
    # SQLite는 기본적으로 같은 스레드에서만 연결 사용을 허용함
    # FastAPI는 멀티스레드로 동작하므로 이 제한을 해제
    connect_args={"check_same_thread": False},
)


# SQL 쿼리 로그: 실행되는 SQL을 한 줄로 출력
@event.listens_for(engine, "before_cursor_execute")
def _log_sql(conn, cursor, statement, parameters, context, executemany):
    sql = " ".join(statement.split())  # 줄바꿈/탭 → 공백 한 칸으로 압축
    logger.info(f"SQL: {sql} | params: {parameters}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
