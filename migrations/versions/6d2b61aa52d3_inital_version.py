"""inital version

Revision ID: 6d2b61aa52d3
Revises: 
Create Date: 2020-12-08 06:26:56.164735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d2b61aa52d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_id', sa.String(length=20), nullable=True),
    sa.Column('hardware_version', sa.String(length=20), nullable=True),
    sa.Column('software_version', sa.String(length=20), nullable=True),
    sa.Column('creation_time', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('location', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.Column('connected', sa.Boolean(), nullable=True),
    sa.Column('user_configured', sa.Boolean(), nullable=True),
    sa.Column('last_update_received', sa.DateTime(), nullable=True),
    sa.Column('interior_temp', sa.String(length=7), nullable=True),
    sa.Column('exterior_temp', sa.String(length=7), nullable=True),
    sa.Column('device_temp', sa.String(length=7), nullable=True),
    sa.Column('uptime', sa.Interval(), nullable=True),
    sa.Column('current_time', sa.DateTime(), nullable=True),
    sa.Column('load_avg', sa.String(length=20), nullable=True),
    sa.Column('disk_total', sa.String(length=20), nullable=True),
    sa.Column('disk_used', sa.String(length=20), nullable=True),
    sa.Column('disk_free', sa.String(length=20), nullable=True),
    sa.Column('grainbin_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('device_id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(length=20), nullable=True),
    sa.Column('destination', sa.String(length=20), nullable=True),
    sa.Column('classification', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('valid_from', sa.DateTime(), nullable=True),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('payload', sa.PickleType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('system_hardware',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_name', sa.String(length=20), nullable=True),
    sa.Column('hardware_version', sa.String(length=20), nullable=True),
    sa.Column('serial_number', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('system_interface',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('interface', sa.String(length=5), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_for_fm', sa.Boolean(), nullable=True),
    sa.Column('is_external', sa.Boolean(), nullable=True),
    sa.Column('state', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('system_setup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_setup_complete', sa.Boolean(), nullable=True),
    sa.Column('first_setup_time', sa.DateTime(), nullable=True),
    sa.Column('update_in_progress', sa.Boolean(), nullable=True),
    sa.Column('new_update_installed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('system_software',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('software_version', sa.String(length=20), nullable=True),
    sa.Column('software_version_last', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('grainbin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_time', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('grainbin_type', sa.String(length=20), nullable=True),
    sa.Column('sensor_type', sa.String(length=20), nullable=True),
    sa.Column('location', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.Column('total_updates', sa.Integer(), nullable=True),
    sa.Column('average_temp', sa.String(length=7), nullable=True),
    sa.Column('bus_number', sa.Integer(), nullable=False),
    sa.Column('user_configured', sa.Boolean(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('system_wifi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.Column('mode', sa.String(length=20), nullable=True),
    sa.Column('interface_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['interface_id'], ['system_interface.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('temperature_cable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_count', sa.Integer(), nullable=True),
    sa.Column('cable_type', sa.String(length=20), nullable=True),
    sa.Column('bin_cable_number', sa.Integer(), nullable=True),
    sa.Column('grainbin_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grainbin_id'], ['grainbin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('temperature_sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('templow', sa.String(length=4), nullable=True),
    sa.Column('temphigh', sa.String(length=4), nullable=True),
    sa.Column('last_value', sa.String(length=7), nullable=True),
    sa.Column('cable_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cable_id'], ['temperature_cable.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('temperature_sensor')
    op.drop_table('temperature_cable')
    op.drop_table('user_roles')
    op.drop_table('system_wifi')
    op.drop_table('grainbin')
    op.drop_table('users')
    op.drop_table('system_software')
    op.drop_table('system_setup')
    op.drop_table('system_interface')
    op.drop_table('system_hardware')
    op.drop_table('roles')
    op.drop_table('message')
    op.drop_table('device')
    # ### end Alembic commands ###