import streamlit as st
from database.db import get_db
from controllers.venda import *
from database.models import Estoque
import pandas as pd
from datetime import date

# Função para registrar o usuário e armazenar o estado
def user_register():
    db = next(get_db())
    st.title("Dados do usuário:")

    if 'user_confirmed' not in st.session_state:
        st.session_state['user_confirmed'] = False

    with st.form(key="form_user"):  # Alterado para chave única "form_user"
        data = st.date_input("Data da venda", value=date.today())
        cliente = st.text_input("CPF do cliente")
        funcionario = st.text_input("CPF do funcionário")
        confirm_user_button = st.form_submit_button(label="Confirmar usuário")

    inputs = [data, funcionario, cliente]

    if confirm_user_button:
        if all(input is not None for input in inputs):
            # Armazenar os dados no session_state para uso posterior
            venda = create_venda(db, data, cliente, funcionario, 0, 0, 0, "chuck Berries", "Processando")
            st.session_state['user_confirmed'] = True
            st.session_state['user_data'] = {
                'id_venda' : venda.id,
                'data': data,
                'cliente': cliente,
                'funcionario': funcionario
            }
            
            st.success("Usuário confirmado")
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios.")

    return st.session_state['user_confirmed']

# Função para buscar e selecionar produtos
def search_and_pick():
    db = next(get_db())
    st.title("Selecione os produtos:")

    if 'user_confirmed' in st.session_state and st.session_state['user_confirmed']:
        with st.form(key="form_plants"):  # Alterado para chave única "form_plants"
            especie = st.text_input("Espécie")
            variedade = st.text_input("Variedade")
            search_plant = st.form_submit_button(label="Buscar planta")

        inputs = [especie, variedade]

        if search_plant:
            if all(input is not None for input in inputs):
                result = db.query(Estoque).filter(Estoque.especie == especie, Estoque.variedade == variedade).all()
                if result:
                    st.success("Plantas encontradas")
                    result_table = [
                        {
                            "especie": item.especie,
                            "variedade": item.variedade,
                            "quantidade": item.quantidade,
                            "fornecedor": item.fornecedor,
                            "custo": item.custo,
                            "preco": item.preco
                        }
                        for item in result
                    ]
                    df = pd.DataFrame(result_table)
                    st.table(df)
                else:
                    st.error("Planta não encontrada")
            else:
                st.warning("Por favor, preencha todos os campos obrigatórios.")
    else:
        st.warning("Por favor, confirme o usuário antes de buscar produtos.")

# Função principal para exibir a venda
def display_vendas():
    user_confirmed = user_register()
    if user_confirmed:
        search_and_pick()

# Exibir a interface
display_vendas()
