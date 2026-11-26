"""Simple in-memory rate limiter for local/dev. Replace with Redis at scale."""

from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

WINDOW = 60
LIMITS = {
    "default": 120,
    "auth": 30,
    "coach": 40,
}


_hits: dict[str, deque[float]] = defaultdict(deque)


def rate_limit(bucket: str = "default"):
    limit = LIMITS.get(bucket, LIMITS["default"])

    async def _dep(request: Request) -> None:
        key = f"{bucket}:{request.client.host if request.client else 'anon'}"
        now = time.time()
        q = _hits[key]
        while q and now - q[0] > WINDOW:
            q.popleft()
        if len(q) >= limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        q.append(now)

    return _dep
