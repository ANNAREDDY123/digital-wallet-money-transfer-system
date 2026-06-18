from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.wallet import Wallet
from models.transaction import Transaction

from schemas.transaction import (
    AddMoney,
    WithdrawMoney
)

from services.transfer_service import (
    generate_reference
)

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/{user_id}")
def get_wallet(
    user_id: int,
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id
    ).first()

    if not wallet:

        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    return wallet


@router.post("/add-money")
def add_money(
    data: AddMoney,
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.id == data.wallet_id
    ).first()

    if not wallet:

        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    wallet.balance += data.amount

    transaction = Transaction(
        wallet_id=wallet.id,
        transaction_reference=generate_reference(),
        transaction_type="Credit",
        amount=data.amount,
        status="Success"
    )

    db.add(transaction)

    db.commit()

    return {
        "message": "Money added successfully",
        "balance": wallet.balance
    }


@router.post("/withdraw")
def withdraw_money(
    data: WithdrawMoney,
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.id == data.wallet_id
    ).first()

    if not wallet:

        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    if wallet.balance < data.amount:

        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    wallet.balance -= data.amount

    transaction = Transaction(
        wallet_id=wallet.id,
        transaction_reference=generate_reference(),
        transaction_type="Debit",
        amount=data.amount,
        status="Success"
    )

    db.add(transaction)

    db.commit()

    return {
        "message": "Withdrawal successful",
        "balance": wallet.balance
    }


@router.get("/transactions/{wallet_id}")
def wallet_transactions(
    wallet_id: int,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Transaction).filter(
        Transaction.wallet_id == wallet_id
    )

    total_records = query.count()

    total_pages = (
        total_records + limit - 1
    ) // limit

    transactions = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total_records,
        "current_page": page,
        "total_pages": total_pages,
        "data": transactions
    }
