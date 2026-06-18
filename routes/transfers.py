from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.wallet import Wallet
from models.transaction import Transaction

from schemas.transfer import TransferMoney

from services.transfer_service import (
    generate_reference
)

router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/send")
def send_money(
    data: TransferMoney,
    db: Session = Depends(get_db)
):

    if (
        data.sender_wallet_id ==
        data.receiver_wallet_id
    ):

        raise HTTPException(
            status_code=400,
            detail="Self transfer not allowed"
        )

    sender = db.query(Wallet).filter(
        Wallet.id == data.sender_wallet_id
    ).first()

    receiver = db.query(Wallet).filter(
        Wallet.id == data.receiver_wallet_id
    ).first()

    if not sender:

        raise HTTPException(
            status_code=404,
            detail="Sender wallet not found"
        )

    if not receiver:

        raise HTTPException(
            status_code=404,
            detail="Receiver wallet not found"
        )

    if sender.balance < data.amount:

        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    sender.balance -= data.amount

    receiver.balance += data.amount

    reference = generate_reference()

    debit_transaction = Transaction(
        wallet_id=sender.id,
        transaction_reference=reference + "-D",
        transaction_type="Debit",
        amount=data.amount,
        status="Success"
    )

    credit_transaction = Transaction(
        wallet_id=receiver.id,
        transaction_reference=reference + "-C",
        transaction_type="Credit",
        amount=data.amount,
        status="Success"
    )

    db.add(debit_transaction)
    db.add(credit_transaction)

    db.commit()

    return {
        "message": "Transfer successful",
        "reference": reference,
        "amount": data.amount
    }


@router.get("/{transaction_id}")
def get_transfer(
    transaction_id: int,
    db: Session = Depends(get_db)
):

    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction
