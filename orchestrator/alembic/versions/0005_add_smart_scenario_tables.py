"""Add smart scenario tables

Revision ID: 0005
Revises: 0004
Create Date: 2025-08-30 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create interview_scenarios table
    op.create_table('interview_scenarios',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('vacancy_id', sa.String(length=50), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('version', sa.String(length=20), nullable=True, default='1.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_interview_scenarios_id', 'interview_scenarios', ['id'], unique=False)

    # Create scenario_nodes table
    op.create_table('scenario_nodes',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('scenario_id', sa.String(length=50), nullable=False),
        sa.Column('question_id', sa.String(length=50), nullable=True),
        sa.Column('node_type', sa.String(length=50), nullable=False),
        sa.Column('position_x', sa.Integer(), nullable=True, default=0),
        sa.Column('position_y', sa.Integer(), nullable=True, default=0),
        sa.Column('node_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
        sa.ForeignKeyConstraint(['scenario_id'], ['interview_scenarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_scenario_nodes_id', 'scenario_nodes', ['id'], unique=False)

    # Create scenario_transitions table
    op.create_table('scenario_transitions',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('scenario_id', sa.String(length=50), nullable=False),
        sa.Column('from_node_id', sa.String(length=50), nullable=False),
        sa.Column('to_node_id', sa.String(length=50), nullable=False),
        sa.Column('condition_type', sa.String(length=50), nullable=True),
        sa.Column('condition_value', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True, default=1),
        sa.Column('transition_label', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['from_node_id'], ['scenario_nodes.id'], ),
        sa.ForeignKeyConstraint(['scenario_id'], ['interview_scenarios.id'], ),
        sa.ForeignKeyConstraint(['to_node_id'], ['scenario_nodes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_scenario_transitions_id', 'scenario_transitions', ['id'], unique=False)

    # Create session_context table
    op.create_table('session_context',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('session_id', sa.String(length=50), nullable=False),
        sa.Column('skill_assessments', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('negative_responses', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('current_path', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('context_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('current_node_id', sa.String(length=50), nullable=True),
        sa.Column('scenario_id', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['current_node_id'], ['scenario_nodes.id'], ),
        sa.ForeignKeyConstraint(['scenario_id'], ['interview_scenarios.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_session_context_id', 'session_context', ['id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('ix_session_context_id', table_name='session_context')
    op.drop_table('session_context')
    
    op.drop_index('ix_scenario_transitions_id', table_name='scenario_transitions')
    op.drop_table('scenario_transitions')
    
    op.drop_index('ix_scenario_nodes_id', table_name='scenario_nodes')
    op.drop_table('scenario_nodes')
    
    op.drop_index('ix_interview_scenarios_id', table_name='interview_scenarios')
    op.drop_table('interview_scenarios')
