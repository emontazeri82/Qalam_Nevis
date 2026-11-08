
from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Text,
    Integer,
    DateTime,
    ForeignKeyConstraint,
    UniqueConstraint,
    CheckConstraint,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

if TYPE_CHECKING:
    from .article_translation import ArticleTranslation
    from .user import User

class ArticleRevision(db.Model):
    __tablename__ = "article_revisions"

    __table_args__ = (
        ForeignKeyConstraint(
            ["article_translation_id"],
            ["article_translations.id"],
            name="fk_article_revisions_translation",
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["edited_by_id"],
            ["users.id"],
            name="fk_article_revisions_editor",
            ondelete="SET NULL"
        ),
        UniqueConstraint(
            "article_translation_id",
            "revision_number",
            name="uq_article_revisions_number"
        ),
        CheckConstraint(
            "revision_number >= 1",
            name="ck_article_revisions_number"
        ),
        Index(
            "ix_article_revisions_translation_id",
            "article_translation_id"
        ),
        Index(
            "ix_article_revisions_edited_by_id",
            "edited_by_id"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    article_translation_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    edited_by_id: Mapped[UUID | None] = mapped_column(
        nullable=True
    )

    revision_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    body_document: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    )

    body_html: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    body_text: Mapped[str | None] = mapped_column(
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
        back_populates="revisions"
    )

    editor: Mapped["User | None"] = relationship(
        "User",
        back_populates="article_revisions"
    )
