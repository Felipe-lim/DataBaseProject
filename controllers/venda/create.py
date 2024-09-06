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
