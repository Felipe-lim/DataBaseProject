import streamlit as st
import streamlit.components.v1 as components
import os, uuid
from css import css
from crud import (
    create_pessoa, create_fornecedor, create_cliente, create_funcionario,
    get_pessoa, get_fornecedor, get_cliente, get_funcionario, get_all_pessoas,
    update_pessoa, update_fornecedor, update_cliente, update_funcionario,
    delete_pessoa, delete_fornecedor, delete_cliente, delete_funcionario
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["Start", "Manage Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def find_user_and_pessoa(db, identifier, user_type):
    user = None
    pessoa = None
    
    pessoa = get_pessoa(db, identifier)
    if pessoa:
        if user_type == "Cliente":
            user = get_cliente(db, pessoa.id)
        elif user_type == "Fornecedor":
            user = get_fornecedor(db, pessoa.id)
        elif user_type == "Funcionário":
            user = get_funcionario(db, pessoa.id)
    
    if not user:
        if user_type == "Cliente":
            user = get_cliente(db, identifier)
        elif user_type == "Fornecedor":
            user = get_fornecedor(db, identifier)
        elif user_type == "Funcionário":
            user = get_funcionario(db, identifier)
        
        if user:
            pessoa = get_pessoa(db, user.pessoa_id)
    
    return user, pessoa

def validate_input(fields):
    for field, value in fields.items():
        if not value or (isinstance(value, str) and value.strip() == ""):
            st.error(f"O campo '{field}' é obrigatório.")
            return False
    return True

if page == "Start":
    st.markdown('<h1 class="gradient-text">Bem-vindo ao CLOROFILA TECH</h1>', unsafe_allow_html=True)
    st.write("Somos um sistema de gerenciamento de ervas finas")
    st.write("Use a barra lateral para navegar")

elif page == "Manage Users":
    st.markdown('<h1 class="gradient-text">Gerenciar Usuários</h1>', unsafe_allow_html=True)

    operation = st.selectbox("Escolha sua operação", ["Create", "Read", "Update", "Delete"])
    user_type = st.radio("Escolha o tipo de usuário", ["Cliente", "Fornecedor", "Funcionário"])

    if operation == "Create":
        st.subheader("Adicionar um novo usuário")
        with st.form("create_user_form"):
            nome = st.text_input("Nome")
            endereco = st.text_input("Endereço")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
            cep = st.text_input("CEP")

            if user_type == "Cliente":
                cpf = st.text_input("CPF")
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
                "CEP": cep
            }
            if user_type == "Cliente":
                fields["CPF"] = cpf
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
                    pessoa = create_pessoa(db, user_id, nome, endereco, email, telefone, cep)
                    if user_type == "Cliente":
                        create_cliente(db, pessoa.id, cpf)
                    elif user_type == "Fornecedor":
                        create_fornecedor(db, pessoa.id, cnpj, setor)
                    elif user_type == "Funcionário":
                        create_funcionario(db, pessoa.id, cpf, cargo, genero, nascimento, naturalidade, salario)
                    st.success(f"Usuário '{nome}' criado com sucesso! ID: {user_id}")
                except Exception as e:
                    st.error(f"Erro ao criar usuário: {str(e)}")

    elif operation == "Read":
        st.subheader("Ler informações de um usuário")
        read_option = st.radio("Escolha uma opção", ["Buscar usuário específico", "Listar todas as pessoas"])
        
        if read_option == "Buscar usuário específico":
            identifier = st.text_input("Digite o UUID, CPF ou CNPJ do usuário")
            if st.button("Obter informações"):
                if validate_input({"Identificador": identifier}):
                    db = next(get_db())
                    try:
                        user, pessoa = find_user_and_pessoa(db, identifier, user_type)
                        
                        if user and pessoa:
                            data = {
                                "ID": [pessoa.id],
                                "Nome": [pessoa.nome],
                                "Endereço": [pessoa.endereco],
                                "Email": [pessoa.email],
                                "Telefone": [pessoa.telefone],
                                "CEP": [pessoa.cep],
                            }
                            for k, v in user.__dict__.items():
                                if not k.startswith('_'):
                                    data[k] = [v]
                            df = pd.DataFrame(data)
                            st.table(df)
                        else:
                            st.warning("Usuário não encontrado.")
                    except Exception as e:
                        st.error(f"Erro ao buscar usuário: {str(e)}")
        
        elif read_option == "Listar todas as pessoas":
            db = next(get_db())
            try:
                pessoas = get_all_pessoas(db)
                if pessoas:
                    data = [{
                        "ID": p.id,
                        "Nome": p.nome,
                        "Endereço": p.endereco,
                        "Email": p.email,
                        "Telefone": p.telefone,
                        "CEP": p.cep
                    } for p in pessoas]
                    df = pd.DataFrame(data)
                    st.table(df)
                else:
                    st.warning("Nenhuma pessoa encontrada.")
            except Exception as e:
                st.error(f"Erro ao listar pessoas: {str(e)}")

    elif operation == "Update":
        st.subheader("Atualizar informações de um usuário")
        identifier = st.text_input("Digite o UUID, CPF ou CNPJ do usuário")
        if st.button("Buscar usuário"):
            if validate_input({"Identificador": identifier}):
                db = next(get_db())
                try:
                    user, pessoa = find_user_and_pessoa(db, identifier, user_type)
                    
                    if user and pessoa:
                        with st.form("update_user_form"):
                            nome = st.text_input("Nome", value=pessoa.nome)
                            endereco = st.text_input("Endereço", value=pessoa.endereco)
                            email = st.text_input("Email", value=pessoa.email)
                            telefone = st.text_input("Telefone", value=pessoa.telefone)
                            cep = st.text_input("CEP", value=pessoa.cep)

                            if user_type == "Fornecedor":
                                setor = st.text_input("Setor", value=user.setor)
                            elif user_type == "Funcionário":
                                cargo = st.text_input("Cargo", value=user.cargo)
                                genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"], index=["Masculino", "Feminino", "Outro"].index(user.genero))
                                nascimento = st.date_input("Data de Nascimento", value=user.nascimento)
                                naturalidade = st.text_input("Naturalidade", value=user.naturalidade)
                                salario = st.number_input("Salário", value=user.salario, min_value=0, step=100)

                            submitted = st.form_submit_button("Atualizar")

                        if submitted:
                            fields = {
                                "Nome": nome,
                                "Endereço": endereco,
                                "Email": email,
                                "Telefone": telefone,
                                "CEP": cep
                            }
                            if user_type == "Fornecedor":
                                fields["Setor"] = setor
                            elif user_type == "Funcionário":
                                fields["Cargo"] = cargo
                                fields["Gênero"] = genero
                                fields["Data de Nascimento"] = nascimento
                                fields["Naturalidade"] = naturalidade
                                fields["Salário"] = salario

                            if validate_input(fields):
                                try:
                                    update_pessoa(db, pessoa.id, nome, endereco, email, telefone, cep)
                                    if user_type == "Fornecedor":
                                        update_fornecedor(db, pessoa.id, setor)
                                    elif user_type == "Cliente":
                                        update_cliente(db, pessoa.id, user.cpf)
                                    elif user_type == "Funcionário":
                                        update_funcionario(db, pessoa.id, cargo, genero, nascimento, naturalidade, salario)
                                    st.success("Usuário atualizado com sucesso!")
                                    
                                    updated_user, updated_pessoa = find_user_and_pessoa(db, identifier, user_type)
                                    data = {
                                        "ID": [updated_pessoa.id],
                                        "Nome": [updated_pessoa.nome],
                                        "Endereço": [updated_pessoa.endereco],
                                        "Email": [updated_pessoa.email],
                                        "Telefone": [updated_pessoa.telefone],
                                        "CEP": [updated_pessoa.cep],
                                    }
                                    for k, v in updated_user.__dict__.items():
                                        if not k.startswith('_'):
                                            data[k] = [v]
                                    df = pd.DataFrame(data)
                                    st.table(df)
                                except Exception as e:
                                    st.error(f"Erro ao atualizar usuário: {str(e)}")
                    else:
                        st.warning("Usuário não encontrado.")
                except Exception as e:
                    st.error(f"Erro ao buscar usuário: {str(e)}")

    elif operation == "Delete":
        st.subheader("Deletar um usuário")
        identifier = st.text_input("Digite o UUID, CPF ou CNPJ do usuário")
        if st.button("Apagar"):
            if validate_input({"Identificador": identifier}):
                db = next(get_db())
                try:
                    user, pessoa = find_user_and_pessoa(db, identifier, user_type)
                    
                    if user and pessoa:
                        if user_type == "Cliente":
                            delete_cliente(db, user.cpf)
                        elif user_type == "Fornecedor":
                            delete_fornecedor(db, user.cnpj)
                        elif user_type == "Funcionário":
                            delete_funcionario(db, user.cpf)
                        delete_pessoa(db, pessoa.id)
                        st.success("Usuário deletado com sucesso!")
                    else:
                        st.warning("Usuário não encontrado.")
                except Exception as e:
                    st.error(f"Erro ao deletar usuário: {str(e)}")