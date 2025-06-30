"""
Revision ID: 20250629_add_userstory_proposed_tasks
Revises: 
Create Date: 2025-06-29

Alembic migration script to add userstory_proposed_tasks column to userstories table
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250629_add_userstory_proposed_tasks'
down_revision = 'dad69b01bdb8'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('userstories', sa.Column('userstory_proposed_tasks', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('userstories', 'userstory_proposed_tasks')
