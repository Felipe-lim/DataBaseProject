import streamlit as st
from database.db import get_db
from controllers.estoque import create_estoque
from sqlalchemy.orm import Session
from models import Estoque, Catalogo


def create_estoque(db: Session, 
                   especie: str, 
                   variedade: str,
                   quantidade: int,
                   fornecedor: str,
                   custo: int,
                   preco: int):
    
    # Verifica se a combinação de especie e variedade existe na tabela catalogo
    catalogo_item = db.query(Catalogo).filter_by(especie=especie, variedade=variedade).first()
    
    # Se não existe no catalogo, cria uma nova entrada
    if not catalogo_item:
        new_catalogo_item = Catalogo(especie=especie, variedade=variedade)
        db.add(new_catalogo_item)
        db.commit()
        db.refresh(new_catalogo_item)
    
    # Cria o novo registro na tabela estoque
    db_estoque = Estoque(especie=especie, 
                         variedade=variedade,
                         quantidade=quantidade,
                         fornecedor=fornecedor,
                         custo=custo,
                         preco=preco)
    
    try:
        db.add(db_estoque)
        db.commit()
        db.refresh(db_estoque)
        return db_estoque
    
    except IntegrityError:
        db.rollback()
        raise Exception("Erro ao cadastrar o produto no estoque. Verifique os dados e tente novamente.")
    

def estoque_page():
    st.title("Cadastro de Produtos no Estoque")
    
    with st.form(key="form_produto"):
        especie = st.text_input("Espécie", max_chars=100)
        variedade = st.text_input("Variedade", max_chars=100)
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        fornecedor = st.text_input("Fornecedor", max_chars=100)
        custo = st.number_input("Custo (em real)", min_value=0, step=100)
        preco = st.number_input("Preço (em real)", min_value=0, step=100)
        
        submit_button = st.form_submit_button(label="Cadastrar Produto")
    
    if submit_button:
        if especie and variedade and fornecedor:
            db = next(get_db())  # Conexão com o banco de dados
            try:
                create_estoque(db, especie, variedade, quantidade, fornecedor, custo, preco)
                st.success("Produto cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao cadastrar produto: {str(e)}")
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios.")

estoque_page()
