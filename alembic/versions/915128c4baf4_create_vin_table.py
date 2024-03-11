"""create vin table

Revision ID: 915128c4baf4
Revises: 
Create Date: 2024-03-11 16:31:05.245301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '915128c4baf4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    equipment_code_type = sa.Enum('000', '014', '037', '036', '038', '027', name='equipment_code_type')
    place_of_production_type = sa.Enum('00', '01', name='place_of_production_type')

    op.create_table(
        'vin',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('version', sa.String(length=3), nullable=False),
        sa.Column('equipment_code', equipment_code_type, nullable=False),
        sa.Column('year_of_issue', sa.String(length=4), nullable=False),
        sa.Column('serial_number', sa.Integer, nullable=False),
        sa.Column('place_of_production', place_of_production_type, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('vin')
    sa.Enum(name='equipment_code_type').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='place_of_production_type').drop(op.get_bind(), checkfirst=False)
