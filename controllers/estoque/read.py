from sqlalchemy.orm import Session
from models import Estoque
from sqlalchemy import and_


def get_estoque(db: Session, especie: str, variedade: str):
    return db.query(Estoque).filter(and_(Estoque.especie == especie, Estoque.variedade == variedade)).first()
