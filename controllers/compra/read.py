from sqlalchemy.orm import Session
from models import Compra
from datetime import date

def get_compra(db: Session, compra_id: int):
    return db.query(Compra).filter(Compra.id == compra_id).first()

