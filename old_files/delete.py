from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa, Fornecedor, Cliente, Funcionario
from datetime import date


def delete_pessoa(db: Session, pessoa_id: str):
    db_pessoa = get_pessoa(db, pessoa_id)
    if db_pessoa:
        db.delete(db_pessoa)
        db.commit()

def delete_fornecedor(db: Session, cnpj: str):
    db_fornecedor = get_fornecedor(db, cnpj)
    if db_fornecedor:
        db.delete(db_fornecedor)
        db.commit()

def delete_cliente(db: Session, cpf: str):
    db_cliente = get_cliente(db, cpf)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()

def delete_funcionario(db: Session, cpf: str):
    db_funcionario = get_funcionario(db, cpf)
    if db_funcionario:
        db.delete(db_funcionario)
        db.commit()
