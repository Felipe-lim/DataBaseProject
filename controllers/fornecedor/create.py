from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Fornecedor
from datetime import date

def create_fornecedor(db: Session, 
                      pessoa_id: str, 
                      cnpj: str, 
                      setor:str):
    
    db_fornecedor = Fornecedor(pessoa_id=pessoa_id, 
                               cnpj=cnpj, 
                               setor=setor)
    db.add(db_fornecedor)
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor
