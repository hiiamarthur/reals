import logging
from typing import TypeVar, Type, List, Optional, Dict
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.query_schema import QueryParams
from app.core.database import get_async_db
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import DeclarativeMeta
from typing import Generic
from sqlalchemy import inspect, select

logger = logging.getLogger(__name__)

M = TypeVar("M", bound=DeclarativeMeta)


class DataController(Generic[M]):
    def __init__(self, model: Type[M], db: AsyncSession):
        self.model = model
        self.db = db
        self.repository = BaseRepository(model, db)
        # Get all valid relationship names for this model
        self.valid_relationships = [rel.key for rel in inspect(model).relationships]

    async def create(self, data_dict: dict) -> M:
        """Handle create request"""
        logger.info(f"Creating new {self.model.__name__} item")
        try:
            # Basic validation
            if not data_dict:
                raise HTTPException(
                    status_code=400, detail="Create data cannot be empty"
                )

            # Validate fields exist in model
            valid_fields = set(self.model.__mapper__.attrs.keys())
            invalid_fields = set(data_dict.keys()) - valid_fields
            if invalid_fields:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid fields: {', '.join(invalid_fields)}",
                )

            # Delegate to repository
            try:
                result = await self.repository.create(data_dict)
                await self.db.refresh(result)
                return result
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    async def get_by_id(self, id: int, select: List[str] = None) -> M:
        try:
            # result = await self.repository.get_first(
            #     {"filter_by[uuid][equals]": id}, select
            # )
            result = await self.repository.get_by_id(id, select)
            if not result:
                raise HTTPException(status_code=404, detail="Record not found")
            return result
        except Exception as e:
            logger.error(f"Error getting item: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all(self, query_params: QueryParams) -> List[M]:
        """Get all records with pagination and filters"""
        try:
            # Validate requested relationships
            # if query_params.select:
            #     invalid_relations = [
            #         rel
            #         for rel in query_params.select
            #         if rel not in self.valid_relationships
            #     ]
            #     if invalid_relations:
            #         raise HTTPException(
            #             status_code=400,
            #             detail=f"Invalid relationships requested: {', '.join(invalid_relations)}. Valid relationships are: {', '.join(self.valid_relationships)}",
            #         )

            result = await self.repository.get_all(
                page=query_params.page,
                items_per_page=query_params.items_per_page,
                order_by=query_params.order_by,
                order_type=query_params.order_type,
                filter_by=query_params.filter_by,
                # search_by=query_params.search_by,
                select_list=query_params.select,
                group_by=query_params.group_by,
            )
            return result
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} items: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    async def delete(self, id: str) -> bool:
        try:
            print("delete", id)
            result = await self.repository.delete(id)
            if not result:
                raise HTTPException(status_code=404, detail="Record not found")
            return result
        except Exception as e:
            logger.error(f"Error deleting item: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def update(self, id: str, data_dict: dict) -> M:
        """Update a record with nested relationships"""
        logger.info(f"Updating {self.model.__name__} with id {id}")
        # try:
        #     # Validate that update data is not empty
        #     if not data_dict:
        #         raise HTTPException(
        #             status_code=400, detail="Update data cannot be empty"
        #         )

        #     # First get the existing record
        #     result = await self.db.execute(
        #         select(self.model).where(self.model.id == int(id))
        #     )
        #     existing_record = result.scalar_one_or_none()

        #     if not existing_record:
        #         raise HTTPException(status_code=404, detail="Record not found")

        #     # ✅ Handle nested relationships
        #     for relationship in self.model.__mapper__.relationships:
        #         if relationship.key in data_dict:
        #             related_data = data_dict.pop(relationship.key)
        #             related_model = relationship.mapper.class_

        #             if isinstance(related_data, dict):
        #                 # Handle one-to-one relationship
        #                 existing_related = getattr(existing_record, relationship.key)
        #                 if existing_related:
        #                     # Update existing related record
        #                     for key, value in related_data.items():
        #                         if hasattr(existing_related, key):
        #                             setattr(existing_related, key, value)
        #                 else:
        #                     # Create new related record
        #                     setattr(
        #                         existing_record,
        #                         relationship.key,
        #                         related_model(**related_data),
        #                     )

        #     # ✅ Update main fields
        #     for key, value in data_dict.items():
        #         if hasattr(existing_record, key):
        #             setattr(existing_record, key, value)

        #     # Commit changes in a single transaction
        #     try:
        #         await self.db.commit()
        #         await self.db.refresh(existing_record)
        #         return existing_record
        #     except Exception as e:
        #         await self.db.rollback()
        #         raise HTTPException(status_code=400, detail=str(e))

        # except HTTPException:
        #     raise
        # except Exception as e:
        #     await self.db.rollback()
        #     logger.error(f"Error updating {self.model.__name__}: {str(e)}")
        #     raise HTTPException(status_code=400, detail=str(e))

        try:
            # Reflect the table and get its columns
            # model_inspect = inspect(self.model)
            # columns = model_inspect.columns

            # # Fetch the model instance by id
            # result = await self.db.execute(select(self.model).filter_by(id=int(id)))
            # instance = result.scalar_one_or_none()

            # if not instance:
            #     raise Exception(f"{self.model.__name__} with id {id} not found")

            # # Update simple fields (based on column names)
            # for key, value in data_dict.items():
            #     if key in columns:
            #         setattr(instance, key, value)

            # # Handle nested relationships (assuming the relationships are passed as dictionaries)
            # for relation_name, related_data in data_dict.items():
            #     if isinstance(
            #         related_data, list
            #     ):  # if the value is a list, it likely represents related items
            #         relation = getattr(self.model, relation_name, None)
            #         if relation:
            #             for related_item in related_data:
            #                 related_model = relation.property.mapper.class_
            #                 related_instance = await self.db.execute(
            #                     select(related_model).filter_by(id=related_item["id"])
            #                 )
            #                 related_instance = related_instance.scalar_one_or_none()

            #                 if related_instance:
            #                     # Update the related instance's fields
            #                     for key, value in related_item.items():
            #                         if key in inspect(related_model).columns:
            #                             setattr(related_instance, key, value)
            #                     self.db.add(related_instance)

            # # Add the updated main instance to the session
            # self.db.add(instance)
            # await self.db.commit()  # Ensure to await commit

            # Return the updated instance
            # return instance
            result = await self.repository.update(id, data_dict)
            return result
        except Exception as e:
            await self.db.rollback()  # Ensure to rollback in case of an error
            raise e
