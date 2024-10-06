from utils import get_all_counts, get_db
import streamlit as st

def display_report():
   db = next(get_db())
   counts = get_all_counts(db)

   st.title("Relatório de Usuários")
   
   st.write(f"Contamos com {counts['Pessoas']} pessoas cadastradas.")
   st.write(f"{counts['Clientes']} clientes cadastrados.")
   st.write(f"{counts['Fornecedores']} fornecedores cadastrados.")
   st.write(f"{counts['Funcionários']} funcionários cadastrados.")