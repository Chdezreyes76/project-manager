"""merge status and userstory status enum

Revision ID: 597a2c80f880
Revises: status_enum_update, 20250629_userstory_status_enum
Create Date: 2025-06-29 19:07:32.014033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '597a2c80f880'
down_revision: Union[str, Sequence[str], None] = ('status_enum_update', '20250629_userstory_status_enum')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
