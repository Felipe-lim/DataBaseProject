from sqlalchemy.orm import Session
from models import Venda
from datetime import date
from controllers.pessoas import get_pessoa 
import streamlit as st
from models import Cliente, Funcionario

# Função para obter o cliente pelo CPF
def get_cliente(db: Session, cpf: str):
    cpf_formatado = cpf.replace('.', '').replace('-', '')  # Remover a formatação do CPF
    st.write(f"Buscando Cliente com CPF: {cpf_formatado}")  # Log para verificação

    cliente = db.query(Cliente).filter(Cliente.cpf == cpf_formatado).first()

    if cliente:
        st.write(f"Cliente encontrado: {cliente.pessoa.nome}")  # Log para verificar se encontrou o cliente
        return cliente
    else:
        st.error(f"CPF {cpf_formatado} não encontrado no banco de dados.")  # Mensagem de erro se não encontrado
        return None


# Função para obter o funcionário pelo CPF
def get_funcionario(db: Session, cpf: str):
    cpf_formatado2 = cpf.replace('.', '').replace('-', '')  # Remover a formatação do CPF
    st.write(f"Buscando vendedor com CPF: {cpf_formatado2}")  # Adicione esta linha para verificar o CPF

    funcionario = db.query(Funcionario).filter(Funcionario.cpf == cpf_formatado2).first()

    if funcionario:
        st.write(f"Vendedor encontrado: {funcionario.pessoa.nome}")  # Adicione esta linha para verificar se encontrou
        return funcionario
    else:
        st.error(f"CPF {cpf_formatado2} não encontrado no banco de dados.")  # Verificação adicional para CPF não encontrado
        return None



def get_venda(db: Session, venda_id: int):
    return db.query(Venda).filter(Venda.id == venda_id).first()

def get_all_vendas(db: Session):
    return db.query(Venda).all()

def delete_venda(db: Session, venda_id: int):
    db_venda = get_venda(db, venda_id)
    if db_venda:
        db.delete(db_venda)
        db.commit()
        return True
    return False

def calculate_discount(endereco, time, one_piece):
    discount = 0
    if endereco.lower() == "sousa":
        discount += 5
    if time.lower() == "flamengo":
        discount += 5
    if one_piece:
        discount += 5
    return discount
def create_venda(db: Session, 
                 data: date,
                 comprador_id: str,
                 vendedor_id: str,
                 preco_normal: int,
                 desconto: int,
                 preco_final: int,
                 forma_pagamento: str,
                 status_pagamento: str):
    
    # Buscar as informações do comprador no banco de dados
    comprador = get_cliente(db, comprador_id)
    if not comprador:
        raise Exception("Comprador não encontrado no banco de dados")

    # Extrair as informações relevantes para o cálculo do desconto
    endereco = comprador.pessoa.endereco  # Acessando o endereço através de 'pessoa'
    time = comprador.time  # Acessando o campo "time" diretamente no cliente
    one_piece = comprador.one_piece  # Supondo que você tenha um campo booleano "one_piece" na tabela Cliente

    # Calcula o desconto adicional com base nas informações do banco de dados
    desconto += calculate_discount(endereco, time, one_piece)
    
    # Recalcula o preço final
    preco_final = preco_normal - (preco_normal * (desconto / 100))
    
    # Cria a venda no banco de dados
    db_venda = Venda(data=data,
                     comprador_id=comprador_id,
                     vendedor_id=vendedor_id,
                     preco_normal=preco_normal,
                     desconto=desconto,
                     preco_final=preco_final,
                     forma_pagamento=forma_pagamento,
                     status_pagamento=status_pagamento)
    
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda

def update_venda(db: Session, 
                 venda_id: int,
                 data: date = None,
                 comprador_id: str = None,
                 vendedor_id: str = None,
                 preco_normal: int = None,
                 desconto: int = None,
                 preco_final: int = None,
                 forma_pagamento: str = None,
                 status_pagamento: str = None):
    
    db_venda = get_venda(db, venda_id)
    if not db_venda:
        raise Exception("Venda não encontrada no banco de dados")

    # Buscar as informações do comprador no banco de dados
    comprador = get_cliente(db, comprador_id)
    if not comprador:
        raise Exception("Comprador não encontrado no banco de dados")

    # Extrair as informações relevantes para o cálculo do desconto
    endereco = comprador.pessoa.endereco  # Acessando o endereço através de 'pessoa'
    time = comprador.time  # Acessando o campo "time" diretamente no cliente
    one_piece = comprador.one_piece  # Supondo que você tenha um campo booleano "one_piece" na tabela Cliente

    # Calcula o desconto adicional com base nas informações do banco de dados
    desconto += calculate_discount(endereco, time, one_piece)
    
    # Recalcula o preço final
    preco_final = preco_normal - (preco_normal * (desconto / 100))

    # Atualiza os campos da venda se forem fornecidos
    if data is not None:
        db_venda.data = data
    if comprador_id is not None:
        db_venda.comprador_id = comprador_id
    if vendedor_id is not None:
        db_venda.vendedor_id = vendedor_id
    if preco_normal is not None:
        db_venda.preco_normal = preco_normal
    if desconto is not None:
        db_venda.desconto = desconto
    if preco_final is not None:
        db_venda.preco_final = preco_final
    if forma_pagamento is not None:
        db_venda.forma_pagamento = forma_pagamento
    if status_pagamento is not None:
        db_venda.status_pagamento = status_pagamento
    
    db.commit()
    db.refresh(db_venda)
    return db_venda
