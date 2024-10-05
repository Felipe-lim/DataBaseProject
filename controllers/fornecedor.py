from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Fornecedor
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


def get_fornecedor(db: Session, cnpj: str):
    return db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()


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


def delete_fornecedor(db: Session, cnpj: str):
    db_fornecedor = get_fornecedor(db, cnpj)
    if db_fornecedor:
        db.delete(db_fornecedor)
        db.commit()
