from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Funcionario
from datetime import date


def get_funcionario(db: Session, cpf: str):
    return db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
