"""Update Api Request log

Revision ID: c2f40050c188
Revises: 17b3ddc74aa0
Create Date: 2025-02-11 00:38:44.601414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2f40050c188'
down_revision: Union[str, None] = '17b3ddc74aa0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('api_request_logs', 'rate_limit_remaining_requests',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=99),
               existing_nullable=True)
    op.alter_column('api_request_logs', 'rate_limit_remaining_tokens',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=99),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('api_request_logs', 'rate_limit_remaining_tokens',
               existing_type=sa.String(length=99),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('api_request_logs', 'rate_limit_remaining_requests',
               existing_type=sa.String(length=99),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ### 