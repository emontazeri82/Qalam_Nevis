
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
    from .article import Article
    from .media_asset import MediaAsset
    from .user import User
    from .editorial_review import EditorialReview
    from .article_status_history import ArticleStatusHistory
    from .article_revision import ArticleRevision

class ArticleTranslation(db.Model):
    __tablename__ = "article_translations"

    __table_args__ = (
        UniqueConstraint(
            "article_id",
            "language",
            name="uq_article_translations_article_language"
        ),
        UniqueConstraint(
            "language",
            "slug",
            name="uq_article_translations_language_slug"
        ),

        ForeignKeyConstraint(
            ["article_id"],
            ["articles.id"],
            name="fk_article_translations_article",
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["cover_media_id"],
            ["media_assets.id"],
            name="fk_article_translations_cover_media",
            ondelete="SET NULL"
        ),
        ForeignKeyConstraint(
            ["last_edited_by_id"],
            ["users.id"],
            name="fk_article_translations_last_editor",
            ondelete="SET NULL"
        ),

        CheckConstraint(
            "language IN ('en', 'fa')",
            name="ck_article_translations_language"
        ),
        CheckConstraint(
            "status IN ("
            "'draft', 'submitted', 'in_review', "
            "'changes_requested', 'approved', 'rejected', "
            "'published', 'archived')",
            name="ck_article_translations_status"
        ),
        CheckConstraint(
            "length(trim(title)) > 0",
            name="ck_article_translations_title_nonblank"
        ),
        CheckConstraint(
            "length(trim(slug)) > 0",
            name="ck_article_translations_slug_nonblank"
        ),
        CheckConstraint(
            "document_version >= 1",
            name="ck_article_translations_document_version"
        ),
        CheckConstraint(
            "lock_version >= 1",
            name="ck_article_translations_lock_version"
        ),

        Index(
            "ix_article_translations_article_id",
            "article_id"
        ),
        Index(
            "ix_article_translations_status",
            "status"
        ),
        Index(
            "ix_article_translations_cover_media_id",
            "cover_media_id"
        ),
        Index(
            "ix_article_translations_last_edited_by_id",
            "last_edited_by_id"
        ),
        Index(
            "ix_article_translations_published_at",
            "published_at"
        ),
        Index(
            "ix_article_translations_language_status",
            "language",
            "status"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    article_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    language: Mapped[str] = mapped_column(
        String(2),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String(350),
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

    editor_format: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=text("'unselected'")
    )

    document_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("1")
    )

    body_html: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    body_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    cover_media_id: Mapped[UUID | None] = mapped_column(
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        server_default=text("'draft'")
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    last_edited_by_id: Mapped[UUID | None] = mapped_column(
        nullable=True
    )

    lock_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("1")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    article: Mapped["Article"] = relationship(
        "Article",
        back_populates="translations"
    )

    cover_media: Mapped["MediaAsset | None"] = relationship(
        "MediaAsset",
        back_populates="cover_translations"
    )
    last_editor: Mapped["User | None"] = relationship(
        "User",
        back_populates="edited_translations"
    )
    reviews: Mapped[list["EditorialReview"]] = relationship(
        "EditorialReview",
        back_populates="translation"
    )
    status_history: Mapped[list["ArticleStatusHistory"]] = relationship(
        "ArticleStatusHistory",
        back_populates="translation"
    )
    revisions: Mapped[list["ArticleRevision"]] = relationship(
        "ArticleRevision",
        back_populates="translation"
    )
