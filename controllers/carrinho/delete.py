from sqlalchemy.orm import Session
from models import Carrinho


def delete_carrinho(db: Session, carrinho_id: int):
    db_carrinho = get_carrinho(db, carrinho_id)
    if db_carrinho:
        db.delete(db_carrinho)
        db.commit()
        return True
    return False
