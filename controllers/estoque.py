from sqlalchemy.orm import Session
from database.models import Estoque
from sqlalchemy import and_


def create_estoque(db: Session, 
                   especie: str, 
                   variedade: str,
                   quantidade: int,
                   fornecedor: str,
                   custo: int,
                   preco: int):
    
    db_estoque = Estoque(especie=especie, 
                         variedade=variedade,
                         quantidade=quantidade,
                         fornecedor=fornecedor,
                         custo=custo,
                         preco=preco)
    db.add(db_estoque)
    db.commit()
    db.refresh(db_estoque)
    return db_estoque


def get_estoque(db: Session, especie: str, variedade: str):
    return db.query(Estoque).filter(and_(Estoque.especie == especie, Estoque.variedade == variedade)).first()


def update_estoque(db: Session, 
                   especie_atual: str,
                   especie_nova: str,
                   variedade_atual: str,
                   variedade_nova: str,
                   quantidade: int,
                   fornecedor: str,
                   custo: int,
                   preco: int):
    
    db_estoque = get_estoque(db, especie_atual, variedade_atual)
    if db_estoque:
        if especie_nova is not None:
            db_estoque.especie = especie_nova
        if variedade_nova is not None:
            db_estoque.variedade = variedade_nova
        if quantidade is not None:
            db_estoque.quantidade = quantidade
        if fornecedor is not None:
            db_estoque.fornecedor = fornecedor
        if custo is not None:
            db_estoque.custo = custo
        if preco is not None:
            db_estoque.preco = preco

        db.commit()
        db.refresh(db_estoque)
    return db_estoque


def delete_estoque(db: Session, especie: str, variedade: str):
    db_estoque = get_estoque(db, especie, variedade)
    if db_estoque:
        db.delete(db_estoque)
        db.commit()
