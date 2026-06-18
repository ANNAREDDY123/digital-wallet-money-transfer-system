from models.wallet import Wallet


def create_wallet(
    db,
    user_id
):
    wallet = Wallet(
        user_id=user_id,
        balance=0
    )

    db.add(wallet)

    db.commit()

    db.refresh(wallet)

    return wallet
