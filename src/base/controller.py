from tortoise.exceptions import DoesNotExist
from typing import Type, TypeVar, Generic, Sequence

from src.base.model import BaseModel
from src.helpers.exceptions.entities import NotFoundError

TModel = TypeVar("ModelType", bound="BaseModel")


class BaseController(Generic[TModel]):
    def __init__(self, model: Type[TModel]):
        self.model = model

    async def create(self, **kwargs):
        instance = await self.model.create(**kwargs)
        return instance


    async def get_by_id(self, id: int) -> TModel:
        try:
            instance = await self.model.get(id=id)
            return instance
        except DoesNotExist:
            raise NotFoundError()

    async def get_entities(self) -> Sequence[TModel]:
        try:
            return await self.model.all()
        except DoesNotExist:
            raise NotFoundError()

    async def update(self, id: int, data: dict) -> TModel:
        instance = await self.get_by_id(id)
        for field, value in data.items():
            setattr(instance, field, value)
        await instance.save()
        return instance

    async def delete(self, id: int):
        instance = await self.get_by_id(id)
        await instance.delete()
