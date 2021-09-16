"""more fields 2 for transfers table

Revision ID: b4a71e6cbbea
Revises: 7b663d32f7e7
Create Date: 2021-09-16 10:42:31.699982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4a71e6cbbea'
down_revision = '7b663d32f7e7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transfers', sa.Column('loan_fee', sa.String, nullable=True))
    op.add_column('transfers', sa.Column('loan_fee_p', sa.BigInteger, nullable=True))
    op.add_column('transfers', sa.Column('created_at', sa.DateTime, nullable=True))
    op.add_column('transfers', sa.Column('updated_at', sa.DateTime, nullable=True))


def downgrade():
    op.drop_column('transfers', 'loan_fee')
    op.drop_column('transfers', 'loan_fee_p')
    op.drop_column('transfers', 'created_at')
    op.drop_column('transfers', 'updated_at')
