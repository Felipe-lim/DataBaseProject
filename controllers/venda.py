from sqlalchemy.orm import Session
from models import Venda
from datetime import date


def create_venda(db: Session, 
                 data: date,
                 comprador_id: str,
                 vendedor_id: str,
                 preco_normal: int,
                 desconto: int,
                 preco_final: int,
                 forma_pagamento: str,
                 status_pagamento: str):
    
    db_venda = Venda(data=data,
                     comprador_id=comprador_id,
                     vendedor_id=vendedor_id,
                     preco_normal=preco_normal,
                     desconto=desconto,
                     preco_final=preco_final,
                     forma_pagamento=forma_pagamento,
                     status_pagamento=status_pagamento)
    
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda


def get_venda(db: Session, venda_id: int):
    return db.query(Venda).filter(Venda.id == venda_id).first()


def update_venda(db: Session, 
                 venda_id: int,
                 data: date = None,
                 comprador_id: str = None,
                 vendedor_id: str = None,
                 preco_normal: int = None,
                 desconto: int = None,
                 preco_final: int = None,
                 forma_pagamento: str = None,
                 status_pagamento: str = None):
    
    db_venda = get_venda(db, venda_id)
    if db_venda:
        if data is not None:
            db_venda.data = data
        if comprador_id is not None:
            db_venda.comprador_id = comprador_id
        if vendedor_id is not None:
            db_venda.vendedor_id = vendedor_id
        if preco_normal is not None:
            db_venda.preco_normal = preco_normal
        if desconto is not None:
            db_venda.desconto = desconto
        if preco_final is not None:
            db_venda.preco_final = preco_final
        if forma_pagamento is not None:
            db_venda.forma_pagamento = forma_pagamento
        if status_pagamento is not None:
            db_venda.status_pagamento = status_pagamento
        
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
