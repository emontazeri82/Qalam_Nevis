 
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

class EditorialReview(db.Model):
    __tablename__ = "editorial_reviews"

    __table_args__ = (
        ForeignKeyConstraint(
            ["article_translation_id"],
            ["article_translations.id"],
            name="fk_editorial_reviews_translation",
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["reviewer_id"],
            ["users.id"],
            name="fk_editorial_reviews_reviewer",
            ondelete="RESTRICT"
        ),
        CheckConstraint(
            "decision IN ('approved', 'changes_requested', 'rejected')",
            name="ck_editorial_reviews_decision"
        ),
        Index(
            "ix_editorial_reviews_translation_id",
            "article_translation_id"
        ),
        Index(
            "ix_editorial_reviews_reviewer_id",
            "reviewer_id"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    article_translation_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    reviewer_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    decision: Mapped[str] = mapped_column(
        String(24),
        nullable=False
    )

    comment: Mapped[str | None] = mapped_column(
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
        back_populates="reviews"
    )
    reviewer: Mapped["User"] = relationship(
        "User",
        back_populates="editorial_reviews"
    )
