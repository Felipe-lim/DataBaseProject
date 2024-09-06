from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Cliente
from datetime import date

def delete_cliente(db: Session, cpf: str):
    db_cliente = get_cliente(db, cpf)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()