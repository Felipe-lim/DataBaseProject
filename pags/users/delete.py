import streamlit as st
from utils import get_db, validate_input, find_user_and_pessoa
from controllers.cliente import delete_cliente
from controllers.fornecedor import delete_fornecedor
from controllers.funcionario import delete_funcionario
from controllers.pessoas import delete_pessoa

def display_delete(user_type):
   st.subheader("Deletar um usuário")
   identifier = st.text_input("Digite o CPF ou CNPJ do usuário")
   if st.button("Deletar"):
      if validate_input({"Identificador": identifier}):
            db = next(get_db())
            try:
               user, pessoa = find_user_and_pessoa(db, identifier, user_type)

               if user and pessoa:
                  delete_pessoa(db, pessoa.id)
                  if user_type == "Cliente":
                        delete_cliente(db, user.cpf)
                  elif user_type == "Fornecedor":
                        delete_fornecedor(db, user.cnpj)
                  elif user_type == "Funcionário":
                        delete_funcionario(db, user.cpf)
                  st.success(f"Usuário '{pessoa.nome}' deletado com sucesso!")
               else:
                  st.warning("Usuário não encontrado.")
            except Exception as e:
               st.error(f"Erro ao deletar usuário: {str(e)}")