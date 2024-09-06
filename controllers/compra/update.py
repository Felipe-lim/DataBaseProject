from sqlalchemy.orm import Session
from models import Compra
from datetime import date




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
