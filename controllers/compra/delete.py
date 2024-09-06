from sqlalchemy.orm import Session
from models import Compra
from datetime import date


def delete_compra(db: Session, compra_id: int):
    db_compra = get_compra(db, compra_id)
    if db_compra:
        db.delete(db_compra)
        db.commit()
        return True
    return False
