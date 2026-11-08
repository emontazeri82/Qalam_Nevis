
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

if TYPE_CHECKING: 
    from .article import Article
    from .tag import Tag

class ArticleTag(db.Model):
    __tablename__ = "article_tags"

    __table_args__ = (
        PrimaryKeyConstraint(
            "article_id",
            "tag_id",
            name="pk_article_tags"
        ),
        ForeignKeyConstraint(
            ["article_id"],
            ["articles.id"],
            name="fk_article_tags_article",
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
            name="fk_article_tags_tag",
            ondelete="CASCADE"
        ),
        Index(
            "ix_article_tags_tag_id",
            "tag_id"
        ),
    )

    article_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    tag_id: Mapped[UUID] = mapped_column(
        nullable=False
    )
    
    article: Mapped["Article"] = relationship(
        "Article",
        back_populates="article_tags"
    )

    tag: Mapped["Tag"] = relationship(
        "Tag",
        back_populates="article_tags"
    )
