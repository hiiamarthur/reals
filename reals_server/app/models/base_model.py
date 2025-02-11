from datetime import datetime
import uuid as uuidLib
from typing import (
    Any,
    Dict,
    TypeVar,
    Type,
    TypedDict,
    Optional,
    ClassVar,
    get_type_hints,
    List,
    Set,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    class_mapper,
    RelationshipProperty,
)
from sqlalchemy import func, Column, Integer, inspect
from sqlalchemy.dialects.postgresql import UUID
from typing_extensions import TypedDict
import types
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.state import InstanceState
from sqlalchemy.orm.attributes import NO_VALUE

# from uuid import UUID
from app.models.enums import MessageRole
import logging

T = TypeVar("T")
FilterT = TypeVar("FilterT", bound=Dict[str, Any])

logger = logging.getLogger(__name__)


class FilterType(TypedDict, total=False):
    pass


class BaseModel(DeclarativeBase):
    # def __init__(cls, name, bases, dct):
    #     super().__init__(name, bases, dct)
    #     for attr_name, attr in dct.items():
    #         if isinstance(attr, relationship):
    #             # Use selectinload by default instead of lazy-loading
    #             attr.lazy = "selectin"

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Cache for filter types
    _filter_types: ClassVar[Dict[str, Type[FilterType]]] = {}

    @classmethod
    def get_filter_type(cls) -> Type[FilterType]:
        """Get or create TypedDict filter type for this model"""
        if cls.__name__ not in cls._filter_types:
            mapper = inspect(cls)
            annotations = {
                column.key: Optional[column.type.python_type]
                for column in mapper.columns
            }

            # Create a concrete filter type class
            filter_type = type(
                f"{cls.__name__}Filter",
                (FilterType,),
                {"__annotations__": annotations},
            )

            cls._filter_types[cls.__name__] = filter_type

        return cls._filter_types[cls.__name__]

    def get_max_depth(self, model, visited=None, depth=0):
        """Recursively determines the max depth of relationships in the model"""
        if visited is None:
            visited = set()

        if model in visited:
            return depth  # Avoid circular references

        visited.add(model)
        max_depth = depth

        mapper = class_mapper(model)
        for prop in mapper.iterate_properties:
            if isinstance(prop, RelationshipProperty):  # Only count relationships
                related_model = prop.mapper.class_
                max_depth = max(
                    max_depth, self.get_max_depth(related_model, visited, depth + 1)
                )

        return max_depth

    def to_dict(self, depth=1, max_depth=None) -> Dict[str, Any]:
        """Convert model instance to dictionary with automatic depth detection"""
        print(f"Depth: {depth}, Max Depth: {max_depth}")
        if max_depth is None:
            max_depth = self.get_max_depth(self.__class__)  # Automatically calculate

        if depth > max_depth:
            return {"id": self.id}  # Prevent infinite recursion

        result = {}
        mapper = inspect(self.__class__)

        # Get all columns first
        for column in mapper.columns:
            value = getattr(self, column.key)
            # Convert non-serializable types
            if isinstance(value, datetime):
                result[column.key] = value.isoformat()
            elif isinstance(value, (UUID, uuidLib.UUID)):
                result[column.key] = str(value)
            elif isinstance(value, (types.MethodType, property)):
                continue
            else:
                result[column.key] = value

        # Convert relationships
        state = inspect(self)
        for relationship_name, relationship_prop in mapper.relationships.items():
            # Skip if relationship is not loaded
            if not state.attrs[relationship_name].loaded_value is not NO_VALUE:
                continue

            try:
                value = getattr(self, relationship_name)

                # Skip None values
                if value is None:
                    continue

                # Handle collections (lists)
                if relationship_prop.uselist:
                    if isinstance(value, list):
                        # Only include IDs for related objects at max depth
                        if depth + 1 >= max_depth:
                            result[relationship_name] = [
                                {"id": getattr(item, "id", None)} for item in value
                            ]
                        else:
                            result[relationship_name] = [
                                item.to_dict(depth + 1, max_depth)
                                for item in value
                                if hasattr(item, "to_dict")
                            ]
                    else:
                        result[relationship_name] = []

                # Handle single objects
                else:
                    if depth + 1 >= max_depth:
                        result[relationship_name] = {"id": getattr(value, "id", None)}
                    else:
                        if hasattr(value, "to_dict"):
                            result[relationship_name] = value.to_dict(
                                depth + 1, max_depth
                            )
                        else:
                            result[relationship_name] = str(value)

            except Exception as e:
                # Log the error but continue processing
                logger.warning(
                    f"Error serializing relationship {relationship_name}: {str(e)}"
                )
                continue

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseModel":
        """Create model instance from dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__table__.columns})

    def update(self, data: Dict[str, Any]) -> None:
        """Update model instance from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):

                setattr(self, key, value)


class UUIDBase(BaseModel):
    __abstract__ = True

    uuid: Mapped[uuidLib.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuidLib.uuid4
    )

    @property
    def get_uuid(self) -> str:
        """Return UUID as string for public API"""
        return str(self.uuid)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        # def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary including relationships"""
        result = {}

        # Get mapper
        mapper = inspect(self.__class__)

        # Get all columns
        for column in mapper.columns:
            value = getattr(self, column.key)
            # Convert non-serializable types
            if isinstance(value, datetime):
                result[column.key] = value.isoformat()
            elif isinstance(value, (UUID, uuidLib.UUID)):
                result[column.key] = str(value)
            elif isinstance(value, (types.MethodType, property)):
                continue
            else:
                result[column.key] = value

        # Handle relationships that are already loaded
        state = inspect(self)
        for relationship in mapper.relationships:
            # Skip unloaded relationships to prevent lazy loading
            if state.attrs[relationship.key].loaded_value is NO_VALUE:
                continue

            value = getattr(self, relationship.key, None)
            if value is not None:
                if relationship.uselist:
                    # Handle collections (lists)
                    if isinstance(value, list):
                        result[relationship.key] = [
                            item.to_dict() if hasattr(item, "to_dict") else item
                            for item in value
                        ]
                    else:
                        result[relationship.key] = []
                else:
                    # Handle single objects
                    result[relationship.key] = (
                        value.to_dict() if hasattr(value, "to_dict") else value
                    )

        return result
