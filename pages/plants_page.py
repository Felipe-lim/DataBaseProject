import streamlit as st
from sqlalchemy.orm import Session
from controllers.estoque import get_all_estoque  
from database.db import SessionLocal  

 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def plants_page():
    st.title("Plantas Cadastradas")
    st.write("Aqui estão todas as plantas cadastradas no sistema:")

    db = next(get_db())

    plantas = get_all_estoque(db)  

    if not plantas:
        st.write("Nenhuma planta cadastrada.")
    else:
        for planta in plantas:
            st.subheader(f"{planta.especie} ({planta.variedade})")
            st.write(f"**Quantidade**: {planta.quantidade}")
            st.write(f"**Fornecedor**: {planta.fornecedor}")
            st.write(f"**Custo**: R$ {planta.custo}")
            st.write(f"**Preço de Venda**: R$ {planta.preco}")
            st.write("---")

plants_page()