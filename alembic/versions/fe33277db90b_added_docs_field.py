"""added docs field

Revision ID: fe33277db90b
Revises: 3822e5a0523a
Create Date: 2022-05-26 17:17:52.026563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe33277db90b'
down_revision = '3822e5a0523a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Models', sa.Column('docs', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Models', 'docs')
    # ### end Alembic commands ###
