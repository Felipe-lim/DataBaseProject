from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import Catalogo
from datetime import date


from sqlalchemy.orm import Session
from models import Catalogo



def get_catalogo(db: Session, especie: str, variedade: str):
    return db.query(Catalogo).filter(and_(Catalogo.especie == especie, Catalogo.variedade == variedade)).first()
