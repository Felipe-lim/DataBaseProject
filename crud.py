from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa, Fornecedor, Cliente, Funcionario
from datetime import date

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# CREATE
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

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
                   cpf: str):
    
    db_cliente = Cliente(pessoa_id=pessoa_id, 
                         cpf=cpf)
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


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# READ
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def get_pessoa(db: Session, pessoa_id: str):
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

def get_fornecedor(db: Session, cnpj: str):
    return db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()

def get_cliente(db: Session, cpf: str):
    return db.query(Cliente).filter(Cliente.cpf == cpf).first()

def get_funcionario(db: Session, cpf: str):
    return db.query(Funcionario).filter(Funcionario.cpf == cpf).first()

# Fazer função para pegar todas as informações de todos os usuários
def get_all_pessoas(db: Session):
    return db.query(Pessoa).all()

def get_all_counts(db: Session):
	pessoa_count = db.query(func.count(Pessoa.id)).scalar()
	cliente_count = db.query(func.count(Cliente.pessoa_id)).scalar()
	fornecedor_count = db.query(func.count(Fornecedor.pessoa_id)).scalar()
	funcionario_count = db.query(func.count(Funcionario.pessoa_id)).scalar()
	
	return {
		"Pessoas": pessoa_count,
		"Clientes": cliente_count,
		"Fornecedores": fornecedor_count,
		"Funcionários": funcionario_count
	}
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# UPDATE
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def update_pessoa(db: Session, 
                  pessoa_id: str = None,
                  nome: str = None, 
                  endereco: str = None, 
                  email: str = None, 
                  telefone: str = None, 
                  cep: str = None):
    
    db_pessoa = get_pessoa(db, pessoa_id=pessoa_id)
    
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
        
        db.commit()
        db.refresh(db_pessoa)
    
    return db_pessoa

def update_fornecedor(db: Session, 
                      pessoa_id: str, 
                      cnpj: str = None, 
                      setor: str = None):
    
    db_fornecedor = get_fornecedor(db, cnpj=cnpj)
    if db_fornecedor:
        if cnpj is not None:
            db_fornecedor.cnpj = cnpj
        if setor is not None:
            db_fornecedor.setor = setor
        db.commit()
        db.refresh(db_fornecedor)
    return db_fornecedor

def update_cliente(db: Session, 
                   cpf: str = None):
    
    db_cliente = get_cliente(db, cpf)
    if db_cliente and cpf is not None:
        db_cliente.cpf = cpf
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

def update_funcionario(db: Session, 
                       pessoa_id: str, 
                       cpf: str = None, 
                       cargo: str = None, 
                       genero: str = None, 
                       nascimento: date = None, 
                       naturalidade: str = None, 
                       salario: int = None):

    db_funcionario = get_funcionario(db, cpf=cpf)
    if db_funcionario:
        if cpf is not None:
            db_funcionario.cpf = cpf
        if cargo is not None:
            db_funcionario.cargo = cargo
        if genero is not None:
            db_funcionario.genero = genero
        if nascimento is not None:
            db_funcionario.nascimento = nascimento
        if naturalidade is not None:
            db_funcionario.naturalidade = naturalidade
        if salario is not None:
            db_funcionario.salario = salario
        db.commit()
        db.refresh(db_funcionario)
    return db_funcionario

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# DELETE
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

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
