import streamlit as st
from database.db import get_db
from controllers.venda import *
from controllers.carrinho import *
from controllers.cliente import *
from controllers.pessoas import *
from controllers.estoque import *
from pags.sales.sales_aux import *
from database.models import Estoque
from sqlalchemy import desc
import pandas as pd
from pags.sales.verify_discount import verify_discount
from time import sleep

# Função para buscar e selecionar produtos
def search_and_pick():
    db = next(get_db())
    st.title('Selecione os produtos:')

    if 'user_confirmed' in st.session_state and st.session_state['user_confirmed']:
        with st.form(key='form_plants'):
            especie = st.text_input('Espécie')
            variedade = st.text_input('Variedade')
            search_plant = st.form_submit_button(label='Buscar planta')

        if search_plant:
            # Se os valores de espécie e variedade estiverem preenchidos, faça a busca no banco de dados
            if especie and variedade:
                try:
                    result = db.query(Estoque).filter(Estoque.especie == especie, Estoque.variedade == variedade).order_by(desc(Estoque.quantidade)).all()
                    if result:
                        st.success('Plantas encontradas')

                        # Salvar os resultados no session_state para manter após a interação
                        st.session_state['plants_result'] = [
                            {
                                'especie': item.especie,
                                'variedade': item.variedade,
                                'quantidade': item.quantidade,
                                'fornecedor': item.fornecedor,
                                'custo': item.custo,
                                'preco': item.preco
                            }
                            for item in result
                        ]
                    else:
                        st.error('Planta não encontrada')
                except:
                    st.error(f"Erro ao buscar a planta")
            else:
                st.warning('Por favor, preencha todos os campos obrigatórios.')

    # Verificar se existem resultados armazenados e mostrar a tabela
    if 'plants_result' in st.session_state and st.session_state['plants_result']:
        df = pd.DataFrame(st.session_state['plants_result'])
        st.table(df)

        # Seletor para escolher a planta e quantidade
        plant_selected = f'{especie} {variedade}'
        quantidade = st.number_input('Quantidade', min_value=1, step=1)

        # Inicializar a lista de plantas selecionadas, se ainda não existir
        if 'selected_plants' not in st.session_state:
            st.session_state['selected_plants'] = []

        # Botão para adicionar planta e quantidade à lista
        add_plant_button = st.button('Adicionar planta')

        if add_plant_button:
            # Adiciona no carrinho
            plant_on_estoque = db.query(Estoque).filter(Estoque.especie == especie, Estoque.variedade == variedade).order_by(desc(Estoque.quantidade)).first()
            q_plant_available = plant_on_estoque.quantidade
            
            if q_plant_available >= quantidade:

                id_venda = st.session_state['user_data']['id_venda']
                fornecedor = plant_on_estoque.fornecedor
                custo = plant_on_estoque.custo
                preco = (plant_on_estoque.preco)*quantidade

                carrinho = create_carrinho(db, id_venda, especie, variedade, fornecedor, custo, quantidade)

                if carrinho:
                    # Adicionar a planta e quantidade à lista no session_state
                    st.session_state['selected_plants'].append({
                        'planta': plant_selected,
                        'quantidade': quantidade,
                        'preco': preco
                    })
                    st.success(f'Planta {plant_selected} adicionada com quantidade {quantidade}. +R$ {preco}')

                else:st.error('Não possível adicionar ao carrinho.')
            else:
                st.error('A quantidade do produto é insuficiente.')

    # Exibir a lista de plantas selecionadas, se houver
    if 'selected_plants' in st.session_state and st.session_state['selected_plants']:
        st.subheader('Plantas selecionadas')
        price = 0
        discount = 0

        for plant in st.session_state['selected_plants']:
            st.write(f"Planta: {plant['planta']}    Quantidade: {plant['quantidade']}")
            price += plant['preco']

        st.write('')
        st.write('')
        discount = verify_discount(st.session_state['user_data']['cliente'])
        
        if discount:
            final_price = price * 0.9
            discount = price * 0.1
            st.write('Desconto de 10% adicionado:')
        else:
            final_price = price

        st.markdown(f'### Preço Final R$ {final_price}')
        st.write('')
        st.session_state['payment'] = {
            'preco': price,
            'desconto': discount,
            'preco_final': final_price
        }

        # Formulário para finalizar venda
        with st.form(key='form_pagamento'):
            metodos_pagamento = ["Cartão de Crédito", "Boleto Bancário", "Pix", "Berries"]

            if 'forma_pagamento' not in st.session_state:
                st.session_state['forma_pagamento'] = metodos_pagamento[0]

            # Selecionar método de pagamento
            st.session_state['forma_pagamento'] = st.selectbox(
                "Selecione o método de pagamento:",
                metodos_pagamento,
                index=metodos_pagamento.index(st.session_state['forma_pagamento'])  # Seleciona a escolha atual
            )

            # Botão para confirmar pagamento
            confirmar_pagamento = st.form_submit_button("Confirmar pagamento")

            if confirmar_pagamento:
                venda_updated = update_venda(db,
                                            venda_id=st.session_state['user_data']['id_venda'],
                                            preco_normal=price,
                                            desconto=discount,
                                            preco_final=final_price,
                                            forma_pagamento=st.session_state['forma_pagamento'],
                                            status_pagamento="Aprovado")
                
                carrinho = db.query(Carrinho).filter(Carrinho.id_venda == st.session_state['user_data']['id_venda']).all()
                for item in carrinho:
                    stock_item = get_estoque(db, item.especie, item.variedade, item.fornecedor, item.custo)
                    stock_quantity = stock_item.quantidade
                    new_quantity = stock_quantity - item.quantidade
                    update_estoque(db=db, especie_atual=item.especie, variedade_atual=item.variedade, fornecedor_atual=item.fornecedor, custo_atual=item.custo, quantidade=new_quantity)
                
                if venda_updated:
                    st.success("Pagamento confirmado com sucesso!")
                    
                sleep(5)
                reset_session()

        # Botão para cancelar venda fora do formulário
        if st.button('Cancelar venda'):
            carrinho = db.query(Carrinho).filter(Carrinho.id_venda == st.session_state['user_data']['id_venda']).all()
            for item in carrinho:
                delete_carrinho(db, item.id)
                delete_venda(db, st.session_state['user_data']['id_venda'])
            reset_session()


            
