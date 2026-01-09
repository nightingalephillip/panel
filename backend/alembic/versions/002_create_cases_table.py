"""create cases table

Revision ID: 002
Revises: 001
Create Date: 2026-01-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types
    casestatus = postgresql.ENUM(
        'open', 'in_progress', 'pending', 'closed', 'archived',
        name='casestatus'
    )
    casestatus.create(op.get_bind())

    casepriority = postgresql.ENUM(
        'low', 'medium', 'high', 'critical',
        name='casepriority'
    )
    casepriority.create(op.get_bind())

    tlp = postgresql.ENUM(
        'white', 'green', 'amber', 'red',
        name='tlp'
    )
    tlp.create(op.get_bind())

    # Create cases table
    op.create_table(
        'cases',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('case_number', sa.String(length=20), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column(
            'status',
            postgresql.ENUM(
                'open', 'in_progress', 'pending', 'closed', 'archived',
                name='casestatus',
                create_type=False
            ),
            nullable=False,
            server_default='open'
        ),
        sa.Column(
            'priority',
            postgresql.ENUM(
                'low', 'medium', 'high', 'critical',
                name='casepriority',
                create_type=False
            ),
            nullable=False,
            server_default='medium'
        ),
        sa.Column(
            'tlp',
            postgresql.ENUM(
                'white', 'green', 'amber', 'red',
                name='tlp',
                create_type=False
            ),
            nullable=False,
            server_default='amber'
        ),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=False, server_default='{}'),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assigned_to_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assigned_to_id'], ['users.id'], ondelete='SET NULL'),
    )

    # Create indexes
    op.create_index('ix_cases_case_number', 'cases', ['case_number'], unique=True)
    op.create_index('ix_cases_status', 'cases', ['status'])
    op.create_index('ix_cases_priority', 'cases', ['priority'])
    op.create_index('ix_cases_created_at', 'cases', ['created_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_cases_created_at', table_name='cases')
    op.drop_index('ix_cases_priority', table_name='cases')
    op.drop_index('ix_cases_status', table_name='cases')
    op.drop_index('ix_cases_case_number', table_name='cases')

    # Drop table
    op.drop_table('cases')

    # Drop enum types
    op.execute('DROP TYPE IF EXISTS tlp')
    op.execute('DROP TYPE IF EXISTS casepriority')
    op.execute('DROP TYPE IF EXISTS casestatus')
