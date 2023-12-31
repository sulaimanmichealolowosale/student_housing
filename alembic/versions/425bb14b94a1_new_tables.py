"""new tables

Revision ID: 425bb14b94a1
Revises: 
Create Date: 2023-06-26 07:22:46.953297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '425bb14b94a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('nick_name', sa.String(), nullable=False),
    sa.Column('role', sa.String(), server_default='student', nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('rating', sa.Integer(), server_default=sa.text('0'), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('agent_nickname', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('properties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('security_type', sa.String(), nullable=False),
    sa.Column('water_system', sa.String(), nullable=False),
    sa.Column('toilet_bathroom_desc', sa.String(), nullable=False),
    sa.Column('kitchen_desc', sa.String(), nullable=False),
    sa.Column('property_status', sa.String(), nullable=False),
    sa.Column('property_type', sa.String(), nullable=False),
    sa.Column('price', sa.String(), nullable=False),
    sa.Column('payment_duration', sa.String(), nullable=False),
    sa.Column('additional_fee', sa.String(), nullable=True),
    sa.Column('reason_for_fee', sa.String(), nullable=True),
    sa.Column('primary_image_path', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('agent_phone', sa.String(), nullable=True),
    sa.Column('agent_nickname', sa.String(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('property_images')
    op.drop_table('properties')
    op.drop_table('categories')
    op.drop_table('users')
    # ### end Alembic commands ###
