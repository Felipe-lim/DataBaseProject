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


def get_catalogo(db: Session, especie: str, variedade: str):
    return db.query(Catalogo).filter(and_(Catalogo.especie == especie, Catalogo.variedade == variedade)).first()


def update_catalogue(db: Session, 
                     especie_atual: str,
                     especie_nova: str,  
                     variedade_atual: str,
                     variedade_nova: str,
                     nome_popular: str,
                     origem: str,
                     ambiente: str,
                     cuidado: str,
                     utilidade: str):
    
    db_catalogo = get_catalogo(db, especie_atual, variedade_atual)
    if db_catalogo:
        if especie_nova is not None:
            db_catalogo.especie = especie_nova
        if variedade_nova is not None:
            db_catalogo.variedade = variedade_nova
        if nome_popular is not None:
            db_catalogo.nome_popular = nome_popular
        if origem is not None:
            db_catalogo.origem = origem
        if ambiente is not None:
            db_catalogo.ambiente = ambiente
        if cuidado is not None:
            db_catalogo.cuidado = cuidado
        if utilidade is not None:
            db_catalogo.utilidade = utilidade
        
        db.commit()
        db.refresh(db_catalogo)

    return db_catalogo


def delete_catalogo(db:Session, especie:str, variedade:str):
    db_catalogo = get_catalogo(db, especie, variedade)
    if db_catalogo:
        db.delete(db_catalogo)
        db.commit()
