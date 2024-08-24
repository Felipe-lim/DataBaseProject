from sqlalchemy.orm import Session
from models import Pessoa, Fornecedor, Cliente, Funcionario
from datetime import date

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# CREATE
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def create_pessoa(db: Session,
                  id:int,
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
                      pessoa_id: int, 
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
                   pessoa_id: int, 
                   cpf: str):
    
    db_cliente = Cliente(pessoa_id=pessoa_id, 
                         cpf=cpf)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def create_funcionario(db: Session, 
                       pessoa_id: int, 
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


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# READ
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def get_pessoa(db: Session, pessoa_id: int):
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

def get_fornecedor(db: Session, cnpj: str):
    return db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()

def get_cliente(db: Session, cpf: str):
    return db.query(Cliente).filter(Cliente.cpf == cpf).first()

def get_funcionario(db: Session, cpf: str):
    return db.query(Funcionario).filter(Funcionario.cpf == cpf).first()


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# UPDATE
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def update_pessoa(db: Session, 
                  pessoa_id: int,  # Corrigi o tipo do identificador
                  nome: str = None, 
                  endereco: str = None, 
                  email: str = None, 
                  telefone: str = None, 
                  cep: str = None):
    
    # Primeiro, busque a pessoa pelo ID
    db_pessoa = get_pessoa(db, pessoa_id=pessoa_id)
    
    # Verifique se a pessoa foi encontrada e atualize os campos que não são None
    if db_pessoa:
        if nome is not None:
            db_pessoa.nome = nome
        if endereco is not None:
            db_pessoa.endereco = endereco
        if email is not None:
            db_pessoa.email = email
        if telefone is not None:
            db_pessoa.telefone = telefone
        if cep is not None:
            db_pessoa.cep = cep
        
        # Commit das mudanças
        db.commit()
        db.refresh(db_pessoa)
    
    return db_pessoa

def update_fornecedor(db: Session, 
                      pessoa_id: int, 
                      cnpj: str, 
                      setor:str):
    
    db_fornecedor = get_fornecedor(db, cnpj=cnpj)
    if db_fornecedor:
        db_fornecedor.setor = setor
        db.commit()
        db.refresh(db_fornecedor)
    return db_fornecedor

def update_cliente(db: Session, 
                   pessoa_id: int, 
                   cpf: str):
    
    db_cliente = get_cliente(db, cpf=cpf)
    if db_cliente:
        db_cliente.cpf = cpf
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

def update_funcionario(db: Session, 
                       pessoa_id: int, 
                       cpf: str, 
                       cargo: str, 
                       genero: str, 
                       nascimento: date, 
                       naturalidade: str, 
                       salario: int):

    db_funcionario = get_funcionario(db, cpf=cpf)
    if db_funcionario:
        db_funcionario.cargo = cargo
        db_funcionario.genero = genero
        db_funcionario.nascimento = nascimento
        db_funcionario.naturalidade = naturalidade
        db_funcionario.salario = salario
        db.commit()
        db.refresh(db_funcionario)
    return db_funcionario


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# DELETE
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def delete_pessoa(db: Session, pessoa_id: int):
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
