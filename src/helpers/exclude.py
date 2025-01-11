from typing import Any, Union
from tortoise import Model
from tortoise.queryset import QuerySet


def remove_excludes(
    query: Union[QuerySet, list[Union[dict[str, Any], tuple]]],
    model: Model,
    exclude: list[str],
    allowed_fields: list[str] = None,
):
    if isinstance(query, QuerySet):
        return query.values(
            *[
                field
                for field in (allowed_fields or model._meta.fields_map.keys())
                if field not in exclude
                and not hasattr(model._meta.fields_map[field], "related_model")
                and not hasattr(model._meta.fields_map[field], "related_objects")
            ]
        )

    if isinstance(query, model):
        return {
            key: getattr(query, key)
            for key in (allowed_fields or model._meta.fields_map.keys())
            if key not in exclude
            and not hasattr(model._meta.fields_map[key], "related_model")
            and not hasattr(model._meta.fields_map[key], "related_objects")
        }

    results = []
    for item in query:
        if isinstance(item, dict):
            results.append({
                key: item[key]
                for key in (allowed_fields or model._meta.fields_map.keys())
                if key not in exclude and key in item
            })
        elif isinstance(item, model):
            results.append({
                key: getattr(item, key)
                for key in (allowed_fields or model._meta.fields_map.keys())
                if key not in exclude
            })
        elif isinstance(item, tuple):
            field_keys = allowed_fields or model._meta.fields_map.keys()
            results.append({
                key: item[i]
                for i, key in enumerate(field_keys)
                if key not in exclude and i < len(item)
            })
        else:
            raise TypeError(f"Unsupported item type: {type(item)}")

    return results
