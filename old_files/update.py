from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa, Fornecedor, Cliente, Funcionario
from datetime import date




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

def update_cliente(db: Session, 
                   cpf: str,
                   time: str,
                   one_piece: bool):
    
    db_cliente = get_cliente(db, cpf)
    if db_cliente and cpf is not None:
        db_cliente.cpf = cpf
        db_cliente.time = time,
        db_cliente = one_piece,
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

def update_funcionario(db: Session, 
                       pessoa_id: str, 
                       cpf_atual: str = None,
                       cpf_novo: str = None, 
                       cargo: str = None, 
                       genero: str = None, 
                       nascimento: date = None, 
                       naturalidade: str = None, 
                       salario: int = None):

    db_funcionario = get_funcionario(db, cpf=cpf_atual)
    if db_funcionario:
        if cpf_novo is not None:
            db_funcionario.cpf = cpf_novo
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
