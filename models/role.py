from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
  String, Text, 
  DateTime, text,
  CheckConstraint,
  UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .extensions import db

if TYPE_CHECKING:
    from .user_role import UserRole

class Role(db.Model):
  __tablename__ = "roles"

  __table_args__ = (
    UniqueConstraint(
        "code",
        name="uq_roles_code"
    ),
    CheckConstraint(
      "length(trim(code)) > 0",
      name="ck_roles_code_nonblank"
    ),
  )

  id: Mapped[UUID] = mapped_column(
    primary_key=True,
    server_default=text("gen_random_uuid()")
  )
  code: Mapped[str] = mapped_column(
    String(30),
    nullable=False
  )
  description: Mapped[str | None] = mapped_column(
    Text,
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
  user_roles: Mapped[list["UserRole"]] = relationship(
      "UserRole",
      back_populates="role"
  )