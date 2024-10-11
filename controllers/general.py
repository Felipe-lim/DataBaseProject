from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from database.models import Pessoa, Fornecedor, Cliente, Funcionario, Venda

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

def gerar_relatorio_vendas(db, data_inicial: date, data_final: date):
    total_vendas = db.query(func.count(Venda.id)).filter(Venda.data.between(data_inicial, data_final)).scalar()
    total_preco_final = db.query(func.sum(Venda.preco_final)).filter(Venda.data.between(data_inicial, data_final)).scalar() or 0

    vendas_por_vendedor = db.query(
        Venda.vendedor_id,
        func.count(Venda.id).label('total_vendas'),
        func.sum(Venda.preco_final).label('total_vendido')
    ).filter(Venda.data.between(data_inicial, data_final)).group_by(Venda.vendedor_id).all()

    relatorio = {
        'Total de Vendas': total_vendas,
        'Total Vendido': total_preco_final,
        'Vendas por Vendedor': {vendedor: {'total_vendas': total, 'total_vendido': vendido} for vendedor, total, vendido in vendas_por_vendedor},
    }

    return relatorio