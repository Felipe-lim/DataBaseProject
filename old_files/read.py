from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pessoa, Fornecedor, Cliente, Funcionario
from datetime import date


def get_pessoa(db: Session, pessoa_id: str):
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

def get_fornecedor(db: Session, cnpj: str):
    return db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()

def get_cliente(db: Session, cpf: str):
    return db.query(Cliente).filter(Cliente.cpf == cpf).first()

def get_funcionario(db: Session, cpf: str):
    return db.query(Funcionario).filter(Funcionario.cpf == cpf).first()

# Fazer função para pegar todas as informações de todos os usuários
def get_all_pessoas(db: Session):
    return db.query(Pessoa).all()

def get_all_counts(db: Session):
	pessoa_count = db.query(func.count(Pessoa.id)).scalar()
	cliente_count = db.query(func.count(Cliente.pessoa_id)).scalar()
	fornecedor_count = db.query(func.count(Fornecedor.pessoa_id)).scalar()
	funcionario_count = db.query(func.count(Funcionario.pessoa_id)).scalar()
	
	return {
		"Pessoas": pessoa_count,
		"Clientes": cliente_count,
		"Fornecedores": fornecedor_count,
		"Funcionários": funcionario_count
	}