from database.db import engine, Base

def drop_all_tables(engine):
    try:
        # Certifica-se de que a conexão com o banco está ativa
        with engine.connect() as connection:
            # Instancia o MetaData e conecta ao banco de dados para apagar todas as tabelas
            Base.metadata.drop_all(bind=engine)
            print("Todas as tabelas foram apagadas com sucesso.")
    except Exception as e:
        print(f"Erro ao apagar tabelas: {str(e)}")

# Chama a função para apagar todas as tabelas
drop_all_tables(engine)
