"""Add Order and Customer models

Revision ID: 795e3bf4b62d
Revises: 090ba6ef67ce
Create Date: 2024-12-19 00:15:55.302709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '795e3bf4b62d'
down_revision = '090ba6ef67ce'
branch_labels = None
depends_on = None


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customer')
    op.drop_table('order')
    # ### end Alembic commands ###


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.Column('price', sa.FLOAT(), nullable=False),
    sa.Column('customer_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('about_customer', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###
