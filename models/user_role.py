
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

if TYPE_CHECKING:
    from .user import User
    from .role import Role

class UserRole(db.Model):
    __tablename__ = "user_roles"

    __table_args__ = (
        PrimaryKeyConstraint(
            "user_id",
            "role_id",
            name="pk_user_roles"
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_user_roles_user",
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name="fk_user_roles_role",
            ondelete="CASCADE"
        ),
        Index(
            "ix_user_roles_role_id",
            "role_id"
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    role_id: Mapped[UUID] = mapped_column(
        nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_roles"
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user_roles"
    )
