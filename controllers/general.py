from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Pessoa, Fornecedor, Cliente, Funcionario

# Função para pegar todas as informações de todas as pessoas com o join das tabelas relacionadas
def get_all_pessoas(db: Session):
    # Realizando o JOIN com as tabelas de clientes, fornecedores e funcionários
    query = (
        db.query(Pessoa, Cliente, Fornecedor, Funcionario)
        .outerjoin(Cliente, Pessoa.id == Cliente.pessoa_id)
        .outerjoin(Fornecedor, Pessoa.id == Fornecedor.pessoa_id)
        .outerjoin(Funcionario, Pessoa.id == Funcionario.pessoa_id)
        .all()
    )
    
    # Formatando o resultado em uma lista de dicionários para facilitar a visualização e uso
    result = []
    for pessoa, cliente, fornecedor, funcionario in query:
        result.append({
            "id": pessoa.id,
            "nome": pessoa.nome,
            "endereco": pessoa.endereco,
            "email": pessoa.email,
            "telefone": pessoa.telefone,
            "cep": pessoa.cep,
            "cliente": {
                "cpf": cliente.cpf if cliente else None,
                "time": cliente.time if cliente else None,
                "one_piece": cliente.one_piece if cliente else None,
            } if cliente else None,
            "fornecedor": {
                "cnpj": fornecedor.cnpj if fornecedor else None,
                "setor": fornecedor.setor if fornecedor else None,
            } if fornecedor else None,
            "funcionario": {
                "cpf": funcionario.cpf if funcionario else None,
                "cargo": funcionario.cargo if funcionario else None,
                "genero": funcionario.genero if funcionario else None,
                "nascimento": funcionario.nascimento if funcionario else None,
                "naturalidade": funcionario.naturalidade if funcionario else None,
                "salario": funcionario.salario if funcionario else None,
            } if funcionario else None
        })
    
    return result


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