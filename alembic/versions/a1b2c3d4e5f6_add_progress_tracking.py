"""add progress tracking (days_of_week, tracked_exercises)

Revision ID: a1b2c3d4e5f6
Revises: 034b6754a33c
Create Date: 2026-09-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '034b6754a33c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('workout_templates', sa.Column('days_of_week', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    op.create_table(
        'tracked_exercises',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('exercise_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['program_id'], ['program_templates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('program_id', 'exercise_id', name='uq_tracked_exercise_program_exercise'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tracked_exercises')
    op.drop_column('workout_templates', 'days_of_week')
