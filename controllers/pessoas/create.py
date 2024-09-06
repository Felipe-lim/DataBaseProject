from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa
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
