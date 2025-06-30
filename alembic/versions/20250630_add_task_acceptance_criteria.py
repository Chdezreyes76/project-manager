"""
Add task_acceptance_criteria column to tasks table

Revision ID: 20250630_add_task_acceptance_criteria
Revises: 87f3306b2933
Create Date: 2025-06-30
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250630_add_task_acceptance_criteria'
down_revision = '87f3306b2933'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('tasks', sa.Column('task_acceptance_criteria', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('tasks', 'task_acceptance_criteria')
