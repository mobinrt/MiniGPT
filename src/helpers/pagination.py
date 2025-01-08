from functools import wraps
from typing import Callable, Generic, List, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from tortoise.queryset import QuerySet, ValuesQuery

T = TypeVar("T")


class Paginated(BaseModel, Generic[T]):
    total: int
    pages: int
    page: int
    limit: int
    data: List[T]

    class Config:
        extra = "allow"


class BasePaginator:
    def __init__(
        self,
        limit: int = 10,
        page: int = 1,
    ) -> None:
        self.limit = limit
        self.page = page
        self.paginated_result = []
        self.total = 0
        self.pages = 1
        self.page = 1

    def paginate(self, result, serializer_class: Callable | None = None):
        self.result = result
        self.serializer_class = serializer_class
        return self.result


class Paginator(BasePaginator):
    async def paginate(self, result, serializer_class: Callable | None = None):
        self.result = result
        self.serializer_class = serializer_class
        if isinstance(self.result, (list, tuple)):
            await self.paginate_iterable()

        if isinstance(self.result, QuerySet):
            self.is_query_set = True
            await self.paginate_queryset()

        else:
            self.total = len(self.result)
            self.pages = 1
            self.page = 1
            self.paginated_result = self.result

        return self

    async def get_paginated_response(self, paginated_result):
        return {
            "total": self.total,
            "pages": self.pages,
            "page": self.page,
            "limit": self.limit,
            "data": (
                await paginated_result
                if isinstance(paginated_result, (QuerySet, ValuesQuery))
                else paginated_result
            ),
        }

    async def paginate_queryset(self):
        self.total = await self.result.count()
        if self.total == 0:
            self.pages = 1
            self.paginated_result = self.result.all()
            return
        self.pages = (self.total + self.limit - 1) // self.limit

        if self.page > self.pages:
            raise HTTPException(
                status_code=400, detail="Page number exceeds total pages"
            )
        offset = (self.page - 1) * self.limit
        self.paginated_result = self.result.offset(offset).limit(self.limit)

    async def paginate_iterable(self) -> None:
        self.total = len(self.result)
        if self.total == 0:
            self.pages = 1
            self.paginated_result = self.result
            return
        self.pages = (self.total + self.limit - 1) // self.limit

        if self.page > self.pages:
            raise HTTPException(
                status_code=400, detail="Page number exceeds total pages"
            )

        offset = (self.page - 1) * self.limit
        self.paginated_result = self.result[offset : offset + self.limit]


def paginate(limit: int = 10, page: int = 1, paginator: BasePaginator = Paginator):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            page_value = kwargs.get("page", page)
            limit_value = kwargs.get("limit", limit)

            result = await func(*args, **kwargs)

            return await paginator(result, limit_value, page_value).paginate()

        return wrapper

    return decorator
