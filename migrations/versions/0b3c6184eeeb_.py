"""empty message

Revision ID: 0b3c6184eeeb
Revises: e713687e6e39
Create Date: 2024-02-22 01:08:30.996968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b3c6184eeeb'
down_revision = 'e713687e6e39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('titre', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.drop_column('titre')

    # ### end Alembic commands ###
