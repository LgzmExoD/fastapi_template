from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> ModelType | None:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, data: CreateSchemaType) -> ModelType:
        obj_data = jsonable_encoder(data)
        instance = self.model(**obj_data)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def update(
        self,
        db: AsyncSession,
        *,
        instance: ModelType,
        data: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(instance)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(instance, field, update_data[field])

        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType | None:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        instance = result.scalars().first()
        if instance:
            await db.delete(instance)
            await db.commit()
        return instance
