import streamlit as st
from pags.Manage.create import display_create
from pags.Manage.read import display_read
from pags.Manage.update import display_update
from pags.Manage.delete import display_delete
from controllers.cliente import *
from controllers.fornecedor import *
from controllers.funcionario import *
from controllers.general import *
from controllers.pessoas import *

def display_manager():
   st.markdown(
      '<h1 class="gradient-text">Gerenciar Usuários</h1>', unsafe_allow_html=True
   )

   operation = st.selectbox(
      "Escolha sua operação", ["Create", "Read", "Update", "Delete"]
   )
   user_type = st.radio(
      "Escolha o tipo de usuário", ["Cliente", "Fornecedor", "Funcionário"]
   )

   match operation:
      case "Create":
         display_create(user_type)
      case "Read":
         display_read(user_type)
      case "Update":
         display_update(user_type)
      case "Delete":
         display_delete(user_type)

