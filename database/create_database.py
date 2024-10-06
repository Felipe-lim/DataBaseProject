from database.db import engine
from database.models import Base

try:
    Base.metadata.create_all(bind=engine)
    print("As tabelas foram criadas com sucesso!")
except Exception as e:
    print(f"Erro ao criar tabelas: {str(e)}")