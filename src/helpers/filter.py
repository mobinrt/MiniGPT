from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from pydantic import BaseModel

from tortoise.queryset import QuerySet


class Filter:
    def __init__(self):
        self.data: Dict[str, Any] = {}

    def _add(self, field_name: str, operator: Optional[str], value: Any):
        if value is not None:
            key = f"{field_name}__{operator}" if operator else field_name
            self.data[key] = value

    def _apply(self, query: QuerySet):
        return query.filter(**self.data)

    @staticmethod
    def create(
        query: QuerySet, filters: BaseModel, exclude: Optional[List[str]] = None
    ):
        filter_obj = Filter()
        exclude = exclude or []
        for field_with_op, value in filters.model_dump(exclude_none=True).items():
            try:
                field, operator = (field_with_op.split("__") + [None])[:2]
                if field in exclude:
                    continue
                filter_obj._add(field, operator, value)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail=f"Invalid filter format: {field_with_op}"
                )
        return filter_obj._apply(query)
