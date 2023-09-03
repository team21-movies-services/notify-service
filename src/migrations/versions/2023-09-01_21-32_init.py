"""init

Revision ID: 77bc96ecfcaa
Revises: 
Create Date: 2023-09-01 21:32:45.122726

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '77bc96ecfcaa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'senders',
        sa.Column('name', sa.String(length=127), nullable=False, comment='Имя отправителя'),
        sa.Column('description', sa.String(length=255), nullable=False, comment='Описание отправителя'),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('id', name='sender_pkey'),
        schema='public',
    )
    op.create_table(
        'wrappers',
        sa.Column('name', sa.String(length=127), nullable=False, comment='Название враппера'),
        sa.Column('body', sa.Text(), nullable=False, comment='Тело враппера'),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('id', name='wrapper_pkey'),
        schema='public',
    )
    op.create_table(
        'templates',
        sa.Column('name', sa.String(length=127), nullable=False, comment='Название шаблона'),
        sa.Column('description', sa.String(length=255), nullable=False, comment='Описание шаблона'),
        sa.Column('subject', sa.String(length=127), nullable=True, comment='Заголовок шаблона'),
        sa.Column('body', sa.Text(), nullable=False, comment='Тело шаблона'),
        sa.Column('json_vars', postgresql.JSONB(astext_type=sa.Text()), nullable=False, comment='Переменные шаблона'),
        sa.Column('wrapper_id', sa.UUID(), nullable=False, comment='ID враппера'),
        sa.Column('sender_id', sa.UUID(), nullable=True, comment='ID отправителя'),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(['sender_id'], ['public.senders.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['wrapper_id'], ['public.wrappers.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='template_pkey'),
        schema='public',
    )
    op.create_table(
        'notifications',
        sa.Column('event_name', sa.String(length=127), nullable=False, comment='Название события'),
        sa.Column('template_id', sa.UUID(), nullable=False, comment='ID шаблона'),
        sa.Column(
            'notification_type',
            postgresql.ENUM('instant', 'scheduled', 'periodic', name='notification_type'),
            nullable=False,
            comment='Типы нотификаций',
        ),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(['template_id'], ['public.templates.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='notification_pkey'),
        schema='public',
    )
    op.create_table(
        'schedule',
        sa.Column('crontab', sa.String(length=127), nullable=True, comment='Шаблон расписания'),
        sa.Column('start_time', sa.TIMESTAMP(), nullable=True, comment='Время старта нотификации'),
        sa.Column('completed', sa.BOOLEAN(), nullable=False, comment='Флаг завершения расписания'),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False, comment='Содержимое нотификации'),
        sa.Column('notification_id', sa.UUID(), nullable=False, comment='ID нотификации'),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(
            ['notification_id'], ['public.notifications.id'], onupdate='CASCADE', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name='schedule_pkey'),
        schema='public',
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule', schema='public')
    op.drop_table('notifications', schema='public')
    op.drop_table('templates', schema='public')
    op.drop_table('wrappers', schema='public')
    op.drop_table('senders', schema='public')
    # ### end Alembic commands ###
