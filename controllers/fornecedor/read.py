from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Fornecedor
from datetime import date

def get_fornecedor(db: Session, cnpj: str):
    return db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()
