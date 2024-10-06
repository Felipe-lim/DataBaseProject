from controllers.cliente import *
from controllers.fornecedor import *
from controllers.funcionario import *
from controllers.general import *
from controllers.pessoas import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st
import os

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

def buscar_valor(lista, valor):
    for i in range(len(lista)):
        if lista[i] == valor:
            return i
    return -1

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