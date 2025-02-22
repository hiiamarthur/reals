"""Update Api Request log

Revision ID: 975acc080aa8
Revises: c2f40050c188
Create Date: 2025-02-11 00:44:00.832786

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "975acc080aa8"
down_revision: Union[str, None] = "c2f40050c188"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "api_request_logs",
        sa.Column("rate_limit_reset_requests", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "api_request_logs",
        sa.Column("rate_limit_reset_tokens", sa.String(length=255), nullable=True),
    )
    op.alter_column(
        "api_request_logs",
        "rate_limit_remaining_requests",
        existing_type=sa.String(length=99),
        type_=sa.Integer(),
        existing_nullable=True,
    )
    op.alter_column(
        "api_request_logs",
        "rate_limit_remaining_tokens",
        existing_type=sa.String(length=99),
        type_=sa.Integer(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "api_request_logs",
        "rate_limit_remaining_tokens",
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(length=99),
        existing_nullable=True,
    )
    op.alter_column(
        "api_request_logs",
        "rate_limit_remaining_requests",
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(length=99),
        existing_nullable=True,
    )
    op.drop_column("api_request_logs", "rate_limit_reset_tokens")
    op.drop_column("api_request_logs", "rate_limit_reset_requests")
    # ### end Alembic commands ###
