from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Fornecedor
from datetime import date

def delete_fornecedor(db: Session, cnpj: str):
    db_fornecedor = get_fornecedor(db, cnpj)
    if db_fornecedor:
        db.delete(db_fornecedor)
        db.commit()
