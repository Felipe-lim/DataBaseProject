from sqlalchemy.orm import Session
from database.models import Carrinho


def create_carrinho(db: Session,
                    id_venda: int,
                    especie: str,
                    variedade: str,
                    quantidade: int):
    db_carrinho = Carrinho(id_venda=id_venda,
                           especie=especie,
                           variedade=variedade,
                           quantidade=quantidade)

    db.add(db_carrinho)
    db.commit()
    db.refresh(db_carrinho)
    return db_carrinho


def get_carrinho(db: Session, carrinho_id: int):
    return db.query(Carrinho).filter(Carrinho.id == carrinho_id).first()


def update_carrinho(db: Session,
                    carrinho_id: int,
                    id_venda: int = None,
                    especie: str = None,
                    variedade: str = None,
                    quantidade: int = None):
    
    db_carrinho = get_carrinho(db, carrinho_id)
    if db_carrinho:
        if id_venda is not None:
            db_carrinho.id_venda = id_venda
        if especie is not None:
            db_carrinho.especie = especie
        if variedade is not None:
            db_carrinho.variedade = variedade
        if quantidade is not None:
            db_carrinho.quantidade = quantidade
        
        db.commit()
        db.refresh(db_carrinho)
    return db_carrinho


def delete_carrinho(db: Session, carrinho_id: int):
    db_carrinho = get_carrinho(db, carrinho_id)
    if db_carrinho:
        db.delete(db_carrinho)
        db.commit()
        return True
    return False
