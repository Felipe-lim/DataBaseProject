from sqlalchemy.orm import Session
from database.models import Compra
from datetime import date


def create_compra(db: Session, 
                  data: date,
                  fornecedor_cnpj: str,
                  quantidade: int,
                  especie: str,
                  variedade: str,
                  custo: int,
                  forma_pagamento: str):
    
    db_compra = Compra(data=data,
                       fornecedor_cnpj=fornecedor_cnpj,
                       quantidade=quantidade,
                       especie=especie,
                       variedade=variedade,
                       custo=custo,
                       forma_pagamento=forma_pagamento)
    
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra


def get_compra(db: Session, compra_id: int):
    return db.query(Compra).filter(Compra.id == compra_id).first()


def update_compra(db: Session, 
                  compra_id: int,
                  data: date,
                  fornecedor_cnpj: str,
                  quantidade: int,
                  especie: str ,
                  variedade: str,
                  custo: int,
                  forma_pagamento: str):
    
    db_compra = get_compra(db, compra_id)
    if db_compra:
        if data is not None:
            db_compra.data = data
        if fornecedor_cnpj is not None:
            db_compra.fornecedor_cnpj = fornecedor_cnpj
        if quantidade is not None:
            db_compra.quantidade = quantidade
        if especie is not None:
            db_compra.especie = especie
        if variedade is not None:
            db_compra.variedade = variedade
        if custo is not None:
            db_compra.custo = custo
        if forma_pagamento is not None:
            db_compra.forma_pagamento = forma_pagamento
        
        db.commit()
        db.refresh(db_compra)
    return db_compra


def delete_compra(db: Session, compra_id: int):
    db_compra = get_compra(db, compra_id)
    if db_compra:
        db.delete(db_compra)
        db.commit()
        return True
    return False
