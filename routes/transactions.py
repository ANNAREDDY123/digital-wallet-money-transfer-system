from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.transaction import Transaction

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_transactions(
    type: str = None,
    status: str = None,
    date: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Transaction)

    if type:
        query = query.filter(
            Transaction.transaction_type == type
        )

    if status:
        query = query.filter(
            Transaction.status == status
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
