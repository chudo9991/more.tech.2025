"""add contextual questions table

Revision ID: 0007
Revises: 0006_add_vacancy_section_keywords
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006_add_vacancy_section_keywords'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create contextual_questions table
    op.create_table('contextual_questions',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('session_id', sa.String(length=50), nullable=False),
        sa.Column('scenario_node_id', sa.String(length=50), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(length=50), nullable=True),
        sa.Column('context_source', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_used', sa.Boolean(), nullable=True),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['scenario_node_id'], ['scenario_nodes.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_contextual_questions_id', 'contextual_questions', ['id'], unique=False)
    
    # Add contextual_questions column to session_context table
    op.add_column('session_context', sa.Column('contextual_questions', postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    # Drop contextual_questions column from session_context table
    op.drop_column('session_context', 'contextual_questions')
    
    # Drop contextual_questions table
    op.drop_index('ix_contextual_questions_id', table_name='contextual_questions')
    op.drop_table('contextual_questions')
