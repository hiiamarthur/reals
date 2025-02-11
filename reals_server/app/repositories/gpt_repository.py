from app.repositories.base_repository import BaseRepository
from app.models.gpt_model import (
    APIUsage,
    Message,
    Session,
    APIRequestLog,
    APIUsageFilter,
    MessageFilter,
    SessionFilter,
    APIRequestLogFilter,
)
from sqlalchemy import inspect
import logging
from typing import (
    List,
    Optional,
    Type,
    TypeVar,
    Generic,
    Dict,
    Any,
    get_type_hints,
    ParamSpec,
    Concatenate,
    Unpack,
    overload,
    TypedDict,
)
from enum import Enum
from dataclasses import dataclass, make_dataclass
from uuid import UUID

from app.models.base_model import (
    BaseModel,
    FilterType,
)
from app.models.enums import MessageRole

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
P = ParamSpec("P")
APIUsageT = TypeVar("APIUsageT", bound="APIUsage")
MessageT = TypeVar("MessageT", bound="Message")
SessionT = TypeVar("SessionT", bound="Session")
APIRequestLogT = TypeVar("APIRequestLogT", bound="APIRequestLog")


@dataclass
class ModelInfo:
    """Holds model metadata"""

    model: Type[T]
    table_name: str
    columns: Dict[str, Type]
    primary_keys: List[str]
    relationships: Dict[str, Type]


class GPTRepository:
    def __init__(self, db):
        self.db = db
        self._repos: Dict[Type, BaseRepository] = {}
        self._filter_types: Dict[Type, Type] = {}

        # Initialize filter types using reflection
        for model in [Session, Message, APIUsage, APIRequestLog]:
            self._init_model(model)

    def _init_model(self, model: Type) -> None:
        """Initialize repository and filter type for a model"""
        mapper = inspect(model)
        fields = [
            (column.key, Optional[column.type.python_type], None)
            for column in mapper.columns
        ]

        filter_type = make_dataclass(
            f"{model.__name__}Filters", fields, frozen=True, slots=True
        )

        self._filter_types[model] = filter_type
        self._repos[model] = BaseRepository(self.db, model)

    def _get_model_info(self, model: Type[T]) -> ModelInfo:
        """Extract model metadata using reflection"""
        mapper = inspect(model)

        # Get column info
        columns = {column.key: column.type.python_type for column in mapper.columns}

        # Get primary keys
        primary_keys = [key.name for key in mapper.primary_key]

        # Get relationships
        relationships = {rel.key: rel.mapper.class_ for rel in mapper.relationships}

        return ModelInfo(
            model=model,
            table_name=mapper.mapped_table.name,
            columns=columns,
            primary_keys=primary_keys,
            relationships=relationships,
        )

    def _validate_filters(self, model: Type[T], filters: Dict[str, Any]) -> None:
        """Validate filter keys against model columns"""
        model_info = self._get_model_info(model)
        valid_fields = set(model_info.columns.keys()) | set(
            model_info.relationships.keys()
        )
        invalid_fields = set(filters.keys()) - valid_fields

        if invalid_fields:
            raise ValueError(
                f"Invalid filters for {model_info.table_name}: {invalid_fields}. "
                f"Valid fields are: {valid_fields}"
            )

    @overload
    async def get(
        self, model: Type[Session], **filters: Unpack[SessionFilter]
    ) -> Optional[Session]: ...

    @overload
    async def get(
        self, model: Type[Message], **filters: Unpack[MessageFilter]
    ) -> Optional[Message]: ...

    @overload
    async def get(
        self, model: Type[APIUsage], **filters: Unpack[APIUsageFilter]
    ) -> Optional[APIUsage]: ...

    @overload
    async def get(
        self, model: Type[APIRequestLog], **filters: Unpack[APIRequestLogFilter]
    ) -> Optional[APIRequestLog]: ...

    async def get(self, model: Type[T], /, **filters: Any) -> Optional[T]:
        """Get single record with type-safe return"""
        filter_types = {
            Session: SessionFilter,
            Message: MessageFilter,
            APIUsage: APIUsageFilter,
            APIRequestLog: APIRequestLogFilter,
        }

        filter_type = filter_types[model]
        validated_filters = filter_type(**filters)
        repo = self._repos[model]
        results = await repo.get_by_filters(**vars(validated_filters))
        return results[0] if results else None

    async def get_all(self, model: Type[T], **filters) -> List[T]:
        """Get all records with dynamic filter validation"""
        try:
            if model not in self._filter_types:
                raise ValueError(f"Unsupported model: {model}")

            # Validate filters using the dynamically created filter type
            filter_type = self._filter_types[model]
            validated_filters = filter_type(**filters)

            repo = self._repos[model]
            return await repo.get_by_filters(**vars(validated_filters))

        except Exception as e:
            logger.error(f"Error getting all {model.__name__}: {e}")
            raise

    async def create(self, model: Type[T], **data) -> T:
        """Create with validation"""
        try:
            if model not in self._filter_types:
                raise ValueError(f"Unsupported model: {model}")

            # Validate filters using the dynamically created filter type
            filter_type = self._filter_types[model]
            validated_filters = filter_type(**data)

            repo = self._repos[model]
            return await repo.create(**vars(validated_filters))

        except Exception as e:
            logger.error(f"Error creating {model.__name__}: {e}")
            raise


# class SessionRepository(BaseRepository[Session]):
#     async def get_by_filters(self, **filters: Unpack[SessionFilter]) -> List[Session]:
#         return await super().get_by_filters(**filters)

#     async def get_first(self, **filters: Unpack[SessionFilter]) -> Optional[Session]:
#         return await super().get_first(**filters)

#     async def get_all(
#         self, skip: int = 0, limit: int = 100, **filters: Unpack[SessionFilter]
#     ) -> List[Session]:
#         return await super().get_all(skip, limit, **filters)
