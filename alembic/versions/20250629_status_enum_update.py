"""update proyect_status to enum and migrate values

Revision ID: status_enum_update
Revises: dad69b01bdb8
Create Date: 2025-06-29 20:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'status_enum_update'
down_revision = 'dad69b01bdb8'
branch_labels = None
depends_on = None

# Estados válidos
status_enum = sa.Enum(
    'Activo',
    'En Desarrollo',
    'En Pruebas',
    'Finalizado',
    'Entregado',
    name='proyect_status_enum'
)

def upgrade():
    # 1. Crear el nuevo tipo ENUM
    status_enum.create(op.get_bind(), checkfirst=True)
    # 2. Convertir valores antiguos a uno válido (si existen)
    op.execute("UPDATE proyects SET proyect_status = 'Activo' WHERE proyect_status = 'active';")
    op.execute("UPDATE proyects SET proyect_status = 'En Desarrollo' WHERE proyect_status = 'development';")
    op.execute("UPDATE proyects SET proyect_status = 'En Pruebas' WHERE proyect_status = 'testing';")
    op.execute("UPDATE proyects SET proyect_status = 'Finalizado' WHERE proyect_status = 'finished';")
    op.execute("UPDATE proyects SET proyect_status = 'Entregado' WHERE proyect_status = 'delivered';")
    # 3. Alterar la columna a ENUM
    op.alter_column('proyects', 'proyect_status',
        type_=status_enum,
        existing_type=sa.String(length=50),
        existing_nullable=False,
        server_default='Activo',
    )

def downgrade():
    # Volver a string
    op.alter_column('proyects', 'proyect_status',
        type_=sa.String(length=50),
        existing_type=status_enum,
        existing_nullable=False,
        server_default='Activo',
    )
    status_enum.drop(op.get_bind(), checkfirst=True)
