"""Initial migration

Revision ID: d40c22d111cd
Revises: 
Create Date: 2024-12-02 19:50:54.999343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd40c22d111cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('title', sa.VARCHAR(length=100), nullable=False),
        sa.Column('content', sa.TEXT(), nullable=False),
        sa.Column('category', sa.VARCHAR(length=50), nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), nullable=True),
        sa.Column('publish_date', sa.DATETIME(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('posts')
