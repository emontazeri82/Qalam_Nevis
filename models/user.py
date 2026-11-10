from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
  String,
  Text,
  DateTime,
  Boolean,
  CheckConstraint,
  Index,
  text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

from flask_login import UserMixin

if TYPE_CHECKING:
  from .article import Article
  from .media_asset import MediaAsset
  from .article_translation import ArticleTranslation
  from .editorial_review import EditorialReview
  from .article_status_history import ArticleStatusHistory
  from .article_revision import ArticleRevision
  from .user_role import UserRole

class User(UserMixin, db.Model):
  __tablename__ = "users"

  
  __table_args__ = (
    CheckConstraint(
        "preferred_language IN ('en', 'fa')",
        name="ck_users_language"
    ),
    CheckConstraint(
        "length(trim(username)) > 0",
        name="ck_users_username_nonblank"
    ),
    CheckConstraint(
        "length(trim(email)) > 0",
        name="ck_users_email_nonblank"
    ),
    CheckConstraint(
        "length(trim(display_name)) > 0",
        name="ck_users_display_name_nonblank"
    ),
    Index(
        "uq_users_username_lower",
        text("lower(username)"),
        unique=True
    ),
    Index(
      "uq_users_email_lower",
      text("lower(email)"),
      unique=True
    ),

  )
  id: Mapped[UUID] = mapped_column(
    primary_key=True,
    server_default=text("gen_random_uuid()")
  )

  email: Mapped[str] = mapped_column(
    String(320),
    nullable=False
  )

  username: Mapped[str] = mapped_column(
    String(80),
    nullable=False
  )

  password_hash: Mapped[str] = mapped_column(
    Text,
    nullable=False
  )

  display_name: Mapped[str] = mapped_column(
    String(160),
    nullable=False
  )

  bio: Mapped[str | None] = mapped_column(
    Text,
    nullable=True
  )

  preferred_language: Mapped[str] = mapped_column(
    String(2),
    nullable=False,
    server_default=text("'en'")
  )

  is_active: Mapped[bool] = mapped_column(
    Boolean,
    nullable=False,
    server_default=text("true")
  )

  last_login_at: Mapped[datetime | None] = mapped_column(
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
  articles: Mapped[list["Article"]] = relationship(
    "Article",
    back_populates="author"
  )

  uploaded_media: Mapped[list["MediaAsset"]] = relationship(
    "MediaAsset",
    back_populates="uploaded_by"
  )
  edited_translations: Mapped[list["ArticleTranslation"]] = relationship(
    "ArticleTranslation",
    back_populates="last_editor"
  )
  editorial_reviews: Mapped[list["EditorialReview"]] = relationship(
    "EditorialReview",
    back_populates="reviewer"
  )
  status_changes: Mapped[list["ArticleStatusHistory"]] = relationship(
      "ArticleStatusHistory",
      back_populates="changed_by"
  )
  article_revisions: Mapped[list["ArticleRevision"]] = relationship(
      "ArticleRevision",
      back_populates="editor"
  )
  user_roles: Mapped[list["UserRole"]] = relationship(
      "UserRole",
      back_populates="user"
  )