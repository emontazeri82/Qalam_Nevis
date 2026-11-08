from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

if TYPE_CHECKING:
  from .user import User
  from .category import Category
  from .article_translation import ArticleTranslation
  from .article_tag import ArticleTag

class Article(db.Model):
  __tablename__ = "articles"

  __table_args__ = (
    ForeignKeyConstraint(
      ["author_id"],
      ["users.id"],
      name="fk_articles_author",
      ondelete="RESTRICT"
    ),
    ForeignKeyConstraint(
      ["category_id"],
      ["categories.id"],
      name="fk_articles_category",
      ondelete="RESTRICT"
    ),
    Index("ix_articles_author_id", "author_id"),
    Index("ix_articles_category_id", "category_id"),
    Index("ix_articles_deleted_at", "deleted_at"),
  ) 
  id: Mapped[UUID] = mapped_column(
      primary_key=True,
      server_default=text("gen_random_uuid()")
  )

  author_id: Mapped[UUID] = mapped_column(
      nullable=False
  )

  category_id: Mapped[UUID] = mapped_column(
      nullable=False
  )

  deleted_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
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
  author: Mapped["User"] = relationship(
    "User",
    back_populates="articles"
  )

  category: Mapped["Category"] = relationship(
    "Category",
    back_populates="articles"
  )

  translations: Mapped[list["ArticleTranslation"]] = relationship(
    "ArticleTranslation",
    back_populates="article"
  )

  article_tags: Mapped[list["ArticleTag"]] = relationship(
      "ArticleTag",
      back_populates="article"
  )