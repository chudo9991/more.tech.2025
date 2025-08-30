"""Extend questions table with vacancy-specific fields

Revision ID: 0004
Revises: 0003
Create Date: 2025-08-30 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to questions table
    op.add_column('questions', sa.Column('is_vacancy_specific', sa.Boolean(), nullable=True, default=False))
    op.add_column('questions', sa.Column('category', sa.String(length=100), nullable=True))
    op.add_column('questions', sa.Column('difficulty_level', sa.String(length=50), nullable=True, default='medium'))
    
    # Create indexes for new columns
    op.create_index('ix_questions_is_vacancy_specific', 'questions', ['is_vacancy_specific'], unique=False)
    op.create_index('ix_questions_category', 'questions', ['category'], unique=False)
    op.create_index('ix_questions_difficulty_level', 'questions', ['difficulty_level'], unique=False)
    
    # Update existing questions to have default values
    op.execute("UPDATE questions SET is_vacancy_specific = false WHERE is_vacancy_specific IS NULL")
    op.execute("UPDATE questions SET difficulty_level = 'medium' WHERE difficulty_level IS NULL")


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_questions_difficulty_level', table_name='questions')
    op.drop_index('ix_questions_category', table_name='questions')
    op.drop_index('ix_questions_is_vacancy_specific', table_name='questions')
    
    # Drop columns
    op.drop_column('questions', 'difficulty_level')
    op.drop_column('questions', 'category')
    op.drop_column('questions', 'is_vacancy_specific')
