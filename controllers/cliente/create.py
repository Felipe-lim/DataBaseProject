from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Cliente
from datetime import date

def create_cliente(db: Session, 
                   pessoa_id: str, 
                   cpf: str,
                   time: str,
                   one_piece: str):
    
    db_cliente = Cliente(pessoa_id=pessoa_id, 
                         cpf=cpf,
                         time=time,
                         one_piece=one_piece)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

