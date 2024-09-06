from sqlalchemy.orm import Session
from models import Carrinho


def get_carrinho(db: Session, carrinho_id: int):
    return db.query(Carrinho).filter(Carrinho.id == carrinho_id).first()
