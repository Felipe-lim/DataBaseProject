from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Fornecedor
from datetime import date

def update_fornecedor(db: Session,  
                      cnpj_atual: str = None,
                      cnpj_novo: str = None, 
                      setor: str = None):
    
    db_fornecedor = get_fornecedor(db, cnpj=cnpj_atual)
    if db_fornecedor:
        if cnpj_novo is not None:
            db_fornecedor.cnpj = cnpj_novo
        if setor is not None:
            db_fornecedor.setor = setor
        db.commit()
        db.refresh(db_fornecedor)
    return db_fornecedor

