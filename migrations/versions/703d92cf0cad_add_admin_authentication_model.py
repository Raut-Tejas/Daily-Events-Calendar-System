
"""Add admin authentication model

Revision ID: 703d92cf0cad
Revises: dfbf52fe2fa1
Create Date: 2026-11-11 18:29:43.562855
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '703d92cf0cad'
down_revision = 'dfbf52fe2fa1'
branch_labels = None
depends_on = None


def upgrade():
    # Create only the admins table.
    # Existing event-related tables must remain untouched.

    op.create_table(
        'admins',

        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            'username',
            sa.String(length=80),
            nullable=False,
            unique=True
        ),

        sa.Column(
            'email',
            sa.String(length=120),
            nullable=False,
            unique=True
        ),

        sa.Column(
            'password_hash',
            sa.String(length=256),
            nullable=False
        ),

        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False
        )
    )


def downgrade():
    # Remove only the admins table if this migration is reversed.
    op.drop_table('admins')
