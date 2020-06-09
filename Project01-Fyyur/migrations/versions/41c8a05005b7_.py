"""empty message

Revision ID: 41c8a05005b7
Revises: 4aa7f41859f3
Create Date: 2020-06-08 16:24:20.894842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41c8a05005b7'
down_revision = '4aa7f41859f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Shows', ['artist_id', 'venue_id', 'start_time'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Shows', type_='unique')
    # ### end Alembic commands ###
