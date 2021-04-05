"""empty message

Revision ID: 1a96a4cc18cd
Revises: 
Create Date: 2021-04-04 19:56:22.554665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a96a4cc18cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('authors')
    op.drop_table('categories')
    op.drop_table('books')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.VARCHAR(length=50), nullable=False),
    sa.Column('published_date', sa.VARCHAR(length=120), nullable=True),
    sa.Column('average_rating', sa.INTEGER(), nullable=True),
    sa.Column('ratings_count', sa.INTEGER(), nullable=True),
    sa.Column('thumbnail', sa.VARCHAR(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('category', sa.VARCHAR(length=120), nullable=True),
    sa.Column('books_id', sa.VARCHAR(length=50), nullable=True),
    sa.ForeignKeyConstraint(['books_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('authors',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('author', sa.VARCHAR(length=120), nullable=True),
    sa.Column('books_id', sa.VARCHAR(length=50), nullable=True),
    sa.ForeignKeyConstraint(['books_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
