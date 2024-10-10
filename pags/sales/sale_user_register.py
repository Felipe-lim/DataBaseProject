import streamlit as st
from database.db import get_db
from controllers.venda import *
from validate import validar_venda


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

   fields = {
      "data": data,
      "cliente": cliente,
      "funcionario": funcionario
   }

   status, errors = validar_venda(fields)
   if confirm_user_button:
      if status:
         try:
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
            return st.session_state['user_confirmed']

         except:
            st.error(f"Por favor, preencha todos os campos obrigatórios.")
      else:
         for campo, erro in errors.items():
            st.error(erro)
