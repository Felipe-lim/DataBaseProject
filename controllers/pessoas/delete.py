from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa
from datetime import date

def delete_pessoa(db: Session, pessoa_id: str):
    db_pessoa = get_pessoa(db, pessoa_id)
    if db_pessoa:
        db.delete(db_pessoa)
        db.commit()

