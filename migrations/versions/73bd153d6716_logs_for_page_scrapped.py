"""logs for page scrapped

Revision ID: 73bd153d6716
Revises: b4a71e6cbbea
Create Date: 2021-12-12 21:20:15.416668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73bd153d6716'
down_revision = 'b4a71e6cbbea'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transfers', sa.Column('temp_dates_page', sa.String, nullable=True))
    op.add_column('transfers', sa.Column('temp_players_page', sa.String, nullable=True))


def downgrade():
    op.drop_column('transfers', 'temp_dates_page')
    op.drop_column('transfers', 'temp_players_page')
