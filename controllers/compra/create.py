from sqlalchemy.orm import Session
from models import Compra
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

