from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Funcionario
from datetime import date


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


def get_funcionario(db: Session, cpf: str):
    return db.query(Funcionario).filter(Funcionario.cpf == cpf).first()


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


def delete_funcionario(db: Session, cpf: str):
    db_funcionario = get_funcionario(db, cpf)
    if db_funcionario:
        db.delete(db_funcionario)
        db.commit()
