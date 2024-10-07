import streamlit as st
import os, uuid
from database.db import engine, SessionLocal, get_db
from styles.css import css
from controllers.compra import *
from controllers.estoque import *
from controllers.catalogo import *


def display_compras():
    st.title("Cadastro de Produtos no Estoque")
    
    with st.form(key="form_produto"):
        data = st.date_input("Data da compra", value=date.today())
        fornecedor_cnpj = st.text_input("CNPJ do Fornecedor")
        especie = st.text_input("Espécie", max_chars=100)
        variedade = st.text_input("Variedade", max_chars=100)
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        custo = st.number_input("Custo Unitário(em real)", min_value=0, step=100)
        preco = st.number_input("Preço Revenda(em real)", min_value=0, step=100)
        forma_pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão", "Boleto", "Pix", "Berries"])

        submit_button = st.form_submit_button(label="Cadastrar Produto")
    
    inputs = [data, fornecedor_cnpj, especie, variedade, quantidade, custo, preco, forma_pagamento]

    if submit_button:
        if all(input is not None for input in inputs):
            db = next(get_db())  # Conexão com o banco de dados

            try:
                estoque = create_estoque(db, especie, variedade, quantidade, fornecedor_cnpj, custo, preco)
                st.success("Produto cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao cadastrar no estoque: {str(e)}")

            if estoque:
                try:
                    create_compra(db, data, fornecedor_cnpj, quantidade, especie, variedade, custo, forma_pagamento)
                except Exception as e:
                    st.error(f"Erro ao cadastrar compra: {str(e)}")

        else:
            st.warning("Por favor, preencha todos os campos obrigatórios.")