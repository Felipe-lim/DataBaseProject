from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from models import Base
from db import engine

def drop_all_tables(engine):
    try:
        # Instancia o MetaData e conecta ao banco de dados para apagar todas as tabelas
        Base.metadata.drop_all(bind=engine)
        print("Todas as tabelas foram apagadas com sucesso.")
    except Exception as e:
        print(f"Erro ao apagar tabelas: {str(e)}")

drop_all_tables(engine)