from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime

from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    wallet_id = Column(
        Integer,
        ForeignKey("wallets.id")
    )

    transaction_reference = Column(
        String,
        unique=True
    )

    transaction_type = Column(String)

    amount = Column(Float)

    status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
