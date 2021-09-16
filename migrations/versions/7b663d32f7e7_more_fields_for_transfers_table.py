"""more fields for transfers table

Revision ID: 7b663d32f7e7
Revises: dddc92cf0023
Create Date: 2021-09-16 08:05:08.273709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b663d32f7e7'
down_revision = 'dddc92cf0023'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transfers', sa.Column('left_club_country', sa.String, nullable=True))
    op.add_column('transfers', sa.Column('joined_club_country', sa.String, nullable=True))


def downgrade():
    op.drop_column('transfers', 'left_club_country')
    op.drop_column('transfers', 'joined_club_country')
