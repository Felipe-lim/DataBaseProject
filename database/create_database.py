from database.db import engine
from database.models import Base

try:
    Base.metadata.create_all(bind=engine)
    print("As tabelas foram criadas com sucesso!")
except:
    print("Error: As tabelas não foram criadas.")