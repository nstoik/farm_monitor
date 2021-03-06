"""remove unique timestamp requirement

Revision ID: e9b3d0614f90
Revises: 9d9cc8958287
Create Date: 2021-10-26 04:01:54.234050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9b3d0614f90'
down_revision = '9d9cc8958287'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_device_update_timestamp', table_name='device_update')
    op.create_index(op.f('ix_device_update_timestamp'), 'device_update', ['timestamp'], unique=False)
    op.drop_index('ix_grainbin_update_timestamp', table_name='grainbin_update')
    op.create_index(op.f('ix_grainbin_update_timestamp'), 'grainbin_update', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_grainbin_update_timestamp'), table_name='grainbin_update')
    op.create_index('ix_grainbin_update_timestamp', 'grainbin_update', ['timestamp'], unique=False)
    op.drop_index(op.f('ix_device_update_timestamp'), table_name='device_update')
    op.create_index('ix_device_update_timestamp', 'device_update', ['timestamp'], unique=False)
    # ### end Alembic commands ###
