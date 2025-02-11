from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    BinaryExpression,
    ColumnElement,
    Select,
    inspect,
    not_,
    or_,
    select,
    and_,
    func,
    asc,
    desc,
)
from typing import (
    Awaitable,
    Generic,
    Set,
    TypeVar,
    Type,
    Optional,
    List,
    Union,
    Any,
    Dict,
    Tuple,
)
from app.models.base_model import BaseModel
from sqlalchemy.orm import (
    Mapped,
    selectinload,
    joinedload,
    Load,
    Query,
    aliased,
    contains_eager,
    load_only,
    noload,
)
from sqlalchemy.sql._typing import _ColumnExpressionArgument
import logging
from sqlalchemy import Integer
from uuid import UUID
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import selectinload, load_only, noload, defer
from fastapi import HTTPException

from app.schemas.query_schema import FilterCondition


T = TypeVar("T", bound=BaseModel)
M = TypeVar("M", bound=DeclarativeMeta)

logger = logging.getLogger(__name__)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    def refresh(self, obj: T):
        self.db.refresh(obj)

    def _handle_nested_relationships(self, data_dict: dict) -> dict:
        """Handle nested relationships in data dictionary"""
        processed_data = data_dict.copy()

        for relationship in self.model.__mapper__.relationships:
            if relationship.key in processed_data:
                related_data = processed_data.pop(relationship.key)
                related_model = relationship.mapper.class_

                if isinstance(related_data, dict):
                    # Handle one-to-one relationship
                    related_instance = related_model(**related_data)
                    processed_data[relationship.key] = related_instance
                elif isinstance(related_data, list) and related_data:
                    # Handle one-to-many relationship
                    related_instances = [
                        related_model(**item) for item in related_data if item
                    ]
                    processed_data[relationship.key] = related_instances

        return processed_data

    def _apply_filters(
        self, query: Query, filters_by: Optional[Dict[str, Any]] = None
    ) -> Query:
        """Apply filtering to the query with support for nested and Prisma-like filtering."""

        if not filters_by:
            return query

        filter_conditions = []

        for key, value in filters_by.items():
            if key in ["AND", "OR", "NOT"]:
                # Handle logical conditions like {"AND": [...], "OR": [...], "NOT": [...]}
                if isinstance(value, list):
                    sub_conditions = [
                        self._apply_filters(query, sub_filter).whereclause
                        for sub_filter in value
                    ]
                    if key == "AND":
                        filter_conditions.append(and_(*sub_conditions))
                    elif key == "OR":
                        filter_conditions.append(or_(*sub_conditions))
                    elif key == "NOT":
                        filter_conditions.append(not_(and_(*sub_conditions)))
            elif "__" in key:
                # Handle "field__operator" style (e.g., "name__eq")
                field_name, operator = key.split("__", 1)
                column_attr = getattr(self.model, field_name, None)
                if not column_attr:
                    continue
                print("test apply", column_attr, operator, value)
                filter_conditions.append(
                    self._apply_operator(column_attr, operator, value)
                )
            elif isinstance(value, dict):
                # Handle nested dictionary format (e.g., {"name": {"eq": "John"}})
                column_attr = getattr(self.model, key, None)
                if not column_attr:
                    continue

                for operator, op_value in value.items():
                    print("test apply loop", column_attr, operator, op_value)
                    operator_func = self._apply_operator(
                        column_attr, operator, op_value
                    )
                    filter_conditions.append(operator_func)
            else:
                # Default to equality check (e.g., {"name": "John"})
                column_attr = getattr(self.model, key, None)
                if column_attr:
                    filter_conditions.append(column_attr == value)

        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

        return query

    def _apply_operator(self, column, op: str, value: Any):
        """Apply operator to column"""
        op = op.lower() if isinstance(op, str) else op

        operator_map = {
            "equals": lambda col, val: col == val,
            "not_equals": lambda col, val: col != val,
            "greater_than": lambda col, val: col > val,
            "less_than": lambda col, val: col < val,
            "greater_equal": lambda col, val: col >= val,
            "less_equal": lambda col, val: col <= val,
            "contains": lambda col, val: col.ilike(f"%{val}%"),
            "starts_with": lambda col, val: col.ilike(f"{val}%"),
            "ends_with": lambda col, val: col.ilike(f"%{val}"),
            "in": lambda col, val: col.in_(
                val if isinstance(val, (list, tuple)) else [val]
            ),
            "not_in": lambda col, val: col.notin_(
                val if isinstance(val, (list, tuple)) else [val]
            ),
            "is_null": lambda col, val: col.is_(None) if val else col.isnot(None),
        }

        # Map common operators to their functions
        if op in operator_map:
            return operator_map[op](column, value)

        # Handle direct operator strings
        direct_ops = {
            "eq": "==",
            "ne": "!=",
            "gt": ">",
            "lt": "<",
            "ge": ">=",
            "le": "<=",
            "like": "contains",
            "ilike": "contains",
            "in": "in",
            "notin": "not_in",
        }

        if op in direct_ops:
            mapped_op = direct_ops[op]
            if mapped_op in operator_map:
                return operator_map[mapped_op](column, value)

        raise HTTPException(
            status_code=400,
            detail=f"Unsupported operator: {op}. Supported operators are: {list(operator_map.keys())}",
        )

    def _apply_sorting(
        self,
        query: Query,
        sort_by: Optional[List[str]] = None,
        sort_order: Optional[List[str]] = None,
    ) -> Query:
        """Apply sorting to the query."""
        if sort_by:
            order_criteria = []
            order_func = desc if sort_order == "desc" else asc
            for field in sort_by:
                order_criteria.append(order_func(getattr(self.model, field)))
            query = query.order_by(*order_criteria)

            # if sort_order is None:
            #     sort_order = ["asc"] * len(sort_by)
            # for field, order in zip(sort_by, sort_order):
            #     column = getattr(self.model, field)
            #     if order == "asc":
            #         query = query.order_by(asc(column))
            #     elif order == "desc":
            #         query = query.order_by(desc(column))
        return query

    def _apply_pagination(
        self, query: Query, page: int = 1, page_size: int = 10
    ) -> Query:
        """Apply pagination to the query."""
        query = query.offset((page - 1) * page_size).limit(page_size)
        return query

    def _apply_joins(self, stmt, filters_by: Optional[Dict[str, Any]] = None):
        """Apply the necessary joins based on the nested model relationships in filters."""
        if not filters_by:
            return stmt

        # Loop through filters to process each key-value pair
        for key in filters_by:
            if not key.startswith("filter_by"):
                continue

            key = key[len("filter_by[") : -1]  # Remove the 'filter_by[' and ']'
            parts = key.split("][")  # Split to extract model path

            model_field = parts[:-2]  # Everything except last two are the model path
            field_name = parts[-2]  # The field to filter by
            operator = parts[-1]  # The operator

            current_model = self.model
            join_tables = []

            # Resolve relationships and apply joins dynamically
            for rel in model_field:
                if hasattr(current_model, rel):
                    related_model = getattr(current_model, rel).property.mapper.class_
                    alias = aliased(related_model)
                    join_tables.append((current_model, alias, rel))
                    current_model = alias

            # Apply joins
            for parent, child, rel_name in join_tables:
                stmt = stmt.join(child, getattr(parent, rel_name))

        return stmt

    def _get_valid_relationships(self, model_class) -> Dict[str, Set[str]]:
        """Get all valid relationships and their nested relationships for a model"""
        relationships = {}
        mapper = inspect(model_class)

        for rel in mapper.relationships:
            relationships[rel.key] = set()
            # Get nested relationships
            nested_mapper = inspect(rel.mapper.class_)
            for nested_rel in nested_mapper.relationships:
                relationships[rel.key].add(nested_rel.key)

        return relationships

    def _validate_select_paths(self, paths: List[str]) -> None:
        """Validate select paths against model relationships"""
        for path in paths:
            parts = path.split(".")
            current_model = self.model

            for part in parts:
                if not hasattr(current_model, part):
                    valid_rels = self._get_valid_relationships(current_model)
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid relationship '{part}' in path '{path}'. "
                        f"Valid relationships for {current_model.__name__} are: {list(valid_rels.keys())}",
                    )

                attr = getattr(current_model, part)
                # If it's a relationship, update current_model to the related model
                if hasattr(attr, "property") and hasattr(attr.property, "mapper"):
                    current_model = attr.property.mapper.class_

    def _apply_select(self, stmt: Select, include: List[str] | str) -> Select:
        """Apply relationship loading to statement"""
        try:
            if not include:
                return stmt
            # Convert string to list if needed and handle comma-separated values
            if isinstance(include, str):
                relationships = [rel.strip() for rel in include.split(",")]
            else:
                relationships = include

            # Debug log
            print(f"Applying select for includes: {relationships}")
            print(f"Original statement: {stmt}")

            for relationship in relationships:
                # Handle nested relationships (e.g., "related_data.subdata")
                parts = relationship.split(".")

                if len(parts) > 1:
                    # Build the relationship path
                    rel_path = []
                    current_model = self.model

                    for part in parts:
                        rel_attr = getattr(current_model, part, None)
                        if rel_attr is None:
                            logger.warning(
                                f"Relationship {part} not found on {current_model.__name__}"
                            )
                            break

                        rel_path.append(rel_attr)
                        if hasattr(rel_attr, "property"):
                            current_model = rel_attr.property.mapper.class_

                    if len(rel_path) == len(parts):
                        # Apply the complete path
                        stmt = stmt.options(
                            selectinload(rel_path[0]).selectinload(*rel_path[1:])
                        )
                        print(f"Applied nested selectinload for: {relationship}")
                else:
                    # Handle single relationship
                    rel_attr = getattr(self.model, relationship, None)
                    if rel_attr is not None:
                        stmt = stmt.options(selectinload(rel_attr))
                        print(f"Applied selectinload for: {relationship}")
                    else:
                        logger.warning(
                            f"Relationship {relationship} not found on {self.model.__name__}"
                        )

            # Debug final statement
            print(f"Final statement: {stmt}")
            return stmt

        except Exception as e:
            logger.error(f"Error in _apply_select: {str(e)}")
            logger.error(f"Stack trace: ", exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"Error applying select: {str(e)}"
            )

    def _apply_grouping(
        self, query: Query, group_by: Optional[List[str]] = None
    ) -> Query:
        """Apply grouping and aggregations to the query."""
        if group_by:
            query = query.group_by(*[getattr(self.model, field) for field in group_by])
        return query

    async def create(self, data: Dict) -> T:
        """Create a new record with nested relationships"""
        try:
            # Extract nested relationship data
            nested_data = {}
            list_nested_data = {}  # For list relationships
            model_data = {}

            # Get model relationships
            mapper = inspect(self.model)
            relationships = mapper.relationships
            columns = mapper.columns.keys()

            # Separate column data and relationship data
            for key, value in data.items():
                if key in relationships.keys():
                    rel = relationships[key]
                    if rel.uselist:  # If it's a list relationship
                        list_nested_data[key] = value
                    elif isinstance(value, dict):
                        nested_data[key] = value
                elif key in columns:
                    model_data[key] = value

            print(f"Model data: {model_data}")
            print(f"Nested data: {nested_data}")
            print(f"List nested data: {list_nested_data}")

            # Create main model instance
            db_obj = self.model(**model_data)

            # Handle single relationships
            for rel_name, rel_data in nested_data.items():
                if hasattr(db_obj, rel_name):
                    rel_attr = getattr(self.model, rel_name)
                    related_model = rel_attr.property.mapper.class_

                    # Get valid columns for related model
                    related_mapper = inspect(related_model)
                    related_columns = related_mapper.columns.keys()
                    valid_rel_data = {
                        k: v for k, v in rel_data.items() if k in related_columns
                    }

                    # Create related object
                    related_obj = related_model(**valid_rel_data)
                    setattr(db_obj, rel_name, related_obj)

            # Handle list relationships
            for rel_name, rel_data_list in list_nested_data.items():
                if hasattr(db_obj, rel_name):
                    rel_attr = getattr(self.model, rel_name)
                    related_model = rel_attr.property.mapper.class_

                    # Get valid columns for related model
                    related_mapper = inspect(related_model)
                    related_columns = related_mapper.columns.keys()

                    # Create list of related objects
                    related_objects = []
                    for item_data in rel_data_list:
                        if isinstance(item_data, dict):
                            valid_item_data = {
                                k: v
                                for k, v in item_data.items()
                                if k in related_columns
                            }
                            related_obj = related_model(**valid_item_data)
                            related_objects.append(related_obj)

                    setattr(db_obj, rel_name, related_objects)

            self.db.add(db_obj)
            await self.db.commit()

            return db_obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating record: {str(e)}")
            raise HTTPException(
                status_code=400, detail=f"Error creating record: {str(e)}"
            )

    async def get_by_filters(self, *filters) -> List[T]:
        """Get by multiple filters"""
        query = select(self.model).filter_by(*filters)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_first(
        self,
        filters: Union[Dict, FilterCondition, None] = None,
        include: List[str] = None,
    ) -> Optional[T]:
        """Get first record matching filters"""
        try:
            stmt = select(self.model)

            # Apply filters if provided
            if filters:
                stmt, _ = self._apply_filter_condition(stmt, filters)

                # Apply relationship loading if needed
                # if include:
                stmt = self._apply_select(stmt, include)

            result = await self.db.execute(stmt)
            # Use scalars().first() instead of scalar_one_or_none()
            return result.scalars().first()

        except Exception as e:
            logger.error(f"Error in get_first: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def _get_load_options(self) -> List[Any]:
        """Get load options based on model relationships"""
        load_options = []

        for relationship in self.model.__mapper__.relationships:
            # Get relationship properties
            is_collection = relationship.uselist
            target_model = relationship.mapper.class_

            # Choose loading strategy based on relationship type
            if is_collection:
                # Use selectinload for collections (one-to-many, many-to-many)
                load_options.append(selectinload(getattr(self.model, relationship.key)))

            else:
                # Use joinedload for single objects (one-to-one)
                load_options.append(joinedload(getattr(self.model, relationship.key)))

        return load_options

    async def get_by_id(self, id: int, include: List[str] = None) -> Optional[T]:
        """Get a record by id"""
        try:
            # Create base query
            stmt = select(self.model).where(self.model.id == int(id))

            # Apply relationship loading if needed
            if include:
                stmt = self._apply_select(stmt, include)
                # for relationship in include:
                #     stmt = stmt.options(joinedload(getattr(self.model, relationship)))

            # Execute query with existing session
            result = await self.db.execute(stmt)
            obj = result.unique().scalars().first()

            # Only refresh if we found an object
            print("obj", obj)
            return obj

        except Exception as e:
            logger.error(f"Error in get_by_id: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def count(self, **filters: ColumnElement | BinaryExpression) -> int:
        """Count records matching filters"""
        query = select(func.count()).select_from(self.model).filter_by(**filters)
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def exists(self, **filters: ColumnElement | BinaryExpression) -> bool:
        """Check if any records match filters"""
        return await self.count(**filters) > 0

    def _apply_filter_condition(
        self,
        stmt: Select,
        condition: Union[Dict, FilterCondition, None],
        model=None,
        path=None,
    ) -> Tuple[Select, List]:
        print(f"Raw condition input: {condition}")
        print(f"Condition type: {type(condition)}")

        # Convert to FilterCondition if needed
        if isinstance(condition, dict):
            print("Converting dict to FilterCondition")
            try:
                condition = FilterCondition.from_dict(condition)
                print(f"Converted condition: {condition}")
            except Exception as e:
                logger.error(f"Error converting condition: {str(e)}")
                return stmt, []
        elif not isinstance(condition, FilterCondition):
            print("Invalid condition type, returning")
            return stmt, []

        model = model or self.model
        current_filters = []

        # Handle direct field filters
        if condition.field and condition.op:
            try:
                column = getattr(model, condition.field)
                filter_expr = self._apply_operator(
                    column, condition.op, condition.value
                )
                if filter_expr is not None:
                    current_filters.append(filter_expr)
                    print(f"Added direct filter: {filter_expr}")
            except Exception as e:
                logger.error(f"Error applying direct filter: {str(e)}")

        # Handle nested relations
        if condition.relation:
            print(f"Processing relations: {condition.relation}")
            for rel_name, rel_condition in condition.relation.items():
                try:
                    print(f"Processing relation: {rel_name}")
                    rel_attr = getattr(model, rel_name)
                    related_model = rel_attr.property.mapper.class_

                    if path:
                        current_path = f"{path}_{rel_name}"
                        related_model = aliased(related_model, name=current_path)
                        rel_attr = getattr(model, rel_name).of_type(related_model)
                    else:
                        current_path = rel_name

                    # Join with the related model
                    stmt = stmt.join(rel_attr)
                    print(f"Joined with {rel_name}")

                    # Apply filters on the related model
                    nested_stmt, nested_filters = self._apply_filter_condition(
                        stmt, rel_condition, related_model, current_path
                    )

                    if nested_filters:
                        current_filters.extend(nested_filters)
                        print(f"Added nested filters from {rel_name}: {nested_filters}")

                    stmt = nested_stmt
                except Exception as e:
                    logger.error(f"Error processing relation {rel_name}: {str(e)}")
                    logger.error(f"Full error: {e.__class__.__name__}: {str(e)}")
                    raise

        if current_filters:
            filter_condition = and_(*current_filters)
            stmt = stmt.where(filter_condition)
            print(f"Applied filter condition: {filter_condition}")

        return stmt, current_filters

    async def get_all(
        self,
        page: int = 1,
        items_per_page: int = 10,
        order_by: List[str] = None,
        order_type: str = "asc",
        filter_by: Union[Dict, FilterCondition, None] = None,
        search_by: Dict = None,
        select_list: List[str] = None,
        group_by: List[str] = None,
    ) -> List[M]:
        stmt = select(self.model)
        print(f"Initial filter_by: {filter_by}")

        # Apply filters using _apply_filter_condition
        # if filter_by:
        #     stmt = self._apply_filters(stmt, filter_by)
        if filter_by:
            # stmt = self._apply_joins(stmt, filter_by)
            stmt, _ = self._apply_filter_condition(stmt, filter_by)
        # print(f"After applying filters: {stmt}")

        # Apply joins
        #
        # stmt = self._apply_filters(stmt, filter_by)
        # stmt = self._apply_joins(stmt, filter_by)
        stmt = self._apply_select(stmt, select_list)

        stmt = self._apply_sorting(stmt, order_by, order_type)
        stmt = self._apply_pagination(stmt, page, items_per_page)
        stmt = self._apply_grouping(stmt, group_by)

        # Execute query and return results
        result = await self.db.execute(stmt)
        return result.unique().scalars().all()

    async def update(self, id: int, data: Dict) -> Optional[M]:
        """Update a record by id"""
        try:
            print("update data", data)
            # Get existing record with relationships loaded
            stmt = select(self.model).where(self.model.id == int(id))

            # Get model relationships and add joinedload for each
            mapper = inspect(self.model)
            relationships = mapper.relationships.keys()
            for rel in relationships:
                stmt = stmt.options(joinedload(getattr(self.model, rel)))

            result = await self.db.execute(stmt)
            db_obj = result.unique().scalar_one_or_none()

            if not db_obj:
                return None

            # Separate nested data and model data
            nested_data = {}
            model_data = {}

            for key, value in data.items():
                if key in relationships and isinstance(value, dict):
                    nested_data[key] = value
                else:
                    model_data[key] = value

            # Update main model fields
            for key, value in model_data.items():
                if hasattr(db_obj, key):
                    setattr(db_obj, key, value)

            # Update nested relationships
            for rel_name, rel_data in nested_data.items():
                if hasattr(db_obj, rel_name):
                    rel_attr = getattr(self.model, rel_name)
                    related_model = rel_attr.property.mapper.class_
                    related_obj = getattr(db_obj, rel_name)

                    if related_obj is None:
                        # Create new related object
                        related_obj = related_model()
                        for key, value in rel_data.items():
                            if hasattr(related_obj, key):
                                setattr(related_obj, key, value)
                        setattr(db_obj, rel_name, related_obj)
                    else:
                        # Update existing related object
                        for key, value in rel_data.items():
                            if hasattr(related_obj, key):
                                setattr(related_obj, key, value)

            # Commit changes
            await self.db.commit()
            await self.db.refresh(db_obj)

            return db_obj

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating record: {str(e)}")
            raise HTTPException(
                status_code=400, detail=f"Error updating record: {str(e)}"
            )

    async def delete(self, id: int, cascade: List[str] = None) -> bool:
        """Delete a record by id with optional cascade relationships"""
        try:
            # Start with base query
            stmt = select(self.model).where(self.model.id == int(id))

            # Load specified relationships if cascade is provided
            if cascade:
                for relationship in cascade:
                    rel_attr = getattr(self.model, relationship)
                    stmt = stmt.options(selectinload(rel_attr))

            # Get the record with relationships
            result = await self.db.execute(stmt)
            record = result.scalar_one_or_none()

            if not record:
                return False

            # Delete the record
            await self.db.delete(record)
            await self.db.commit()

            return True
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting record: {str(e)}")
            raise
