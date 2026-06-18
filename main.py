from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import (
    Base,
    engine
)

from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction

from routes.auth import router as auth_router
from routes.wallet import router as wallet_router
from routes.transactions import router as transaction_router
from routes.transfers import router as transfer_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Digital Wallet & Money Transfer System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(transfer_router)


@app.get("/")
def home():

    return {
        "message":
        "Digital Wallet & Money Transfer System"
    }
