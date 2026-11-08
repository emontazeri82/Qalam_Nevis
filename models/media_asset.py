
from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    DateTime,
    ForeignKeyConstraint,
    UniqueConstraint,
    CheckConstraint,
    Index,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

if TYPE_CHECKING:
    from .article_translation import ArticleTranslation
    from .user import User

class MediaAsset(db.Model):
    __tablename__ = "media_assets"

    __table_args__ = (
        UniqueConstraint(
            "storage_key",
            name="uq_media_assets_storage_key"
        ),
        ForeignKeyConstraint(
            ["uploaded_by_id"],
            ["users.id"],
            name="fk_media_assets_uploaded_by",
            ondelete="RESTRICT"
        ),
        CheckConstraint(
            "size_bytes >= 0",
            name="ck_media_assets_size"
        ),
        CheckConstraint(
            "width IS NULL OR width > 0",
            name="ck_media_assets_width"
        ),
        CheckConstraint(
            "height IS NULL OR height > 0",
            name="ck_media_assets_height"
        ),
        Index(
            "ix_media_assets_uploaded_by_id",
            "uploaded_by_id"
        ),
        Index(
            "ix_media_assets_sha256",
            "sha256"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    uploaded_by_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    storage_key: Mapped[str] = mapped_column(
        String(600),
        nullable=False
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    mime_type: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    sha256: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
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

    cover_translations: Mapped[list["ArticleTranslation"]] = relationship(
        "ArticleTranslation",
        back_populates="cover_media"
    )

    uploaded_by: Mapped["User"] = relationship(
        "User",
        back_populates="uploaded_media"
    )