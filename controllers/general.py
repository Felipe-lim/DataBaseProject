from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import streamlit as st
from database.models import Pessoa, Fornecedor, Cliente, Funcionario, Venda
import calendar

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
    # Verificar se há vendas no período
    total_vendas = db.query(func.count(Venda.id)).filter(Venda.data.between(data_inicial, data_final)).scalar()
    
    if total_vendas == 0:
      st.warning(f"Não foram encontradas vendas no período de {data_inicial} a {data_final}.")
      return None

    total_preco_final = db.query(func.sum(Venda.preco_final)).filter(Venda.data.between(data_inicial, data_final)).scalar() or 0

    # Consulta para vendas por vendedor
    vendas_por_vendedor = db.query(
        Pessoa.nome,
        func.count(Venda.id).label('total_vendas'),
        func.sum(Venda.preco_final).label('total_vendido')
    ).join(Funcionario, Venda.vendedor_id == Funcionario.cpf)\
     .join(Pessoa, Funcionario.pessoa_id == Pessoa.id)\
     .filter(Venda.data.between(data_inicial, data_final))\
     .group_by(Pessoa.nome)\
     .all()

    if not vendas_por_vendedor:
        st.warning("Foram encontradas vendas, mas nenhum vendedor associado.")
        
        # Depuração: Verificar vendas sem vendedor associado
        vendas_sem_vendedor = db.query(Venda).filter(Venda.data.between(data_inicial, data_final), Venda.vendedor_id == None).all()
        if vendas_sem_vendedor:
            st.error(f"Existem {len(vendas_sem_vendedor)} vendas sem vendedor associado.")
        
        # Depuração: Verificar funcionários com cargo de vendedor
        vendedores = db.query(Funcionario).filter(Funcionario.cargo == 'vendedor').all()
        if not vendedores:
            st.error("Não existem funcionários com o cargo de vendedor.")
        else:
            st.info(f"Existem {len(vendedores)} funcionários com o cargo de vendedor.")

    relatorio = {
        'Total de Vendas': total_vendas,
        'Total Vendido': total_preco_final,
        'Vendas por Vendedor': [{'nome': nome, 'total_vendas': total, 'total_vendido': vendido} for nome, total, vendido in vendas_por_vendedor],
    }

    return relatorio

def obter_periodo_mes_ano(mes: int, ano: int):
    primeiro_dia = date(ano, mes, 1)
    ultimo_dia = date(ano, mes, calendar.monthrange(ano, mes)[1])
    return primeiro_dia, ultimo_dia