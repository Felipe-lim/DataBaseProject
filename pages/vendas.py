import streamlit as st
from datetime import date
from sqlalchemy.orm import Session
from controllers.venda import create_venda, get_venda, update_venda, delete_venda, get_all_vendas
from database import get_db  # Função para obter a sessão do banco de dados (deve ser implementada)
from models import Venda
from controllers.cliente import *
from controllers.fornecedor import *
from controllers.funcionario import *
from models import Pessoa, Cliente, Funcionario

# Função para encontrar um Cliente pelo CPF
def find_cliente(db: Session, cpf: str):
    cliente = db.query(Cliente).filter(Cliente.cpf == cpf).first()
    if cliente:
        pessoa = db.query(Pessoa).filter(Pessoa.id == cliente.pessoa_id).first()
        return cliente, pessoa
    return None, None

def find_funcionario(db: Session, cpf: str):
    st.write(f"Buscando Funcionario com CPF: {cpf}")  # Debugging log
    funcionario = db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
    
    if funcionario:
        st.write(f"Funcionario encontrado: {funcionario}")  # Debugging log
        pessoa = db.query(Pessoa).filter(Pessoa.id == funcionario.pessoa_id).first()
        return funcionario, pessoa
    
    st.warning("Nenhum Funcionario encontrado para o CPF fornecido.")  # Log de aviso se não encontrado
    return None, None

# Função auxiliar para exibir todas as vendas na tabela
def display_vendas(db: Session):
    vendas = get_all_vendas(db)
    st.write("## Lista de Vendas")
    if vendas:
        for venda in vendas:
            st.write(f"ID: {venda.id}, Data: {venda.data}, Comprador CPF: {venda.comprador_id}, Vendedor CPF: {venda.vendedor_id}, Preço Normal: {venda.preco_normal}, Desconto: {venda.desconto}, Preço Final: {venda.preco_final}, Forma de Pagamento: {venda.forma_pagamento}, Status de Pagamento: {venda.status_pagamento}")
    else:
        st.write("Nenhuma venda cadastrada.")

st.title("Gerenciamento de Vendas")

option = st.selectbox("Selecione a ação", ["Ver todas as vendas", "Adicionar venda", "Atualizar venda", "Deletar venda"])

db = next(get_db())  # Acessa o primeiro valor gerado pelo generator

if option == "Ver todas as vendas":
    display_vendas(db)


elif option == "Adicionar venda":
    st.write("## Adicionar uma nova venda")

    data = st.date_input("Data da venda", value=date.today())
    comprador_cpf = st.text_input("CPF do Comprador")
    vendedor_cpf = st.text_input("CPF do Vendedor")
    preco_normal = st.number_input("Preço Normal", min_value=0, value=0)
    desconto = st.number_input("Desconto", min_value=0, value=0)
    preco_final = st.number_input("Preço Final", min_value=0, value=0)
    forma_pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão", "Pix"])
    status_pagamento = st.selectbox("Status de Pagamento", ["Pendente", "Pago", "Cancelado"])

    if st.button("Adicionar"):
        try:
            st.write(f"CPF do Comprador: {comprador_cpf}, CPF do Vendedor: {vendedor_cpf}")  # Debugging log
            cliente, pessoa_cliente = find_cliente(db, comprador_cpf)
            funcionario, pessoa_funcionario = find_funcionario(db, vendedor_cpf)

            if not cliente:
                st.warning("Comprador não encontrado.")
            elif not funcionario:
                st.warning("Vendedor não encontrado.")
            else:
                venda = create_venda(
                    db,
                    data,
                    cliente.pessoa_id,
                    funcionario.pessoa_id,
                    preco_normal,
                    desconto,
                    preco_final,
                    forma_pagamento,
                    status_pagamento
                )
                st.success(f"Venda adicionada com sucesso! ID da venda: {venda.id}")
        except Exception as e:
            st.error(f"Erro ao adicionar venda: {str(e)}")


elif option == "Atualizar venda":
    st.write("## Atualizar uma venda")

    venda_id = st.number_input("ID da venda", min_value=1)

    venda = get_venda(db, venda_id)
    if venda:
        st.write(f"Atualizando venda ID: {venda_id}")
        data = st.date_input("Data da venda", value=venda.data)
        comprador_cpf = st.text_input("CPF do Comprador", value=venda.comprador_id)
        vendedor_cpf = st.text_input("CPF do Vendedor", value=venda.vendedor_id)
        preco_normal = st.number_input("Preço Normal", min_value=0, value=venda.preco_normal)
        desconto = st.number_input("Desconto", min_value=0, value=venda.desconto)
        preco_final = st.number_input("Preço Final", min_value=0, value=venda.preco_final)
        forma_pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão", "Pix"], index=["Dinheiro", "Cartão", "Pix"].index(venda.forma_pagamento))
        status_pagamento = st.selectbox("Status de Pagamento", ["Pendente", "Pago", "Cancelado"], index=["Pendente", "Pago", "Cancelado"].index(venda.status_pagamento))

        if st.button("Atualizar"):
            updated_venda = update_venda(db, venda_id, data, comprador_cpf, vendedor_cpf, preco_normal, desconto, preco_final, forma_pagamento, status_pagamento)
            st.success(f"Venda ID {updated_venda.id} atualizada com sucesso!")
    else:
        st.error("Venda não encontrada!")

elif option == "Deletar venda":
    st.write("## Deletar uma venda")

    venda_id = st.number_input("ID da venda para deletar", min_value=1)

    if st.button("Deletar"):
        success = delete_venda(db, venda_id)
        if success:
            st.success(f"Venda ID {venda_id} deletada com sucesso!")
        else:
            st.error(f"Venda ID {venda_id} não encontrada!")
