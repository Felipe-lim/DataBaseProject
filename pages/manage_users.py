import streamlit as st
import pandas as pd
import uuid, os
from database import get_db
from controllers.cliente import *
from controllers.fornecedor import *
from controllers.funcionario import *
from controllers.general import *
from controllers.pessoas import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def find_user_and_pessoa(db, identifier, user_type):
    user = None
    pessoa = None

    # Tentativa de buscar o usuário por CPF ou CNPJ diretamente na tabela correspondente
    if user_type == "Cliente":
        user = get_cliente(db, identifier)
    elif user_type == "Fornecedor":
        user = get_fornecedor(db, identifier)
    elif user_type == "Funcionário":
        user = get_funcionario(db, identifier)

    # Se o usuário foi encontrado, buscar a pessoa correspondente pelo ID
    if user:
        pessoa = get_pessoa(db, user.pessoa_id)
    else:
        st.warning(f"Usuário com identificador '{identifier}' não encontrado.")

    return user, pessoa

def validate_input(fields):
    for field, value in fields.items():
        if not value or (isinstance(value, str) and value.strip() == ""):
            st.error(f"O campo '{field}' é obrigatório.")
            return False
    return True

def delete_user(db, pessoa_id, user_type):
    try:
        st.write(f"Deletando usuário do tipo: {user_type} com pessoa_id: {pessoa_id}")
        
        if user_type == "Cliente":
            cliente = db.query(Cliente).filter(Cliente.pessoa_id == pessoa_id).first()
            if cliente:
                st.write(f"Cliente encontrado: {cliente}")
                db.query(Cliente).filter(Cliente.pessoa_id == pessoa_id).delete()
                db.commit()  # Comitar a deleção aqui
                st.write("Cliente deletado com sucesso!")
            else:
                st.warning("Cliente não encontrado para deleção!")
        
        elif user_type == "Fornecedor":
            fornecedor = db.query(Fornecedor).filter(Fornecedor.pessoa_id == pessoa_id).first()
            if fornecedor:
                st.write(f"Fornecedor encontrado: {fornecedor}")
                db.query(Fornecedor).filter(Fornecedor.pessoa_id == pessoa_id).delete()
                db.commit()  # Comitar a deleção aqui
                st.write("Fornecedor deletado com sucesso!")
            else:
                st.warning("Fornecedor não encontrado para deleção!")
        
        elif user_type == "Funcionário":
            funcionario = db.query(Funcionario).filter(Funcionario.pessoa_id == pessoa_id).first()
            if funcionario:
                st.write(f"Funcionário encontrado: {funcionario}")
                db.query(Funcionario).filter(Funcionario.pessoa_id == pessoa_id).delete()
                db.commit()  # Comitar a deleção aqui
                st.write("Funcionário deletado com sucesso!")
            else:
                st.warning("Funcionário não encontrado para deleção!")
        
        # Deletando a pessoa após deletar o usuário relacionado
        pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
        if pessoa:
            st.write(f"Pessoa encontrada para deleção: {pessoa}")
            db.query(Pessoa).filter(Pessoa.id == pessoa_id).delete()
            db.commit()  # Comitar a deleção da pessoa
            return True, "Usuário deletado com sucesso!"
        else:
            st.warning("Pessoa não encontrada após deletar o usuário relacionado.")
            return False, "Erro: Pessoa não encontrada."
    
    except Exception as e:
        db.rollback()
        return False, f"Erro ao deletar usuário: {str(e)}"


def buscar_valor(opcoes, valor):
    try:
        return opcoes.index(valor)
    except ValueError:
        return 0

page = "Manage Users"
if page == "Manage Users":
    st.markdown('<h1 class="gradient-text">Gerenciar Usuários</h1>', unsafe_allow_html=True)

    user_type = st.sidebar.radio("Escolha o tipo de usuário", ["Cliente", "Fornecedor", "Funcionário"])
    operation = st.sidebar.selectbox("Escolha sua operação", ["Create", "Read", "Update", "Delete"])

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
                    pessoa = create_pessoa(db, user_id, nome, endereco, email, telefone, cep)
                    if user_type == "Cliente":
                        create_cliente(db, pessoa.id, cpf, time, one_piece)
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
            identifier = st.text_input("Digite o CPF ou CNPJ do usuário")
            if st.button("Obter informações"):
                if validate_input({"Identificador": identifier}):
                    db = next(get_db())
                    try:
                        user, pessoa = find_user_and_pessoa(db, identifier, user_type)
                        if user and pessoa:
                            data = {
                                "ID": str(pessoa.id),
                                "Nome": pessoa.nome,
                                "Endereço": pessoa.endereco,
                                "Email": pessoa.email,
                                "Telefone": pessoa.telefone,
                                "CEP": pessoa.cep,
                            }
                            for k, v in user.__dict__.items():
                                if not k.startswith("_"):
                                    data[k] = str(v)
                            st.write("Informações do usuário:")
                            st.write(data)
                        else:
                            st.warning("Usuário não encontrado.")
                    except Exception as e:
                        st.error(f"Erro ao buscar usuário: {str(e)}")

        elif read_option == "Listar todas as pessoas":
            db = next(get_db())
            try:
                pessoas = get_all_pessoas(db)
                if pessoas:
                    data = [
                        {
                            "ID": str(p.id),
                            "Nome": p.nome,
                            "Endereço": p.endereco,
                            "Email": p.email,
                            "Telefone": p.telefone,
                            "CEP": p.cep,
                        }
                        for p in pessoas
                    ]
                    df = pd.DataFrame(data)
                    df = df.astype(str)
                    st.table(df)
                else:
                    st.warning("Nenhuma pessoa encontrada.")
            except Exception as e:
                st.error(f"Erro ao listar pessoas: {str(e)}")

    elif operation == "Update":
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
                    cpf_atual = st.text_input("CPF Atual", value=user.cpf, disabled=True)
                    cpf_novo = st.text_input("CPF Novo", value=user.cpf)
                    time = st.text_input("Time", value=user.time)
                    one_piece = st.selectbox("One Piece:", ['', 'Assiste', 'Não assiste'], index=buscar_valor(['', 'Assiste', 'Não assiste'], user.one_piece))
                elif user_type == "Fornecedor":
                    cnpj_atual = st.text_input("CNPJ Atual", value=user.cnpj, disabled=True)
                    cnpj_novo = st.text_input("CNPJ Novo", value=user.cnpj)
                    setor = st.text_input("Setor", value=user.setor)
                elif user_type == "Funcionário":
                    cpf_atual = st.text_input("CPF Atual", value=user.cpf, disabled=True)
                    cpf_novo = st.text_input("CPF Novo", value=user.cpf)
                    cargo = st.text_input("Cargo", value=user.cargo)
                    genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"], index=["Masculino", "Feminino", "Outro"].index(user.genero))
                    nascimento = st.date_input("Data de Nascimento", value=user.nascimento)
                    naturalidade = st.text_input("Naturalidade", value=user.naturalidade)
                    salario = st.number_input("Salário", value=user.salario, min_value=0, step=100)

                submit_button = st.form_submit_button(label="Atualizar")

            if submit_button:
                fields = {
                    "Nome": nome,
                    "Endereço": endereco,
                    "Email": email,
                    "Telefone": telefone,
                    "CEP": cep,
                }
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

                if validate_input(fields):
                    try:
                        # Atualiza as informações
                        update_pessoa(db, pessoa.id, nome, endereco, email, telefone, cep)

                        if user_type == "Cliente":
                            update_cliente(db, user.id, cpf_novo, time, one_piece)
                        elif user_type == "Fornecedor":
                            update_fornecedor(db, user.id, cnpj_novo, setor)
                        elif user_type == "Funcionário":
                            update_funcionario(db, user.id, cpf_novo, cargo, genero, nascimento, naturalidade, salario)
                            
                        st.success("Usuário atualizado com sucesso!")
                        del st.session_state["user"]
                        del st.session_state["pessoa"]
                    except Exception as e:
                        st.error(f"Erro ao atualizar usuário: {str(e)}")

    elif operation == "Delete":
        st.subheader("Deletar um usuário")
        identifier = st.text_input("Digite o CPF ou CNPJ do usuário")

        if st.button("Buscar Usuário"):
            if validate_input({"Identificador": identifier}):
                db = next(get_db())
                try:
                    # Buscar o usuário e a pessoa relacionada
                    user, pessoa = find_user_and_pessoa(db, identifier, user_type)

                    if user and pessoa:
                        st.write("Usuário encontrado:")
                        data = {
                            "ID": str(pessoa.id),
                            "Nome": pessoa.nome,
                            "Endereço": pessoa.endereco,
                            "Email": pessoa.email,
                            "Telefone": pessoa.telefone,
                            "CEP": pessoa.cep,
                        }
                        st.write(data)

                        # Armazenar user e pessoa no st.session_state
                        st.session_state['user_to_delete'] = user
                        st.session_state['pessoa_to_delete'] = pessoa

                    else:
                        st.warning("Usuário não encontrado.")
                except Exception as e:
                    st.error(f"Erro ao buscar usuário: {str(e)}")

        # Verificar se user e pessoa estão no session_state
        if 'user_to_delete' in st.session_state and 'pessoa_to_delete' in st.session_state:
            if st.button("Confirmar Deleção"):
                db = next(get_db())
                user = st.session_state['user_to_delete']
                pessoa = st.session_state['pessoa_to_delete']
                success, message = delete_user(db, pessoa.id, user_type)
                if success:
                    st.success(message)
                    # Remover user e pessoa do session_state após a deleção
                    del st.session_state['user_to_delete']
                    del st.session_state['pessoa_to_delete']
                else:
                    st.error(message)
