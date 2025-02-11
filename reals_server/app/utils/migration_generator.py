from typing import List, Dict, Any, Optional
from sqlalchemy import inspect, MetaData
import sqlalchemy as sa
from datetime import datetime
import os
import re
from jinja2 import Environment, FileSystemLoader


class MigrationGenerator:
    def __init__(self, metadata: MetaData, inspector, connection):
        self.metadata = metadata
        self.inspector = inspector
        self.connection = connection
        self.changes: Dict[str, Any] = {
            "new_tables": [],
            "dropped_tables": [],
            "altered_columns": [],
            "new_columns": [],
            "dropped_columns": [],
            "altered_constraints": [],
        }

        # Setup Jinja2 for template rendering
        template_dir = os.path.join(
            os.path.dirname(__file__), "../templates/migrations"
        )
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def detect_changes(self) -> Dict[str, Any]:
        """Detect all changes between models and database"""
        existing_tables = set(self.inspector.get_table_names())
        model_tables = set(self.metadata.tables.keys())

        # Detect table changes
        self.changes["new_tables"] = list(model_tables - existing_tables)
        self.changes["dropped_tables"] = list(existing_tables - model_tables)

        # Detect column changes
        for table_name in existing_tables & model_tables:
            self._detect_column_changes(table_name)

        return self.changes

    def _detect_column_changes(self, table_name: str) -> None:
        """Detect column changes for a specific table"""
        existing_columns = {
            col["name"]: col for col in self.inspector.get_columns(table_name)
        }
        model_columns = self.metadata.tables[table_name].columns

        for col_name, model_col in model_columns.items():
            if col_name not in existing_columns:
                self.changes["new_columns"].append(
                    {
                        "table": table_name,
                        "column": model_col,
                        "nullable": model_col.nullable,
                    }
                )
            else:
                existing_col = existing_columns[col_name]
                if self._has_column_changes(existing_col, model_col):
                    self.changes["altered_columns"].append(
                        {
                            "table": table_name,
                            "column": model_col,
                            "old_column": existing_col,
                            "changes": self._get_column_changes(
                                existing_col, model_col
                            ),
                        }
                    )

    def _has_column_changes(self, existing_col: Dict, model_col: sa.Column) -> bool:
        """Check if column has changes"""
        return (
            existing_col["nullable"] != model_col.nullable
            or not isinstance(existing_col["type"], type(model_col.type))
            or (
                hasattr(model_col.type, "length")
                and existing_col["type"].length != model_col.type.length
            )
        )

    def _get_column_changes(self, existing_col: Dict, model_col: sa.Column) -> Dict:
        """Get detailed column changes"""
        changes = {}
        if existing_col["nullable"] != model_col.nullable:
            changes["nullable"] = {
                "from": existing_col["nullable"],
                "to": model_col.nullable,
            }
        if not isinstance(existing_col["type"], type(model_col.type)):
            changes["type"] = {"from": existing_col["type"], "to": model_col.type}
        return changes

    def generate_migration(self, message: str) -> str:
        """Generate migration file based on detected changes"""
        changes = self.detect_changes()

        # Generate migration content
        template = self.jinja_env.get_template("migration.py.jinja2")
        content = template.render(
            message=message, changes=changes, timestamp=datetime.utcnow().isoformat()
        )

        # Save migration file
        filename = self._generate_filename(message)
        filepath = os.path.join("migrations", "versions", filename)
        with open(filepath, "w") as f:
            f.write(content)

        return filepath

    def _generate_filename(self, message: str) -> str:
        """Generate migration filename"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        slug = re.sub(r"[^a-z0-9]+", "_", message.lower())
        return f"{timestamp}_{slug}.py"
