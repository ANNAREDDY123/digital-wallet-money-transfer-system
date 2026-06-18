from pydantic import BaseModel, Field


class TransferMoney(BaseModel):
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: float = Field(gt=0)
