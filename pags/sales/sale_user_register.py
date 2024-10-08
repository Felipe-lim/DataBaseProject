import streamlit as st
from database.db import get_db
from controllers.venda import *


# Função para registrar o usuário e armazenar o estado
def user_register():
    db = next(get_db())
    st.title("Dados do usuário:")

    if 'user_confirmed' not in st.session_state:
        st.session_state['user_confirmed'] = False

    with st.form(key="form_user"):
        data = st.date_input("Data da venda", value=date.today())
        cliente = st.text_input("CPF do cliente")
        funcionario = st.text_input("CPF do funcionário")
        confirm_user_button = st.form_submit_button(label="Confirmar usuário")

    inputs = [data, funcionario, cliente]

    if confirm_user_button:
        if all(input is not None for input in inputs):
            # Armazenar os dados no session_state para uso posterior
            venda = create_venda(db, data, cliente, funcionario, 0, 0, 0, "", "Processando")
            st.session_state['user_confirmed'] = True
            st.session_state['user_data'] = {
                'id_venda': venda.id,
                'data': data,
                'cliente': cliente,
                'funcionario': funcionario
            }
            
            st.success("Usuário confirmado")
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios.")

    return st.session_state['user_confirmed']