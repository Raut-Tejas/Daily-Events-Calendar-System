
"""add student and notification tables

Revision ID: 88d196f6739e
Revises: 703d92cf0cad
Create Date: 2026-11-14 16:00:12.729518

"""

from alembic import op
import sqlalchemy as sa

revision = '88d196f6739e'
down_revision = '703d92cf0cad'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('occurrence_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('notification_type', sa.String(length=30), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['student_id'],
            ['students.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'student_id',
            'occurrence_id',
            'notification_type',
            name='uq_student_occurrence_notification'
        )
    )

    op.create_index(
        'ix_notifications_occurrence_id',
        'notifications',
        ['occurrence_id'],
        unique=False
    )

    op.create_index(
        'ix_notifications_student_id',
        'notifications',
        ['student_id'],
        unique=False
    )


def downgrade():

    op.drop_index(
        'ix_notifications_student_id',
        table_name='notifications'
    )

    op.drop_index(
        'ix_notifications_occurrence_id',
        table_name='notifications'
    )

    op.drop_table('notifications')
    op.drop_table('students')
