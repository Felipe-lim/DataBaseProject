from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from models import Estoque
from sqlalchemy import and_
from models import Catalogo



def create_estoque(db: Session, 
                   especie: str, 
                   variedade: str,
                   quantidade: int,
                   fornecedor: str,
                   custo: int,
                   preco: int):
    
    catalogo_item = db.query(Catalogo).filter_by(especie=especie, variedade=variedade).first()
    
    if not catalogo_item:
        new_catalogo_item = Catalogo(especie=especie, variedade=variedade)
        db.add(new_catalogo_item)
        db.commit()
        db.refresh(new_catalogo_item)
    
    db_estoque = Estoque(especie=especie, 
                         variedade=variedade,
                         quantidade=quantidade,
                         fornecedor=fornecedor,
                         custo=custo,
                         preco=preco)
    
    try:
        db.add(db_estoque)
        db.commit()
        db.refresh(db_estoque)
        return db_estoque
    
    except IntegrityError:
        db.rollback()
        raise Exception("Erro ao cadastrar o produto no estoque. Verifique os dados e tente novamente.")
    



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


def get_all_estoque(db: Session):
    return db.query(Estoque).all()

def update_estoque_quantity(db: Session, especie: str, variedade: str, nova_quantidade: int):
    # Obtém o estoque com base na espécie e variedade
    db_estoque = get_estoque(db, especie, variedade)
    
    # Verifica se o estoque existe
    if db_estoque:
        # Atualiza a quantidade
        db_estoque.quantidade = nova_quantidade
        
        # Salva as alterações no banco de dados
        db.commit()
        db.refresh(db_estoque)
        
    return db_estoque
