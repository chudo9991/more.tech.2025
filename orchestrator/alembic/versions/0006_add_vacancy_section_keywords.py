"""Add vacancy section keywords table

Revision ID: 0006
Revises: 0005
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create vacancy_section_keywords table
    op.create_table('vacancy_section_keywords',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('vacancy_id', sa.String(length=50), nullable=False),
        sa.Column('section_type', sa.Enum('responsibilities', 'requirements', 'programs', 'skills', 'languages', 'description', 'additional', name='sectiontype'), nullable=False),
        sa.Column('keywords', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('extraction_date', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for optimization
    op.create_index('ix_vacancy_section_keywords_id', 'vacancy_section_keywords', ['id'], unique=False)
    op.create_index('ix_vacancy_section_keywords_vacancy_id', 'vacancy_section_keywords', ['vacancy_id'], unique=False)
    op.create_index('ix_vacancy_section_keywords_section_type', 'vacancy_section_keywords', ['section_type'], unique=False)
    op.create_index('ix_vacancy_section_keywords_vacancy_section', 'vacancy_section_keywords', ['vacancy_id', 'section_type'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_vacancy_section_keywords_vacancy_section', table_name='vacancy_section_keywords')
    op.drop_index('ix_vacancy_section_keywords_section_type', table_name='vacancy_section_keywords')
    op.drop_index('ix_vacancy_section_keywords_vacancy_id', table_name='vacancy_section_keywords')
    op.drop_index('ix_vacancy_section_keywords_id', table_name='vacancy_section_keywords')
    
    # Drop table
    op.drop_table('vacancy_section_keywords')
    
    # Drop enum type
    op.execute("DROP TYPE sectiontype")
