"""create transfers table

Revision ID: dddc92cf0023
Revises: 19383297ecea
Create Date: 2021-09-16 03:02:26.805502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dddc92cf0023'
down_revision = '19383297ecea'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transfers',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('player_id', sa.String, nullable=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('age', sa.String, nullable=True),
        sa.Column('position', sa.String, nullable=True),
        sa.Column('national_1', sa.String, nullable=True),
        sa.Column('national_2', sa.String, nullable=True),
        sa.Column('left_club', sa.String, nullable=True),
        sa.Column('left_club_league', sa.String, nullable=True),
        sa.Column('joined_club', sa.String, nullable=True),
        sa.Column('joined_club_league', sa.String, nullable=True),
        sa.Column('transfer_date', sa.String, nullable=False),
        sa.Column('transfer_date_p', sa.String, nullable=True),
        sa.Column('market_value', sa.String, nullable=True),
        sa.Column('fee', sa.String, nullable=True),
    )


def downgrade():
    op.drop_table('transfers')
