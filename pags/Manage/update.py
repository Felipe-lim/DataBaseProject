import streamlit as st
from utils import get_db,find_user_and_pessoa, buscar_valor, validate_input
from controllers.cliente import *
from controllers.fornecedor import *
from controllers.funcionario import *
from controllers.general import *
from controllers.pessoas import *

def display_update(user_type):
   st.subheader("Atualizar informações de um usuário")
   
   identifier = st.text_input("CPF ou CNPJ do usuário")
   
   user_found = False
   db = next(get_db())
   if st.button("Buscar usuário"):
      if validate_input({"Identificador": identifier}):
            try:
               user, pessoa = find_user_and_pessoa(db, identifier, user_type)
               
               if user and pessoa:
                  user_found = True
                  st.success("Usuário encontrado! Preencha os campos abaixo para atualizar.")
                  
                  st.session_state["user"] = user
                  st.session_state["pessoa"] = pessoa
               else:
                  st.warning("Usuário não encontrado.")
            except Exception as e:
               st.error(f"Erro ao buscar usuário: {str(e)}")

   if "user" in st.session_state and "pessoa" in st.session_state:
      user = st.session_state["user"]
      pessoa = st.session_state["pessoa"]

      with st.form(key="update_form"):
            nome = st.text_input("Nome", value=pessoa.nome)
            endereco = st.text_input("Endereço", value=pessoa.endereco)
            email = st.text_input("Email", value=pessoa.email)
            telefone = st.text_input("Telefone", value=pessoa.telefone)
            cep = st.text_input("CEP", value=pessoa.cep)

            if user_type == "Cliente":
               try:
                  cpf_atual = st.text_input("CPF Atual", value=user.cpf, disabled=True)
                  cpf_novo = st.text_input("CPF Novo", value=user.cpf)
                  time = st.text_input("Time", value=user.time)
                  one_piece = st.selectbox("One Piece:", ['','Assiste', 'Não assiste'], index=buscar_valor(['','Assiste', 'Não assiste'], user.one_piece))
               except:
                     pass
            elif user_type == "Fornecedor":
               try:
                  cnpj_atual = st.text_input("CNPJ Atual", value=user.cnpj,disabled=True)
                  cnpj_novo = st.text_input("CNPJ Novo", value=user.cnpj)
                  setor = st.text_input("Setor", value=user.setor)
               except:  
                     pass
            elif user_type == "Funcionário":
               try:
                  cpf_atual = st.text_input("CPF Atual", value=user.cpf, disabled=True)
                  cpf_novo = st.text_input("CPF Novo", value=user.cpf)
                  cargo = st.text_input("Cargo", value=user.cargo)
                  genero = st.selectbox(
                     "Gênero", ["Masculino", "Feminino", "Outro"],
                     index=["Masculino", "Feminino", "Outro"].index(user.genero)
                  )
                  nascimento = st.date_input(
                     "Data de Nascimento", value=user.nascimento
                  )
                  naturalidade = st.text_input(
                     "Naturalidade", value=user.naturalidade
                  )
                  salario = st.number_input(
                     "Salário", value=user.salario, min_value=0, step=100
                  )
               except:
                  pass
            submit_button = st.form_submit_button(label="Atualizar")

      if submit_button:
            fields = {
               "Nome": nome,
               "Endereço": endereco,
               "Email": email,
               "Telefone": telefone,
               "CEP": cep,
            }
            try:
               if user_type == "Cliente":
                  fields["CPF Atual"] = cpf_atual
                  fields["CPF Novo"] = cpf_novo
                  fields["Time"] = time
                  fields["One Piece"] = one_piece
               elif user_type == "Fornecedor":
                  fields["CNPJ Atual"] = cnpj_atual
                  fields["CNPJ Novo"] = cnpj_novo
                  fields["Setor"] = setor
               elif user_type == "Funcionário":
                  fields["CPF Atual"] = cpf_atual
                  fields["CPF Novo"] = cpf_novo
                  fields["Cargo"] = cargo
                  fields["Gênero"] = genero
                  fields["Data de Nascimento"] = nascimento
                  fields["Naturalidade"] = naturalidade
                  fields["Salário"] = salario
            except:
                  pass
            if validate_input(fields):
               try:
                  update_pessoa(db, pessoa.id, nome, endereco, email, telefone, cep)
                  
                  if user_type == "Cliente":
                        update_cliente(db,cpf_atual, cpf_novo, time, one_piece)
                  elif user_type == "Fornecedor":
                        update_fornecedor(db, cnpj_atual, cnpj_novo , setor)
                  elif user_type == "Funcionário":
                        update_funcionario(db, user.pessoa_id, cpf_atual,cpf_novo, cargo, genero, nascimento, naturalidade, salario)
                  
                  st.success(f"Usuário '{nome}' atualizado com sucesso!")
               except Exception as e:
                  st.error(f"Erro ao atualizar usuário: {str(e)}")
            else:
               st.warning("Por favor, preencha todos os campos corretamente.") 