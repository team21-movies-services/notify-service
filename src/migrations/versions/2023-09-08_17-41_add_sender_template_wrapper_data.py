"""add sender-template-wrapper data

Revision ID: 8b33275f74bf
Revises: 0ebd66ec9c87
Create Date: 2023-09-08 17:41:28.047380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm


# revision identifiers, used by Alembic.
revision: str = '8b33275f74bf'
down_revision: Union[str, None] = '0ebd66ec9c87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    db_bind = op.get_bind()
    session = orm.Session(bind=db_bind)
    sender = session.execute(
        sa.sql.text(
            """
            INSERT INTO public.senders (name, description, id, created_at, updated_at) VALUES
            ('no-reply@notify.service.com', 'Email for no reply', '63db0877-1b4e-4f8c-bfd8-57e6adc07a36', now(), now())
            ON CONFLICT DO NOTHING
            RETURNING id
    """
        )
    )
    sender_id = sender.fetchone()[0]


def downgrade() -> None:
    op.execute("DELETE FROM public.senders WHERE name = 'no-reply@notify.service.com'")
