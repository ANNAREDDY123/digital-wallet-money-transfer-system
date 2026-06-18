# digital-wallet-money-transfer-system
FastAPI-based Digital Wallet &amp; Money Transfer System with JWT Authentication, Wallet Transactions, Money Transfers, Transaction Tracking, and SQLAlchemy ORM.
# Digital Wallet & Money Transfer System

## Features

- JWT Authentication
- User Registration & Login
- Auto Wallet Creation
- Add Money
- Withdraw Money
- Money Transfer
- Transaction History
- Transaction Filtering
- Pagination
- SQLAlchemy ORM
- SQLite Database
- Docker Support
- Swagger Documentation

## APIs

### Authentication

- POST /auth/register
- POST /auth/login

### Wallet

- GET /wallet/{user_id}
- POST /wallet/add-money
- POST /wallet/withdraw
- GET /wallet/transactions/{wallet_id}

### Transfers

- POST /transfers/send
- GET /transfers/{transaction_id}

### Transactions

- GET /transactions

## Run

pip install -r requirements.txt

uvicorn main:app --reload

## Swagger

http://127.0.0.1:8000/docs
