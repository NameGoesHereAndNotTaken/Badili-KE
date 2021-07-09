"""empty message

Revision ID: 40b7a2ae2227
Revises: 
Create Date: 2021-07-08 21:11:29.938780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40b7a2ae2227'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('id_number', sa.String(length=50), nullable=False),
    sa.Column('country_code', sa.String(length=10), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('pin', sa.String(length=100), nullable=False),
    sa.Column('public_key', sa.String(length=50), nullable=False),
    sa.Column('secret', sa.String(length=50), nullable=False),
    sa.Column('currencies', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
