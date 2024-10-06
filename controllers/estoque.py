from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from database.models import Estoque
from sqlalchemy import and_
from database.models import Catalogo
from database.models import Fornecedor


def create_estoque(db: Session, 
                   especie: str, 
                   variedade: str,
                   quantidade: int,
                   fornecedor_cnpj: str,
                   custo: int,
                   preco: int):

    # Fetch the corresponding catalogo entry
    catalogo_item = db.query(Catalogo).filter_by(especie=especie, variedade=variedade).first()
    
    if not catalogo_item:
        # Create new catalogo entry if it doesn't exist
        new_catalogo_item = Catalogo(especie=especie, variedade=variedade)
        db.add(new_catalogo_item)
        db.commit()
        db.refresh(new_catalogo_item)
    
    # Fetch the fornecedor using its CNPJ
    fornecedor_item = db.query(Fornecedor).filter_by(cnpj=fornecedor_cnpj).first()

    if not fornecedor_item:
        raise Exception(f"Fornecedor with CNPJ {fornecedor_cnpj} not found.")
    
    # Verificar se já existe um item de estoque com essa chave primária (especie, variedade, fornecedor, custo)
    estoque_existente = db.query(Estoque).filter(
        and_(
            Estoque.especie == especie,
            Estoque.variedade == variedade,
            Estoque.fornecedor == fornecedor_cnpj,
            Estoque.custo == custo
        )
    ).first()
    
    if estoque_existente:
        # Incrementa a quantidade existente com a nova quantidade
        estoque_existente.quantidade += quantidade
        db.commit()
        db.refresh(estoque_existente)
        return estoque_existente
    
    else:
        # Criar a entrada de Estoque com as chaves primárias corretas
        db_estoque = Estoque(
            especie=especie, 
            variedade=variedade,
            quantidade=quantidade,
            fornecedor=fornecedor_item.cnpj,
            custo=custo,
            preco=preco
        )

        try:
            db.add(db_estoque)
            db.commit()
            db.refresh(db_estoque)
            return db_estoque

        except IntegrityError:
            db.rollback()
            raise Exception("Erro ao cadastrar o produto no estoque. Verifique os dados e tente novamente.")


def get_estoque(db: Session, especie: str, variedade: str, fornecedor: str, custo: int):
    return db.query(Estoque).filter(
        and_(
            Estoque.especie == especie,
            Estoque.variedade == variedade,
            Estoque.fornecedor == fornecedor,
            Estoque.custo == custo
        )
    ).first()


def update_estoque(db: Session, 
                   especie_atual: str,
                   variedade_atual: str,
                   fornecedor_atual: str,
                   custo_atual: int,
                   especie_nova: str = None,
                   variedade_nova: str = None,
                   quantidade: int = None,
                   fornecedor_novo: str = None,
                   custo_novo: int = None,
                   preco: int = None):
    
    # Busca o estoque atual com a chave composta
    db_estoque = get_estoque(db, especie_atual, variedade_atual, fornecedor_atual, custo_atual)
    if db_estoque:
        if especie_nova is not None:
            db_estoque.especie = especie_nova
        if variedade_nova is not None:
            db_estoque.variedade = variedade_nova
        if quantidade is not None:
            db_estoque.quantidade = quantidade
        if fornecedor_novo is not None:
            db_estoque.fornecedor = fornecedor_novo
        if custo_novo is not None:
            db_estoque.custo = custo_novo
        if preco is not None:
            db_estoque.preco = preco

        db.commit()
        db.refresh(db_estoque)
    return db_estoque


def delete_estoque(db: Session, especie: str, variedade: str, fornecedor: str, custo: int):
    db_estoque = get_estoque(db, especie, variedade, fornecedor, custo)
    if db_estoque:
        db.delete(db_estoque)
        db.commit()


def get_all_estoque(db: Session):
    return db.query(Estoque).all()


def update_estoque_quantity(db: Session, especie: str, variedade: str, fornecedor: str, custo: int, nova_quantidade: int):
    # Obtém o estoque com base na chave composta
    db_estoque = get_estoque(db, especie, variedade, fornecedor, custo)
    
    # Verifica se o estoque existe
    if db_estoque:
        # Atualiza a quantidade
        db_estoque.quantidade = nova_quantidade
        
        # Salva as alterações no banco de dados
        db.commit()
        db.refresh(db_estoque)
        
    return db_estoque
