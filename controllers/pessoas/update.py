from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa
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
