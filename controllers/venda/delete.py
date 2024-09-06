from sqlalchemy.orm import Session
from models import Venda
from datetime import date


def delete_venda(db: Session, venda_id: int):
    db_venda = get_venda(db, venda_id)
    if db_venda:
        db.delete(db_venda)
        db.commit()
        return True
    return False
