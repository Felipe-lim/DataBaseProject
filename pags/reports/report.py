from utils import get_db
from datetime import date
from controllers.general import get_all_counts, gerar_relatorio_vendas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def display_report():
    db = next(get_db())
    counts = get_all_counts(db)

    st.title("Relatório de Usuários e Vendas")

    tab1, tab2 = st.tabs(["Relatório de Usuários", "Relatório de Vendas"])

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

        data_inicial = st.date_input("Data Inicial", date(2024, 1, 1))
        data_final = st.date_input("Data Final", date(2024, 12, 31))
        
        if st.button("Gerar Relatório de Vendas"):
            relatorio_vendas = gerar_relatorio_vendas(db, data_inicial, data_final)

            st.markdown("### Resumo das Vendas")
            st.metric("Total de Vendas", relatorio_vendas['Total de Vendas'])
            st.metric("Total Vendido", f"R$ {relatorio_vendas['Total Vendido']:,}")

            st.markdown("### Vendas por Vendedor")

            df_vendas_vendedor = pd.DataFrame(relatorio_vendas['Vendas por Vendedor'])
            print("AAIOSJDIJOASIOJDIOJASJIODIOJASOIJDIJOAIJSODIOJAS")
            print(df_vendas_vendedor)
            if not df_vendas_vendedor.empty:
                st.dataframe(df_vendas_vendedor)

                st.markdown("### Gráfico de Vendas por Vendedor")
                fig, ax = plt.subplots()
                ax.bar(df_vendas_vendedor['Vendedor'], df_vendas_vendedor['Total Vendido'], color='skyblue')
                ax.set_xlabel('Vendedores')
                ax.set_ylabel('Total Vendido (R$)')
                ax.set_title('Total Vendido por Vendedor')
                ax.set_xticklabels(df_vendas_vendedor['Vendedor'], rotation=45)
                st.pyplot(fig)
            else:
                st.error("Não foram encontrados dados de vendas por vendedor.")