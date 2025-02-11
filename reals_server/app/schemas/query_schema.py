from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator
from fastapi import Query
import json
from enum import Enum


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class FilterCondition(BaseModel):
    field: Optional[str] = None
    op: Optional[str] = None
    value: Optional[Any] = None
    relation: Optional[Dict[str, "FilterCondition"]] = None
    and_: Optional[List["FilterCondition"]] = None
    or_: Optional[List["FilterCondition"]] = None

    @classmethod
    def from_dict(cls, data: Dict) -> Optional["FilterCondition"]:
        print("from_dict data", data, "type", type(data))
        if not data or not any(key.startswith("filter_by[") for key in data):
            return cls()

        root = cls()
        for key, value in data.items():
            if key.startswith("filter_by["):
                # Remove prefix and split by '][' to handle nested paths
                clean_key = key.replace("filter_by[", "").replace("]", "")
                parts = clean_key.split("[")

                current = root
                # Process all parts except the last two (field and operator)
                for part in parts[:-2]:
                    if not current.relation:
                        current.relation = {}
                    if part not in current.relation:
                        current.relation[part] = cls()
                    current = current.relation[part]

                if len(parts) >= 2:
                    current.field = parts[-2]
                    current.op = parts[-1]
                    current.value = value

        return root

    @classmethod
    def ensure_condition(
        cls, data: Union[Dict, "FilterCondition", None]
    ) -> "FilterCondition":
        if isinstance(data, dict):
            return cls.from_dict(data)
        elif isinstance(data, FilterCondition):
            return data
        return cls()


class QueryParams(BaseModel):
    page: Optional[int] = 1
    items_per_page: Optional[int] = 100
    order_by: Optional[List[str]] = None
    order_type: Optional[str] = "asc"
    filter_by: Optional[FilterCondition] = None
    search_by: Optional[Dict] = None
    select: Optional[List[str]] = None
    group_by: Optional[List[str]] = None

    @field_validator("select")
    @classmethod
    def validate_select(cls, v: Optional[Union[str, List[str]]]) -> Optional[List[str]]:
        if isinstance(v, str):
            return v.split(",") if v else None
        return v

    @classmethod
    def from_query_params(cls, params: dict):
        # Handle filter_by parameters
        if any(key.startswith("filter_by[") for key in params):
            filter_dict = {
                key: value
                for key, value in params.items()
                if key.startswith("filter_by[")
            }
            filter_by = FilterCondition.from_dict(filter_dict)
        else:
            filter_by = None

        # Handle include parameter
        select = params.get("select", "").split(",") if params.get("select") else None
        if select and select[0] == "":
            select = None

        # Create clean params
        clean_params = {
            "page": int(params.get("page", 1)),
            "items_per_page": int(params.get("items_per_page", 100)),
            "order_by": (
                params.get("order_by", "").split(",")
                if params.get("order_by")
                else None
            ),
            "order_type": params.get("order_type", "asc"),
            "filter_by": filter_by,
            "search_by": None,
            "select": select,
            "group_by": (
                params.get("group_by", "").split(",")
                if params.get("group_by")
                else None
            ),
        }

        return cls(**clean_params)

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 1,
                "items_per_page": 100,
                "order_by": "id,name,created_at",
                "order_type": "asc",
                "filter_by[username][contains]": "arthur",
                "filter_by[status]": "active",
                "search_by[name]": "john",
                "include_relationships": False,
                "group_by": "status,type,category",
                "select": "related_data.subdata,additional_info",
            }
        }
    }
