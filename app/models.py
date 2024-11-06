from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column
from app.database import db

class MessageLog(db.Model):
    __tablename__ = "message_log"

    id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String, nullable=False)
    recipient = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    status = mapped_column(String, nullable=False)
    timestamp = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
