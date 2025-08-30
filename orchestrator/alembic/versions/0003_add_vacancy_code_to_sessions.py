"""Add vacancy_code to sessions table

Revision ID: 0003
Revises: 0002
Create Date: 2025-08-30 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add vacancy_code column to sessions table
    op.add_column('sessions', sa.Column('vacancy_code', sa.String(length=50), nullable=True))
    
    # Create index for vacancy_code
    op.create_index('ix_sessions_vacancy_code', 'sessions', ['vacancy_code'], unique=False)
    
    # Update existing sessions with vacancy_code from vacancies table
    op.execute("""
        UPDATE sessions 
        SET vacancy_code = v.vacancy_code 
        FROM vacancies v 
        WHERE sessions.vacancy_id = v.id 
        AND v.vacancy_code IS NOT NULL
    """)


def downgrade() -> None:
    # Drop index
    op.drop_index('ix_sessions_vacancy_code', table_name='sessions')
    
    # Drop column
    op.drop_column('sessions', 'vacancy_code')
