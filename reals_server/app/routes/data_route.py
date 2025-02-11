from typing import TypeVar, Optional, Type, List
from fastapi import APIRouter, Request, HTTPException, Depends, Query
import logging

from pydantic import BaseModel
from app.controllers.data_controller import DataController
from app.schemas.query_schema import QueryParams
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db

logger = logging.getLogger(__name__)

# M = TypeVar("M", bound=DeclarativeMeta)


def create_data_router(
    model: Type[BaseModel],
    prefix: str,
    tags: list[str],
    model_factory: Optional[callable] = None,
    # controller: Optional[Type[DataController]] = None,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)
    # controller = controller or DataController(model)

    def get_controller(db: AsyncSession = Depends(get_async_db)) -> DataController:
        return DataController(model, db)

    @router.post("")
    async def create_item(
        request: Request, controller: DataController = Depends(get_controller)
    ):
        try:
            data_dict = await request.json()
            result = await controller.create(data_dict)
            return result
        except Exception as e:
            logger.error(f"Error in create route: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/{id}")
    async def get_by_id(
        id: str, request: Request, controller: DataController = Depends(get_controller)
    ):
        query_params = QueryParams.from_query_params(dict(request.query_params))
        return await controller.get_by_id(id, query_params.select)

    @router.get("/")
    async def get_all(request: Request, db: AsyncSession = Depends(get_async_db)):
        query_params = QueryParams.from_query_params(dict(request.query_params))
        print("query_params", query_params)
        controller = DataController(model, db)
        return await controller.get_all(query_params)

    @router.delete("/{id}")
    async def delete(id: str, db: AsyncSession = Depends(get_async_db)):
        controller = DataController(model, db)
        return await controller.delete(id)

    @router.put("/{id}")
    async def update_item(
        id: str, request: Request, controller: DataController = Depends(get_controller)
    ):
        try:
            data_dict = await request.json()
            result = await controller.update(id, data_dict)
            return result
        except Exception as e:
            logger.error(f"Error in update route: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    return router
