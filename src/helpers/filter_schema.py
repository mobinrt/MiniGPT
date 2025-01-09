from typing import Any, Optional, Type
from fastapi import Query
from pydantic import BaseModel, create_model
from tortoise.models import Model
from tortoise.fields.relational import ManyToManyRelation

FILTER_OPERATIONS = [
    "exact",
    "contains",
    "startswith",
    "endswith",
    "gte",
    "lte",
    "in",
]


def get_python_type(field):
    if hasattr(field, "field_type"):
        return field.field_type
    elif hasattr(field, "PythonType"):
        return field.PythonType
    elif isinstance(field, ManyToManyRelation):
        return ManyToManyRelation
    else:
        return str


def create_filter_schema(
    model: Type[Model],
    excludes: list[str] | None = None,
    includes: list[dict[str, tuple[type, Any]]] | None = None,
    filter_operations: list[str] | None = None,
) -> Type[BaseModel]:
    excludes = excludes or[]
    fields = {  # Simple Fields
        f"{field_name}{op}": (
            Optional[get_python_type(field)],
            Query(None),
        )
        for field_name, field in model._meta.fields_map.items()
        if field_name not in excludes
        and not hasattr(field, "related_model")
        and not hasattr(field, "offset")
        for op in (filter_operations or FILTER_OPERATIONS)
    }
    fields.update(  # Related Models
        **{
            f"{field_name}_id{op}": (
                Optional[int],
                Query(None),
            )
            for field_name, field in model._meta.fields_map.items()
            if field_name not in excludes
            and hasattr(field, "related_model")
            and not hasattr(field, "related_objects")
            for op in (filter_operations or FILTER_OPERATIONS)
        }
    )
    fields.update(  # Related Models (No ManyToManyRelation)
        **{
            f"{field_name}_id": (
                Optional[int],
                Query(None),
            )
            for field_name, field in model._meta.fields_map.items()
            if field_name not in excludes
            and hasattr(field, "related_model")
            and get_python_type(field) is not ManyToManyRelation
        }
    )
    fields.update(  # Custom Fields
        {
            f"{field_name}__{op}": (
                type_,
                field_,
            )
            for field_name, type_, field_ in includes or []
            for op in (filter_operations or FILTER_OPERATIONS)
        }
    )
    fields.update(  # Basic Fields
        {
            f"{field_name}": (
                Optional[get_python_type(field)],
                Query(None),
            )
            for field_name, field in model._meta.fields_map.items()
            if field_name not in excludes
            and get_python_type(field) is not ManyToManyRelation
        }
    )
    fields.update(  # includes
        **{
            f"{field_name}": (
                type_,
                default_,
            )
            for field_name, type_, default_ in includes or []
        }
    )
    return create_model(f"{model.__name__}FilterSchema", **fields)
