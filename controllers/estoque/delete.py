from sqlalchemy.orm import Session
from models import Estoque
from sqlalchemy import and_

def delete_estoque(db: Session, especie: str, variedade: str):
    db_estoque = get_estoque(db, especie, variedade)
    if db_estoque:
        db.delete(db_estoque)
        db.commit()
