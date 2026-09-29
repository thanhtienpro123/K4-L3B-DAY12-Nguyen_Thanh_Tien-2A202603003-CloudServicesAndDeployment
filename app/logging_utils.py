"""CP1 — Structured logging.

`print("user abc hỏi gì đó")` là log cho người đọc. Cloud (Railway, Render,
Cloud Run, Datadog...) đọc log bằng máy: một dòng = một JSON object thì mới
lọc/đếm/cảnh báo được. Đây là khác biệt lớn giữa localhost và production.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone


def utc_now_iso() -> str:
    """CHO SẴN — thời điểm hiện tại theo ISO-8601, múi giờ UTC."""
    return datetime.now(timezone.utc).isoformat()


def log_event(event: str, level: str = "info", **fields) -> str:
    """Ghi một dòng log JSON ra stdout.

    Tạo payload ít nhất gồm event, level và timestamp, rồi gộp thêm mọi field
    phụ được truyền vào. JSON phải nằm trên một dòng duy nhất để cloud log có
    thể parse theo từng dòng.
    """
    payload = {
        "event": event,
        "level": str(level).lower(),
        "timestamp": utc_now_iso(),
    }
    payload.update(fields)
    line = json.dumps(payload, ensure_ascii=False)
    print(line)
    return line
