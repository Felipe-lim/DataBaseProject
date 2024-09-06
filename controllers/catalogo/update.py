from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import Catalogo
from datetime import date


from sqlalchemy.orm import Session
from models import Catalogo

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

