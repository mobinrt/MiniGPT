from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from time import time
from collections import defaultdict
from fastapi.responses import JSONResponse

from src.helpers.exceptions.rate_limit import RateLimitException

RATE_LIMIT = 5
TIME_WINDOW = 60

request_data = defaultdict(list)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            client_ip = request.client.host
            current_time = time()

            request_data[client_ip] = [
                timestamp
                for timestamp in request_data[client_ip]
                if timestamp > current_time - TIME_WINDOW
            ]

            if len(request_data[client_ip]) >= RATE_LIMIT:
                raise RateLimitException()

            request_data[client_ip].append(current_time)

            response = await call_next(request)
            return response
        except RateLimitException as exc:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": str(exc.detail)},
            )
