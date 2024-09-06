from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa, Fornecedor, Cliente, Funcionario
from datetime import date

def create_pessoa(db: Session,
                  id:str,
                  nome: str, 
                  endereco: str, 
                  email: str, 
                  telefone: str, 
                  cep: str):
    
    db_pessoa = Pessoa(id=id,
                       nome=nome, 
                       endereco=endereco, 
                       email=email, 
                       telefone=telefone, 
                       cep=cep, )
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

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

def create_cliente(db: Session, 
                   pessoa_id: str, 
                   cpf: str,
                   time: str,
                   one_piece: bool):
    
    db_cliente = Cliente(pessoa_id=pessoa_id, 
                         cpf=cpf,
                         time=time,
                         one_piece=one_piece)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def create_funcionario(db: Session, 
                       pessoa_id: str, 
                       cpf:str, 
                       cargo: str, 
                       genero:str, 
                       nascimento:date, 
                       naturalidade:str, 
                       salario: int):
    
    db_funcionario = Funcionario(pessoa_id=pessoa_id, 
                                 cpf=cpf, cargo=cargo, 
                                 genero=genero, 
                                 nascimento=nascimento, 
                                 naturalidade=naturalidade,
                                 salario=salario)
    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario
