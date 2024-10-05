import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from configs.database import Base
from models.mixins import TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    is_admin = Column(Boolean, default=False)
