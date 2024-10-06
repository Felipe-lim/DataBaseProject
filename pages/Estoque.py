import streamlit as st
import os, uuid
from database.db import engine, SessionLocal, get_db
from styles.css import css
from controllers.estoque import *


def show_estoque():
    st.title("Estoque Disponível: ")

    # Conectar ao banco de dados
    db = next(get_db())

    # Mostra o estoque atual
    st.subheader("Lista de Produtos no Estoque")
    estoque_list = get_all_estoque(db)

    if estoque_list:
        for item in estoque_list:
            st.write(f"**Especie:** {item.especie}")
            st.write(f"**Variedade:** {item.variedade}")
            st.write(f"**Quantidade:** {item.quantidade}")
            st.write(f"**Fornecedor:** {item.fornecedor}")
            st.write(f"**Custo:** {item.custo}")
            st.write(f"**Preço:** {item.preco}")
            st.write("---")
    else:
        st.write("Nenhum produto disponível no estoque.")


show_estoque()