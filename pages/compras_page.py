import streamlit as st
from datetime import date
from sqlalchemy.orm import Session
from controllers.compra import create_compra, get_compra, update_compra, delete_compra, get_all_compras
from database import get_db  
from models import Compra

def display_compras(db: Session):
    compras = get_all_compras(db)
    st.write("## Lista de Compras")
    if compras:
        for compra in compras:
            st.write(f"ID: {compra.id}, Data: {compra.data}, Fornecedor: {compra.fornecedor_cnpj}, Quantidade: {compra.quantidade}, Espécie: {compra.especie}, Variedade: {compra.variedade}, Custo: {compra.custo}, Forma de Pagamento: {compra.forma_pagamento}")
    else:
        st.write("Nenhuma compra cadastrada.")

st.title("Gerenciamento de Compras")

option = st.selectbox("Selecione a ação", ["Ver todas as compras", "Adicionar compra", "Atualizar compra", "Deletar compra"])

# Obtenha a sessão do banco de dados consumindo o generator
db = next(get_db())  # Acessa o primeiro valor gerado pelo generator

if option == "Ver todas as compras":
    display_compras(db)

elif option == "Adicionar compra":
    st.write("## Adicionar uma nova compra")

    data = st.date_input("Data da compra", value=date.today())
    fornecedor_cnpj = st.text_input("CNPJ do Fornecedor")
    quantidade = st.number_input("Quantidade", min_value=1, value=1)
    especie = st.text_input("Espécie")
    variedade = st.text_input("Variedade")
    custo = st.number_input("Custo", min_value=0, value=0)
    forma_pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão", "Boleto", "Pix"])

    if st.button("Adicionar"):
        compra = create_compra(db, data, fornecedor_cnpj, quantidade, especie, variedade, custo, forma_pagamento)
        st.success(f"Compra adicionada com sucesso! ID da compra: {compra.id}")

elif option == "Atualizar compra":
    st.write("## Atualizar uma compra")

    compra_id = st.number_input("ID da compra", min_value=1)

    compra = get_compra(db, compra_id)
    if compra:
        st.write(f"Atualizando compra ID: {compra_id}")
        data = st.date_input("Data da compra", value=compra.data)
        fornecedor_cnpj = st.text_input("CNPJ do Fornecedor", value=compra.fornecedor_cnpj)
        quantidade = st.number_input("Quantidade", min_value=1, value=compra.quantidade)
        especie = st.text_input("Espécie", value=compra.especie)
        variedade = st.text_input("Variedade", value=compra.variedade)
        custo = st.number_input("Custo", min_value=0, value=compra.custo)
        forma_pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão", "Transferência"], index=["Dinheiro", "Cartão", "Transferência"].index(compra.forma_pagamento))

        if st.button("Atualizar"):
            updated_compra = update_compra(db, compra_id, data, fornecedor_cnpj, quantidade, especie, variedade, custo, forma_pagamento)
            st.success(f"Compra ID {updated_compra.id} atualizada com sucesso!")
    else:
        st.error("Compra não encontrada!")

elif option == "Deletar compra":
    st.write("## Deletar uma compra")

    compra_id = st.number_input("ID da compra para deletar", min_value=1)

    if st.button("Deletar"):
        success = delete_compra(db, compra_id)
        if success:
            st.success(f"Compra ID {compra_id} deletada com sucesso!")
        else:
            st.error(f"Compra ID {compra_id} não encontrada!")
