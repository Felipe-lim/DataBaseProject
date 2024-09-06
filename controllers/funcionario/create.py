from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Funcionario
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
