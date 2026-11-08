
from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKeyConstraint,
    CheckConstraint,
    Index,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .extensions import db

if TYPE_CHECKING:
    from .article_translation import ArticleTranslation
    from .user import User 

class ArticleStatusHistory(db.Model):
    __tablename__ = "article_status_history"

    __table_args__ = (
        ForeignKeyConstraint(
            ["article_translation_id"],
            ["article_translations.id"],
            name="fk_article_status_history_translation",
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["changed_by_id"],
            ["users.id"],
            name="fk_article_status_history_user",
            ondelete="SET NULL"
        ),
        CheckConstraint(
            "old_status IS NULL OR old_status IN ("
            "'draft', 'submitted', 'in_review', "
            "'changes_requested', 'approved', 'rejected', "
            "'published', 'archived')",
            name="ck_article_status_history_old_status"
        ),
        CheckConstraint(
            "new_status IN ("
            "'draft', 'submitted', 'in_review', "
            "'changes_requested', 'approved', 'rejected', "
            "'published', 'archived')",
            name="ck_article_status_history_new_status"
        ),
        Index(
            "ix_article_status_history_translation_id",
            "article_translation_id"
        ),
        Index(
            "ix_article_status_history_changed_by_id",
            "changed_by_id"
        ),
        Index(
            "ix_article_status_history_created_at",
            "created_at"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    article_translation_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    changed_by_id: Mapped[UUID | None] = mapped_column(
        nullable=True
    )

    old_status: Mapped[str | None] = mapped_column(
        String(24),
        nullable=True
    )

    new_status: Mapped[str] = mapped_column(
        String(24),
        nullable=False
    )

    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    translation: Mapped["ArticleTranslation"] = relationship(
        "ArticleTranslation",
        back_populates="status_history"
    )
    changed_by: Mapped["User | None"] = relationship(
        "User",
        back_populates="status_changes"
    )