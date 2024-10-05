from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from configs.database import Base
from models.mixins import TimeStampMixin


class File(Base, TimeStampMixin):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, index=True, nullable=False)
    url = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
