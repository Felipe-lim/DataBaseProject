from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import Catalogo
from datetime import date


from sqlalchemy.orm import Session
from models import Catalogo


def delete_catalogo(db:Session, especie:str, variedade:str):
    db_catalogo = get_catalogo(db, especie, variedade)
    if db_catalogo:
        db.delete(db_catalogo)
        db.commit()
