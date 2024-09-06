from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Cliente
from datetime import date



def get_cliente(db: Session, cpf: str):
    return db.query(Cliente).filter(Cliente.cpf == cpf).first()