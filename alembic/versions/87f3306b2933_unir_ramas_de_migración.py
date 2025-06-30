"""Unir ramas de migración

Revision ID: 87f3306b2933
Revises: 20250629_add_userstory_proposed_tasks, 597a2c80f880
Create Date: 2025-06-29 20:26:30.978358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87f3306b2933'
down_revision: Union[str, Sequence[str], None] = ('20250629_add_userstory_proposed_tasks', '597a2c80f880')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
