"""Update Api Request log

Revision ID: 24a739b036eb
Revises: 612dd8a6833a
Create Date: 2025-02-11 00:13:43.473576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '24a739b036eb'
down_revision: Union[str, None] = '612dd8a6833a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_request_logs',
    sa.Column('request_id', sa.String(length=255), nullable=True),
    sa.Column('response_code', sa.Integer(), nullable=True),
    sa.Column('processing_time_ms', sa.Integer(), nullable=True),
    sa.Column('prompt_tokens', sa.Integer(), nullable=True),
    sa.Column('completion_tokens', sa.Integer(), nullable=True),
    sa.Column('total_tokens', sa.Integer(), nullable=True),
    sa.Column('rate_limit_remaining_requests', sa.Integer(), nullable=True),
    sa.Column('rate_limit_remaining_tokens', sa.Integer(), nullable=True),
    sa.Column('session_uuid', sa.UUID(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['session_uuid'], ['sessions.uuid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.drop_table('api_request_log')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_request_log',
    sa.Column('request_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('prompt_tokens', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('completion_tokens', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_tokens', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rate_limit_remaining_requests', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rate_limit_remaining_tokens', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('session_uuid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['session_uuid'], ['sessions.uuid'], name='api_request_log_session_uuid_fkey'),
    sa.PrimaryKeyConstraint('id', name='api_request_log_pkey')
    )
    op.drop_table('api_request_logs')
    # ### end Alembic commands ### 