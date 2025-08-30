"""Extend vacancies table with BA fields

Revision ID: 0002
Revises: 0001
Create Date: 2025-01-15 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to vacancies table
    op.add_column('vacancies', sa.Column('vacancy_code', sa.String(length=50), nullable=True))
    op.add_column('vacancies', sa.Column('status', sa.String(length=50), nullable=True, server_default='active'))
    op.add_column('vacancies', sa.Column('region', sa.String(length=100), nullable=True))
    op.add_column('vacancies', sa.Column('city', sa.String(length=100), nullable=True))
    op.add_column('vacancies', sa.Column('address', sa.Text(), nullable=True))
    op.add_column('vacancies', sa.Column('employment_type', sa.String(length=50), nullable=True))
    op.add_column('vacancies', sa.Column('contract_type', sa.String(length=50), nullable=True))
    op.add_column('vacancies', sa.Column('work_schedule', sa.Text(), nullable=True))
    op.add_column('vacancies', sa.Column('business_trips', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('vacancies', sa.Column('salary_min', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('vacancies', sa.Column('salary_max', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('vacancies', sa.Column('total_income', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('vacancies', sa.Column('annual_bonus_percent', sa.Numeric(precision=5, scale=2), nullable=True))
    op.add_column('vacancies', sa.Column('bonus_description', sa.Text(), nullable=True))
    op.add_column('vacancies', sa.Column('responsibilities', sa.Text(), nullable=True))
    op.add_column('vacancies', sa.Column('requirements', sa.Text(), nullable=True))
    op.add_column('vacancies', sa.Column('education_level', sa.String(length=100), nullable=True))
    op.add_column('vacancies', sa.Column('experience_required', sa.String(length=100), nullable=True))
    op.add_column('vacancies', sa.Column('special_programs', sa.Text(), nullable=True))
    op.add_column('vacancies', sa.Column('computer_skills', sa.Text(), nullable=True))
    op.add_column('vacancies', sa.Column('foreign_languages', sa.Text(), nullable=True))
    op.add_column('vacancies', sa.Column('language_level', sa.String(length=50), nullable=True))
    op.add_column('vacancies', sa.Column('additional_info', sa.Text(), nullable=True))

    # Create unique index for vacancy_code
    op.create_index('ix_vacancies_vacancy_code', 'vacancies', ['vacancy_code'], unique=True)
    
    # Create indexes for common search fields
    op.create_index('ix_vacancies_status', 'vacancies', ['status'], unique=False)
    op.create_index('ix_vacancies_region', 'vacancies', ['region'], unique=False)
    op.create_index('ix_vacancies_city', 'vacancies', ['city'], unique=False)
    op.create_index('ix_vacancies_employment_type', 'vacancies', ['employment_type'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_vacancies_employment_type', table_name='vacancies')
    op.drop_index('ix_vacancies_city', table_name='vacancies')
    op.drop_index('ix_vacancies_region', table_name='vacancies')
    op.drop_index('ix_vacancies_status', table_name='vacancies')
    op.drop_index('ix_vacancies_vacancy_code', table_name='vacancies')
    
    # Drop columns
    op.drop_column('vacancies', 'additional_info')
    op.drop_column('vacancies', 'language_level')
    op.drop_column('vacancies', 'foreign_languages')
    op.drop_column('vacancies', 'computer_skills')
    op.drop_column('vacancies', 'special_programs')
    op.drop_column('vacancies', 'experience_required')
    op.drop_column('vacancies', 'education_level')
    op.drop_column('vacancies', 'requirements')
    op.drop_column('vacancies', 'responsibilities')
    op.drop_column('vacancies', 'bonus_description')
    op.drop_column('vacancies', 'annual_bonus_percent')
    op.drop_column('vacancies', 'total_income')
    op.drop_column('vacancies', 'salary_max')
    op.drop_column('vacancies', 'salary_min')
    op.drop_column('vacancies', 'business_trips')
    op.drop_column('vacancies', 'work_schedule')
    op.drop_column('vacancies', 'contract_type')
    op.drop_column('vacancies', 'employment_type')
    op.drop_column('vacancies', 'address')
    op.drop_column('vacancies', 'city')
    op.drop_column('vacancies', 'region')
    op.drop_column('vacancies', 'status')
    op.drop_column('vacancies', 'vacancy_code')
