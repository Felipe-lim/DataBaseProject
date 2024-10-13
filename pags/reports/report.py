from utils import get_db
from datetime import date
from controllers.general import get_all_counts, gerar_relatorio_vendas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from database.models import Venda, Funcionario

def display_report():
   db = next(get_db())
   counts = get_all_counts(db)

   st.title("Relatório de Usuários e Vendas")

   tab1, tab2 = st.tabs(["Relatório de Usuários", "Relatório de Funcionários"])

   with tab1:
      st.subheader("Resumo de Cadastro")
      
      col1, col2, col3, col4 = st.columns(4)
      col1.metric("Pessoas Cadastradas", counts['Pessoas'])
      col2.metric("Clientes", counts['Clientes'])
      col3.metric("Fornecedores", counts['Fornecedores'])
      col4.metric("Funcionários", counts['Funcionários'])

      st.markdown("---")

      st.subheader("Detalhes dos Cadastros")
      detalhes = {
         "Tipo": ["Pessoas", "Clientes", "Fornecedores", "Funcionários"],
         "Total": [counts['Pessoas'], counts['Clientes'], counts['Fornecedores'], counts['Funcionários']]
      }
      df_detalhes = pd.DataFrame(detalhes)
      st.dataframe(df_detalhes)

   with tab2:
      st.subheader("Relatório de Vendas")

      year = st.selectbox("Selecione o ano desejado", (2023, 2024, 2025))
      month = st.number_input("Selecione o mês desejado", min_value=1, max_value=12, value=1)

      data_inicial = date(year, month, 1)
      if(month == 12):
         data_final = date(year+1, 1, 1)
      else:
         data_final = date(year, month+1, 1)
      
      if st.button("Gerar Relatório de Vendas"):
         relatorio_vendas = gerar_relatorio_vendas(db, data_inicial, data_final)

         if relatorio_vendas:
               st.markdown("### Resumo das Vendas")
               st.metric("Total de Vendas", relatorio_vendas['Total de Vendas'])
               st.metric("Total Vendido", f"R$ {relatorio_vendas['Total Vendido']:,.2f}")

               st.markdown("### Vendas por Vendedor")

               df_vendas_vendedor = pd.DataFrame(relatorio_vendas['Vendas por Vendedor'])

               if not df_vendas_vendedor.empty:
                  st.dataframe(df_vendas_vendedor)

                  st.markdown("### Gráfico de Vendas por Vendedor")
                  
                  fig = px.bar(
                     df_vendas_vendedor,
                     x='nome',
                     y='total_vendido',
                     title='Total Vendido por Vendedor',
                     labels={'nome': 'Vendedor', 'total_vendido': 'Total Vendido (R$)'},
                     color='total_vendido',
                     color_continuous_scale='Viridis'
                  )
                  
                  fig.update_layout(
                     xaxis_tickangle=-45,
                     yaxis_title='Total Vendido (R$)',
                     coloraxis_showscale=False
                  )

                  fig.update_traces(
                     hovertemplate='<b>%{x}</b><br>Total Vendido: R$ %{y:.2f}<extra></extra>'
                  )

                  st.plotly_chart(fig, use_container_width=True)
               else:
                  st.error("Não foram encontrados dados de vendas por vendedor.")
         else:
               st.error("Não foi possível gerar o relatório de vendas.")
