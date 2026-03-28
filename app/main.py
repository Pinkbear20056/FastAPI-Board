import time
import uuid
import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from uvicorn.logging import ColourizedFormatter, AccessFormatter

from app.context import trace_id_ctx, TraceIdFilter
from app.database import engine, Base
from app.auth.auth_router import router as auth_router
from app.user.user_router import router as user_router

logger = logging.getLogger("uvicorn")

app = FastAPI(title="SYJ API")


@app.on_event("startup")
def setup_logging():
    """
    로깅 설정: trace_id 자동 주입.
    uvicorn이 핸들러를 모두 생성한 뒤(startup 시점)에 Filter + Formatter를 등록한다.
    "uvicorn.error" 로거에 핸들러가 있으므로 그쪽에 등록해야 한다.
    → 서비스마다 _log() 메서드를 만들 필요 없이 logger.info()만 쓰면 됨
    """
    trace_filter = TraceIdFilter()
    fmt = "%(levelprefix)s [%(trace_id)s] %(message)s"

    for name in ("uvicorn", "uvicorn.error"):
        for handler in logging.getLogger(name).handlers:
            handler.addFilter(trace_filter)
            handler.setFormatter(ColourizedFormatter(fmt))

    for handler in logging.getLogger("uvicorn.access").handlers:
        handler.addFilter(trace_filter)
        handler.setFormatter(AccessFormatter(fmt))

# 서버 시작 시 Base를 상속한 모든 모델의 테이블을 생성 (이미 존재하면 스킵)
Base.metadata.create_all(bind=engine)


# ── 미들웨어: 요청 로깅 ──
# app.middleware로 등록하면 모든 요청에 전역으로 적용됨 (라우터 무관)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    trace_id = uuid.uuid4().hex[:8]  # 요청마다 8자리 고유 ID 생성
    trace_id_ctx.set(trace_id)
    logger.info(f"{request.method} {request.url.path} ← 요청 시작")
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(
        f"{request.method} {request.url.path} → {response.status_code} ({duration:.3f}s)"
    )
    return response


# ── 에러 핸들러 ──
# app.exception_handler로 등록하면 모든 라우터에서 발생하는 예외를 전역으로 처리
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.status_code, "message": exc.detail}},
    )


# Pydantic 검증 실패 시 발생 (예: EmailStr 형식 불일치, 필수 필드 누락 등)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": 400,
                "message": "입력값이 올바르지 않습니다.",
                "details": str(exc),
            }
        },
    )


# ── 라우터 등록 ──
app.include_router(auth_router)
app.include_router(user_router)


# ── API ──
@app.get("/")
def root():
    return {"message": "Hello, SYJ!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
