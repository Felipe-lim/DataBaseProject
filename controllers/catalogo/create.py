from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import Catalogo
from datetime import date


from sqlalchemy.orm import Session
from models import Catalogo

def create_catalogo(db: Session, 
                           especie: str, 
                           variedade: str,
                           nome_popular: str,
                           origem: str,
                           ambiente: str,
                           cuidado: str,
                           utilidade: str):
    
    db_catalogo = Catalogo(especie=especie, 
                                  variedade=variedade,
                                  nome_popular=nome_popular,
                                  origem=origem,
                                  ambiente=ambiente,
                                  cuidado=cuidado,
                                  utilidade=utilidade)
    
    db.add(db_catalogo)
    db.commit()
    db.refresh(db_catalogo)
    return db_catalogo
