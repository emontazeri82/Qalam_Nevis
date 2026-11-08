from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
  String,
  Integer,
  Boolean,
  DateTime,
  UniqueConstraint,
  CheckConstraint,
  text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

if TYPE_CHECKING:
  from .article import Article

class Category(db.Model):
  __tablename__ = "categories"

  __table_args__ = (
    UniqueConstraint(
      "slug",
      name="uq_categories_slug"
    ),
    CheckConstraint(
      "length(trim(slug)) > 0",
      name="ck_categories_slug_nonblank"
    ),
    CheckConstraint(
      "length(trim(name_en)) > 0",
      name="ck_categories_name_en_nonblank"
    ),
    CheckConstraint(
      "length(trim(name_fa)) > 0",
      name="ck_categories_name_fa_nonblank"
    ),
  )

  id: Mapped[UUID] = mapped_column(
    primary_key=True,
    server_default=text("gen_random_uuid()")
  )

  slug: Mapped[str] = mapped_column(
    String(80),
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

  sort_order: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
    server_default=text("0")
  )

  is_active: Mapped[bool] = mapped_column(
    Boolean,
    nullable=False,
    server_default=text("true")
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

  articles: Mapped[list["Article"]] = relationship(
    "Article",
    back_populates="category"
  )