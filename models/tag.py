from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    DateTime,
    CheckConstraint,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

if TYPE_CHECKING:
  from .article_tag import ArticleTag

class Tag(db.Model):
  __tablename__ = "tags"

  __table_args__ = (
    UniqueConstraint(
      "slug",
      name="uq_tags_slug"
    ),
    CheckConstraint(
      "length(trim(slug)) > 0",
      name="ck_tags_slug_nonblank"
    ),
  )
  id: Mapped[UUID] = mapped_column(
    primary_key=True,
    server_default=text("gen_random_uuid()")
  )

  slug: Mapped[str] = mapped_column(
    String(100),
    nullable=False
  )

  name_en: Mapped[str] = mapped_column(
    String(120),
    nullable=False
  )

  name_fa: Mapped[str] = mapped_column(
    String(120),
    nullable=False
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
  
  article_tags: Mapped[list["ArticleTag"]] = relationship(
      "ArticleTag",
      back_populates="tag"
  )