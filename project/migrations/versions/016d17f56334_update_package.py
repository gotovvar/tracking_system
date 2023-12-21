"""Update Package

Revision ID: 016d17f56334
Revises: 666d289a641b
Create Date: 2023-12-21 01:26:18.933952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '016d17f56334'
down_revision: Union[str, None] = '666d289a641b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'administrator', ['login'])
    op.create_unique_constraint(None, 'default_user', ['login'])
    op.add_column('package', sa.Column('sender_login', sa.String(length=128), nullable=True))
    op.add_column('package', sa.Column('recipient_login', sa.String(length=128), nullable=True))
    op.drop_constraint('package_sender_id_fkey', 'package', type_='foreignkey')
    op.drop_constraint('package_recipient_id_fkey', 'package', type_='foreignkey')
    op.create_foreign_key(None, 'package', 'default_user', ['recipient_login'], ['login'])
    op.create_foreign_key(None, 'package', 'default_user', ['sender_login'], ['login'])
    op.drop_column('package', 'sender_id')
    op.drop_column('package', 'recipient_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('package', sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('package', sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'package', type_='foreignkey')
    op.drop_constraint(None, 'package', type_='foreignkey')
    op.create_foreign_key('package_recipient_id_fkey', 'package', 'default_user', ['recipient_id'], ['id'])
    op.create_foreign_key('package_sender_id_fkey', 'package', 'default_user', ['sender_id'], ['id'])
    op.drop_column('package', 'recipient_login')
    op.drop_column('package', 'sender_login')
    op.drop_constraint(None, 'default_user', type_='unique')
    op.drop_constraint(None, 'administrator', type_='unique')
    # ### end Alembic commands ###
