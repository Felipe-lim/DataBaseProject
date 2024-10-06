import streamlit as st
from utils import get_db, validate_input
import uuid
from controllers.cliente import *
from controllers.fornecedor import *
from controllers.funcionario import *
from controllers.general import *
from controllers.pessoas import *

def display_create(user_type):
   st.subheader("Adicionar um novo usuário")
   with st.form("create_user_form"):
      nome = st.text_input("Nome")
      endereco = st.text_input("Endereço")
      email = st.text_input("Email")
      telefone = st.text_input("Telefone")
      cep = st.text_input("CEP")

      if user_type == "Cliente":
            cpf = st.text_input("CPF")
            time = st.text_input("Time")
            one_piece = st.selectbox('One Piece:', ['', 'Assiste', 'Não assiste'])
      elif user_type == "Fornecedor":
            cnpj = st.text_input("CNPJ")
            setor = st.text_input("Setor")
      elif user_type == "Funcionário":
            cpf = st.text_input("CPF")
            cargo = st.text_input("Cargo")
            genero = st.selectbox("Gênero", ["", "Masculino", "Feminino", "Outro"])
            nascimento = st.date_input("Data de Nascimento")
            naturalidade = st.text_input("Naturalidade")
            salario = st.number_input("Salário", min_value=0, step=100)

      submitted = st.form_submit_button("Criar")

   if submitted:
      fields = {
            "Nome": nome,
            "Endereço": endereco,
            "Email": email,
            "Telefone": telefone,
            "CEP": cep,
      }
      if user_type == "Cliente":
            fields["CPF"] = cpf
            fields["Time"] = time
            fields["One Piece"] = one_piece
      elif user_type == "Fornecedor":
            fields["CNPJ"] = cnpj
            fields["Setor"] = setor
      elif user_type == "Funcionário":
            fields["CPF"] = cpf
            fields["Cargo"] = cargo
            fields["Gênero"] = genero
            fields["Data de Nascimento"] = nascimento
            fields["Naturalidade"] = naturalidade
            fields["Salário"] = salario

      if validate_input(fields):
            db = next(get_db())
            try:
               user_id = str(uuid.uuid4())
               pessoa = create_pessoa(
                  db, user_id, nome, endereco, email, telefone, cep
               )
               if user_type == "Cliente":
                  create_cliente(db, pessoa.id, cpf, time, one_piece)
               elif user_type == "Fornecedor":
                  create_fornecedor(db, pessoa.id, cnpj, setor)
               elif user_type == "Funcionário":
                  create_funcionario(
                        db,
                        pessoa.id,
                        cpf,
                        cargo,
                        genero,
                        nascimento,
                        naturalidade,
                        salario,
                  )
               st.success(f"Usuário '{nome}' criado com sucesso! ID: {user_id}")
            except Exception as e:
               st.error(f"Erro ao criar usuário: {str(e)}")