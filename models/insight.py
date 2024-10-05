from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from configs.database import Base
from models.mixins import TimeStampMixin


class Insight(Base, TimeStampMixin):
    __tablename__ = "insights"

    id = Column(UUID(as_uuid=True), primary_key=True)
    prompt = Column(String, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("files.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    data = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
