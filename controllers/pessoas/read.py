from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa
from datetime import date


def get_pessoa(db: Session, pessoa_id: str):
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
