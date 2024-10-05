from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from database.models import Base

def drop_all_tables(db: Session):
    try:
        # Instancia o MetaData e conecta ao banco de dados
        meta = Base.metadata
        
        # Executa o drop de todas as tabelas associadas ao MetaData
        meta.drop_all(bind=db.bind)
        
        print("Todas as tabelas foram apagadas com sucesso.")
    except Exception as e:
        print(f"Erro ao apagar tabelas: {str(e)}")
