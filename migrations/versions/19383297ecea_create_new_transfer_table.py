"""create_new_transfer_table

Revision ID: 19383297ecea
Revises: 
Create Date: 2021-09-03 12:09:21.847340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19383297ecea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'new_transfers',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('player_id', sa.String),
        sa.Column('name', sa.String),
        sa.Column('age', sa.String),
        sa.Column('transfer_date', sa.String),
        sa.Column('market_value', sa.String, nullable=True),
        sa.Column('fee', sa.String, nullable=True),
    )


def downgrade():
    op.drop_table('new_transfers')
