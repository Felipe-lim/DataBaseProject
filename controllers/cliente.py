from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Cliente
from datetime import date
import streamlit as st
from sqlalchemy.orm import joinedload

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


def get_cliente(db: Session, cpf: str):
    cpf_formatado = cpf.replace('.', '').replace('-', '')  # Remover a formatação do CPF
    st.write(f"Buscando Cliente com CPF: {cpf_formatado}")  # Log para verificação

    # Usar joinedload para carregar a relação 'pessoa' juntamente com o cliente
    cliente = db.query(Cliente).options(joinedload(Cliente.pessoa)).filter(Cliente.cpf == cpf_formatado).first()

    if cliente:
        st.write(f"Cliente encontrado: {cliente.pessoa.nome}")  # Log para verificar se encontrou o cliente
        return cliente
    else:
        st.error(f"CPF {cpf_formatado} não encontrado no banco de dados.")  # Mensagem de erro se não encontrado
        return None

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

def delete_cliente(db: Session, cpf: str):
    db_cliente = get_cliente(db, cpf)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
