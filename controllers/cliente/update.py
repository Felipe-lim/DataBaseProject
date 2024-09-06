from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Cliente
from datetime import date

def update_cliente(db: Session, 
                   cpf_atual: str,
                   cpf_novo: str,
                   time: str,
                   one_piece: str):
    
    db_cliente = get_cliente(db, cpf_atual)
    if db_cliente:
        if cpf_novo is not None:
            db_cliente.cpf = cpf_novo
        if time is not None:
            db_cliente.time = time
        if one_piece is not None:
            db_cliente.one_piece = one_piece
        db.commit()
        db.refresh(db_cliente)
    return db_cliente
