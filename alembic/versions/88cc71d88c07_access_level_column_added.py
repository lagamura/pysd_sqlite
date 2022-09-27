"""access_level column added

Revision ID: 88cc71d88c07
Revises: f55fa3e9ac97
Create Date: 2022-09-27 09:55:28.394785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88cc71d88c07'
down_revision = 'f55fa3e9ac97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('access_level', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'access_level')
    # ### end Alembic commands ###