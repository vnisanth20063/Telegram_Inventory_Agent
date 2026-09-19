from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from .database import Base


class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    product_name = Column(
        String,
        nullable=False
    )

    current_stock = Column(
        Integer,
        nullable=False
    )

    daily_demand = Column(
        Integer,
        nullable=False
    )

    lead_time_days = Column(
        Integer,
        nullable=False
    )

    safety_stock = Column(
        Integer,
        nullable=False
    )


class TelegramMessage(Base):

    __tablename__ = "telegram_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    telegram_user_id = Column(
        String,
        nullable=False
    )

    username = Column(
        String,
        nullable=True
    )

    message = Column(
        Text,
        nullable=False
    )

    response = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )