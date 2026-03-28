import logging
from contextvars import ContextVar

# 요청별 고유 ID — 같은 요청 안에서 미들웨어 로그와 SQL 로그를 묶어서 추적
trace_id_ctx: ContextVar[str] = ContextVar("trace_id", default="-")


class TraceIdFilter(logging.Filter):
    """로그 레코드에 trace_id를 자동 주입하는 필터"""
    def filter(self, record):
        record.trace_id = trace_id_ctx.get()
        return True
