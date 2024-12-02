"""add author

Revision ID: d0fd1e5179b3
Revises: d40c22d111cd
Create Date: 2024-12-02 23:39:22.798660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0fd1e5179b3'
down_revision = 'd40c22d111cd'
branch_labels = None
depends_on = None


def upgrade():
    # Додавання нового поля author
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.String(100), nullable=False))

    # Не змінюємо тип publish_date, якщо не потрібно

def downgrade():
    # Видалення поля author, якщо скасовуємо міграцію
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('author')

    # Якщо потрібно скасувати зміни з publish_date
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('publish_date',
               existing_type=sa.String(),
               type_=sa.DATETIME(),
               existing_nullable=True)
