from sqlalchemy.orm import Session
from models import Venda
from datetime import date


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
