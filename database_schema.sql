CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE wallets(
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE,
    balance FLOAT DEFAULT 0
);

CREATE TABLE transactions(
    id INTEGER PRIMARY KEY,
    wallet_id INTEGER,
    transaction_reference VARCHAR(255) UNIQUE,
    transaction_type VARCHAR(50),
    amount FLOAT,
    status VARCHAR(50),
    created_at DATETIME
);
