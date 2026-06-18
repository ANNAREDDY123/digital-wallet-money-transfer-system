from pydantic import BaseModel


class WalletResponse(BaseModel):

    id: int

    user_id: int

    balance: float

    class Config:
        from_attributes = True
