"""users table

Revision ID: 1268c05a3a53
Revises: 62d5edcfa746
Create Date: 2020-05-09 17:39:12.905757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1268c05a3a53'
down_revision = '62d5edcfa746'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_fridge_ingredient', table_name='fridge')
    op.drop_index('ix_fridge_quantity', table_name='fridge')
    op.drop_table('fridge')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fridge',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ingredient', sa.VARCHAR(length=140), nullable=True),
    sa.Column('quantity', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_fridge_quantity', 'fridge', ['quantity'], unique=False)
    op.create_index('ix_fridge_ingredient', 'fridge', ['ingredient'], unique=False)
    # ### end Alembic commands ###
