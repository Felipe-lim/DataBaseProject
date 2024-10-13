import streamlit as st
import pandas as pd
from database.db import get_db
from controllers.estoque import get_all_estoque, update_estoque_info 

def show_estoque():
    st.title("Estoque Disponível: ")

    # Conectar ao banco de dados
    db = next(get_db())

    # Obtém todos os produtos no estoque
    estoque_list = get_all_estoque(db)

    # Converta os dados para um DataFrame do Pandas
    if estoque_list:
        data = [
            {
                "Nome": f"{item.especie} {item.variedade}",
                "Especie": item.especie,
                "Variedade": item.variedade,
                "Quantidade": item.quantidade,
                "Fornecedor": item.fornecedor,
                "Custo": item.custo,
                "Preço": item.preco
            }
            for item in estoque_list
        ]

        df = pd.DataFrame(data)

        # Filtros
        st.subheader("Filtros")
        
        # Filtro por nome
        filtro_nome = st.text_input("Buscar por nome do produto")

        # Filtro por espécie e variedade
        filtro_especie_variedade = st.text_input("Buscar por espécie ou variedade")

        # Filtro por fornecedor/origem
        filtro_fornecedor = st.text_input("Buscar por fornecedor")

        # Filtro para quantidade < 5
        filtro_quantidade = st.checkbox("Mostrar apenas produtos com quantidade menor que 5")

        # Aplicando filtros no DataFrame
        if filtro_nome:
            df = df[df['Nome'].str.contains(filtro_nome, case=False, na=False)]

        if filtro_especie_variedade:
            df = df[
                df['Especie'].str.contains(filtro_especie_variedade, case=False, na=False) |
                df['Variedade'].str.contains(filtro_especie_variedade, case=False, na=False)
            ]

        if filtro_fornecedor:
            df = df[df['Fornecedor'].str.contains(filtro_fornecedor, case=False, na=False)]

        if filtro_quantidade:
            df = df[df['Quantidade'] < 5]

        # Mostrando a tabela filtrada ou não filtrada
        st.subheader("Lista de Produtos no Estoque")
        st.table(df)

    else:
        st.write("Nenhum produto disponível no estoque.")

    # Opção de editar dados de um produto específico
    st.subheader("Editar Informações de um Produto")

        # Escolha o nome do produto (que será dividido em especie e variedade)
    nome_produto = st.selectbox("Nome do Produto", df['Nome'].unique())

    # Quebra o nome em espécie e variedade
    especie_produto, variedade_produto = nome_produto.split(" ", 1)

    # Campos para modificar a quantidade, custo e preço
    nova_quantidade = st.number_input("Nova Quantidade do Produto", step=1, min_value=0)
    novo_preco = st.number_input("Novo Preço do Produto", step=1)
    novo_custo = st.number_input("Novo Custo do Produto", step=1)


        # Botão para atualizar as informações
    if st.button("Atualizar Informações"):
        if especie_produto and variedade_produto and nova_quantidade is not None and novo_preco is not None and novo_custo is not None:
            # Chama a procedure para atualizar os dados
            produto_atualizado = update_estoque_info(
                db,
                especie_produto=especie_produto,
                variedade_produto=variedade_produto,
                nova_quantidade=nova_quantidade,
                novo_custo=novo_custo,
                novo_preco=novo_preco
            )
            if produto_atualizado:
                st.success(f"Informações do produto {nome_produto} atualizadas com sucesso!")
            else:
                st.error("Erro ao atualizar o produto.")
        else:
            st.error("Preencha todos os campos antes de atualizar.")
