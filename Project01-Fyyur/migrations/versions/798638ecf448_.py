"""empty message

Revision ID: 798638ecf448
Revises: 832fee365e65
Create Date: 2020-06-08 19:50:25.950529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '798638ecf448'
down_revision = '832fee365e65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'website',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'website',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###
