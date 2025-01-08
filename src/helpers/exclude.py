from typing import Any

from tortoise import Model
from tortoise.queryset import QuerySet


def remove_excludes(
    query: QuerySet | list[dict[str, Any]],
    model: Model,
    exclude: list,
    allowed_fields: list[str] = None,
):
    if isinstance(query, QuerySet):
        return query.values(
            *[
                field
                for field in (allowed_fields or model._meta.fields_map.keys())
                if field not in exclude
                and not hasattr(
                    model._meta.fields_map[field],
                    "related_model",
                )
                and not hasattr(model._meta.fields_map[field], "related_objects")
            ]
        )
    if isinstance(query, model):
        print(getattr(query, "id"), model._meta.fields_map.keys())
        return {
            key: getattr(query, key)
            for key in (allowed_fields or model._meta.fields_map.keys())
            if key not in exclude
            and not hasattr(
                model._meta.fields_map[key],
                "related_model",
            )
            and not hasattr(model._meta.fields_map[key], "related_objects")
        }
    return [
        [
            getattr(item, key) if hasattr(item, key) else item[key]
            for key in (allowed_fields or model._meta.fields_map.keys())
            if key not in exclude
        ]
        for item in query
    ]
