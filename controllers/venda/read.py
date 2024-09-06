from sqlalchemy.orm import Session
from models import Venda
from datetime import date

def get_venda(db: Session, venda_id: int):
    return db.query(Venda).filter(Venda.id == venda_id).first()
