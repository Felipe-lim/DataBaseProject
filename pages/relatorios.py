import streamlit as st
from controllers.general import get_all_counts
from database.db import get_db

def page_relatorios():
    db = next(get_db())
    
    counts = get_all_counts(db)

    st.title("Relatório de Usuários")
    
    st.write(f"Contamos com **{counts['Pessoas']}** pessoas cadastradas.")
    st.write(f"**{counts['Clientes']}** clientes cadastrados.")
    st.write(f"**{counts['Fornecedores']}** fornecedores cadastrados.")
    st.write(f"**{counts['Funcionários']}** funcionários cadastrados.")


page_relatorios()