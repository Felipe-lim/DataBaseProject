from sqlalchemy.orm import Session
from models import Venda
from datetime import date


def create_venda(db: Session, 
                 data: date,
                 produto_especie: str,
                 produto_variedade: str,
                 comprador_id: str,
                 vendedor_id: str,
                 quantidade: int,
                 desconto: int,
                 forma_pagamento: str,
                 status_pagamento: str,
                 preco_final: int,
                 preco_normal: int):
    
    db_venda = Venda(data=data,
                     produto_especie=produto_especie,
                     produto_variedade=produto_variedade,
                     comprador_id=comprador_id,
                     vendedor_id=vendedor_id,
                     quantidade=quantidade,
                     desconto=desconto,
                     forma_pagamento=forma_pagamento,
                     status_pagamento=status_pagamento,
                     preco_final=preco_final,
                     preco_normal=preco_normal)
    
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda


def get_venda(db: Session, venda_id: int):
    return db.query(Venda).filter(Venda.id == venda_id).first()


def update_venda(db: Session, 
                 venda_id: int,
                 data: date,
                 produto_especie: str,
                 produto_variedade: str,
                 comprador_id: str,
                 vendedor_id: str,
                 quantidade: int,
                 desconto: int,
                 forma_pagamento: str,
                 status_pagamento: str,
                 preco_final: int,
                 preco_normal: int):
    
    db_venda = get_venda(db, venda_id)
    if db_venda:
        if data is not None:
            db_venda.data = data
        if produto_especie is not None:
            db_venda.produto_especie = produto_especie
        if produto_variedade is not None:
            db_venda.produto_variedade = produto_variedade
        if comprador_id is not None:
            db_venda.comprador_id = comprador_id
        if vendedor_id is not None:
            db_venda.vendedor_id = vendedor_id
        if quantidade is not None:
            db_venda.quantidade = quantidade
        if desconto is not None:
            db_venda.desconto = desconto
        if forma_pagamento is not None:
            db_venda.forma_pagamento = forma_pagamento
        if status_pagamento is not None:
            db_venda.status_pagamento = status_pagamento
        if preco_final is not None:
            db_venda.preco_final = preco_final
        if preco_normal is not None:
            db_venda.preco_normal = preco_normal
        
        db.commit()
        db.refresh(db_venda)
    return db_venda


def delete_venda(db: Session, venda_id: int):
    db_venda = get_venda(db, venda_id)
    if db_venda:
        db.delete(db_venda)
        db.commit()
        return True
    return False
