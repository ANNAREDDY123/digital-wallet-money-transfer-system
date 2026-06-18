from pydantic import (
    BaseModel,
    Field
)


class AddMoney(BaseModel):

    wallet_id: int

    amount: float = Field(gt=0)


class WithdrawMoney(BaseModel):

    wallet_id: int

    amount: float = Field(gt=0)
