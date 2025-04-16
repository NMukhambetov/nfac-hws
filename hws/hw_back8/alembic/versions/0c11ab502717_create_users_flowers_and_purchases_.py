"""Create users, flowers, and purchases tables

Revision ID: 0c11ab502717
Revises: 
Create Date: 2025-04-16 03:16:23.527374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c11ab502717'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flowers',
    sa.Column('flower_id', sa.Integer(), nullable=False),
    sa.Column('flower_name', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('flower_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_table('purchases',
    sa.Column('purchase_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('flower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['flower_id'], ['flowers.flower_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('purchase_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchases')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('flowers')
    # ### end Alembic commands ###
