"""Initial schema

Revision ID: 0001
Revises: 
Create Date: 2025-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create candidates table
    op.create_table('candidates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fio', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidates_id'), 'candidates', ['id'], unique=False)

    # Create vacancies table
    op.create_table('vacancies',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create questions table
    op.create_table('questions',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.Column('max_duration_s', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create criteria table
    op.create_table('criteria',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Create vacancy_questions table
    op.create_table('vacancy_questions',
        sa.Column('vacancy_id', sa.String(length=50), nullable=False),
        sa.Column('question_id', sa.String(length=50), nullable=False),
        sa.Column('step_no', sa.Integer(), nullable=False),
        sa.Column('question_weight', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('must_have', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('vacancy_id', 'question_id')
    )

    # Create question_criteria table
    op.create_table('question_criteria',
        sa.Column('question_id', sa.String(length=50), nullable=False),
        sa.Column('criterion_id', sa.String(length=50), nullable=False),
        sa.Column('weight', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('must_have', sa.Boolean(), nullable=True),
        sa.Column('min_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['criterion_id'], ['criteria.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('question_id', 'criterion_id')
    )

    # Create sessions table
    op.create_table('sessions',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('candidate_id', sa.Integer(), nullable=True),
        sa.Column('vacancy_id', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('current_step', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create qa table
    op.create_table('qa',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(length=50), nullable=False),
        sa.Column('step_no', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.String(length=50), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('answer_text', sa.Text(), nullable=True),
        sa.Column('audio_url', sa.String(length=500), nullable=True),
        sa.Column('tone', sa.String(length=50), nullable=True),
        sa.Column('passed', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_qa_id'), 'qa', ['id'], unique=False)

    # Create qa_scores table
    op.create_table('qa_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('qa_id', sa.Integer(), nullable=False),
        sa.Column('criterion_id', sa.String(length=50), nullable=True),
        sa.Column('score', sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column('evidence', sa.Text(), nullable=True),
        sa.Column('red_flag', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['criterion_id'], ['criteria.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['qa_id'], ['qa.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_qa_scores_id'), 'qa_scores', ['id'], unique=False)

    # Create media table
    op.create_table('media',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(length=50), nullable=False),
        sa.Column('kind', sa.String(length=50), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_sessions_candidate_id', 'sessions', ['candidate_id'], unique=False)
    op.create_index('ix_sessions_vacancy_id', 'sessions', ['vacancy_id'], unique=False)
    op.create_index('ix_sessions_status', 'sessions', ['status'], unique=False)
    op.create_index('ix_qa_session_id', 'qa', ['session_id'], unique=False)
    op.create_index('ix_qa_scores_qa_id', 'qa_scores', ['qa_id'], unique=False)
    op.create_index('ix_media_session_id', 'media', ['session_id'], unique=False)
    op.create_index('ix_vacancy_questions_vacancy_id', 'vacancy_questions', ['vacancy_id'], unique=False)
    op.create_index('ix_question_criteria_question_id', 'question_criteria', ['question_id'], unique=False)

    # Create updated_at trigger function
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    # Create triggers for updated_at
    op.execute("CREATE TRIGGER update_candidates_updated_at BEFORE UPDATE ON candidates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();")
    op.execute("CREATE TRIGGER update_vacancies_updated_at BEFORE UPDATE ON vacancies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();")
    op.execute("CREATE TRIGGER update_questions_updated_at BEFORE UPDATE ON questions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();")
    op.execute("CREATE TRIGGER update_criteria_updated_at BEFORE UPDATE ON criteria FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();")
    op.execute("CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();")
    op.execute("CREATE TRIGGER update_qa_updated_at BEFORE UPDATE ON qa FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();")
    op.execute("CREATE TRIGGER update_qa_scores_updated_at BEFORE UPDATE ON qa_scores FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();")


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS update_qa_scores_updated_at ON qa_scores;")
    op.execute("DROP TRIGGER IF EXISTS update_qa_updated_at ON qa;")
    op.execute("DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;")
    op.execute("DROP TRIGGER IF EXISTS update_criteria_updated_at ON criteria;")
    op.execute("DROP TRIGGER IF EXISTS update_questions_updated_at ON questions;")
    op.execute("DROP TRIGGER IF EXISTS update_vacancies_updated_at ON vacancies;")
    op.execute("DROP TRIGGER IF EXISTS update_candidates_updated_at ON candidates;")
    
    # Drop function
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    # Drop tables
    op.drop_table('media')
    op.drop_table('qa_scores')
    op.drop_table('qa')
    op.drop_table('sessions')
    op.drop_table('question_criteria')
    op.drop_table('vacancy_questions')
    op.drop_table('criteria')
    op.drop_table('questions')
    op.drop_table('vacancies')
    op.drop_table('candidates')
