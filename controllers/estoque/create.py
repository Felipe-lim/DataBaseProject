from sqlalchemy.orm import Session
from models import Estoque
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
