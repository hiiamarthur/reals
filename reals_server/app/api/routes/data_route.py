from typing import Generic, TypeVar, Optional, Type
from fastapi import APIRouter, Query, Depends
from app.controllers.data_controller import DataController
from app.schemas.base_schema import BaseSchema
from app.schemas.query_schema import QueryParams

T = TypeVar("T", bound=BaseSchema)


class DataRoute(Generic[T]):
    def __init__(
        self,
        schema: Type[T],
        prefix: str,
        tags: list[str],
        controller: Optional[Type[DataController]] = None,
    ):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.controller = controller or DataController[T](schema)
        self.register_routes()

    def register_routes(self):
        @self.router.get("/{id}")
        async def get_by_id(id: str):
            return await self.controller.get_by_id(id)

        @self.router.get("/")
        async def get_all(query: QueryParams = Depends(QueryParams)):
            return await self.controller.get_all(query)

        @self.router.post("/")
        async def create(data: T):
            return await self.controller.create(data)

        @self.router.delete("/{id}")
        async def delete(id: str):
            return await self.controller.delete(id)

        @self.router.put("/{id}")
        async def update(id: str, data: T):
            return await self.controller.update(id, data)
