from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Funcionario
from datetime import date


def delete_funcionario(db: Session, cpf: str):
    db_funcionario = get_funcionario(db, cpf)
    if db_funcionario:
        db.delete(db_funcionario)
        db.commit()
