"""empty message

Revision ID: 0e996d136c99
Revises: 
Create Date: 2020-08-19 20:43:43.013321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e996d136c99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('gender', sa.Enum('男', '女', '保密'), nullable=True),
    sa.Column('city', sa.String(length=10), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('money', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('gender', sa.Enum('男', '女', '保密'), nullable=True),
    sa.Column('math', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('student')
    # ### end Alembic commands ###