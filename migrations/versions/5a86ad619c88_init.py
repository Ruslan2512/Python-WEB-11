"""Init

Revision ID: 5a86ad619c88
Revises: 
Create Date: 2023-06-17 16:37:17.401132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a86ad619c88'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('birthday', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('fullname')
    )
    op.create_index(op.f('ix_contacts_birthday'), 'contacts', ['birthday'], unique=False)
    op.create_index(op.f('ix_contacts_fullname'), 'contacts', ['fullname'], unique=False)
    op.create_index(op.f('ix_contacts_lastname'), 'contacts', ['lastname'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_contacts_lastname'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_fullname'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_birthday'), table_name='contacts')
    op.drop_table('contacts')
    # ### end Alembic commands ###