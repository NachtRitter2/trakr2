"""reinit all tables

Revision ID: 3b6eed849a95
Revises: 
Create Date: 2023-07-17 23:35:03.388479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b6eed849a95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('firstname', sa.String(length=128), nullable=True),
    sa.Column('lastname', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('about_me', sa.String(length=256), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('username')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('location',
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('is_obsolete', sa.Boolean(), nullable=True),
    sa.Column('updated_dtm', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['updated_by'], ['user.username'], ),
    sa.PrimaryKeyConstraint('name')
    )
    with op.batch_alter_table('location', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_location_name'), ['name'], unique=True)

    op.create_table('sensor',
    sa.Column('serial_nr', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('lower_limit', sa.Integer(), nullable=True),
    sa.Column('upper_limit', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('updated_dtm', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['location'], ['location.name'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.username'], ),
    sa.PrimaryKeyConstraint('serial_nr')
    )
    op.create_table('reading',
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('serial_nr', sa.Integer(), nullable=False),
    sa.Column('reading_dtm', sa.DateTime(), nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['location'], ['location.name'], ),
    sa.ForeignKeyConstraint(['serial_nr'], ['sensor.serial_nr'], ),
    sa.PrimaryKeyConstraint('serial_nr', 'reading_dtm')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reading')
    op.drop_table('sensor')
    with op.batch_alter_table('location', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_location_name'))

    op.drop_table('location')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
