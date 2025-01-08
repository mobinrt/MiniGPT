from typing import List
from tortoise.queryset import QuerySet
from fastapi import HTTPException


class OrderBy:
    def __init__(self):
        self.data: List[str] = []

    def add(self, field: str):
        self.data.add(field)

    def apply(self, query: QuerySet):
        return query.order_by(*self.data)

    @staticmethod
    def create(
        query: QuerySet,
        sort_by: List[str],
        exclude: List[str] = None,
        allowed_fields: List[str] = None,
    ):
        order_obj = OrderBy()
        exclude = exclude or []
        for field in sort_by:
            try:
                if (
                    field.lstrip("-").split("__")[0] in exclude
                    or field.lstrip("-") in exclude
                ):
                    continue
                if allowed_fields and field.lstrip("-") in allowed_fields:
                    continue
                order_obj.add(field)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail=f"Invalid order format: {field}"
                )
        return order_obj.apply(query)
