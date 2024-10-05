import streamlit as st
from datetime import date
from sqlalchemy.orm import Session
from controllers.venda import create_venda, get_venda, update_venda, delete_venda, get_all_vendas
from controllers.estoque import get_all_estoque, update_estoque_quantity
from controllers.cliente import get_cliente
from controllers.funcionario import get_funcionario
from database import get_db
from database.models import Cliente, Funcionario, Venda, Estoque




# Função para aplicar desconto com base nos critérios do cliente
def calcular_desconto(cliente: Cliente):
    desconto = 0
    if 'Sousa' in cliente.pessoa.endereco:  
        desconto = 5
    if cliente.time.lower() == 'flamengo':
        desconto = 5
    if cliente.one_piece.lower() == 'sim':
        desconto = 5
    return desconto


# Função para exibir todos os produtos em estoque, incluindo o preço de venda
def display_estoque(db: Session):
    estoque = get_all_estoque(db)
    st.write("## Estoque Disponível")
    
    # Iterando sobre o estoque e exibindo o nome do produto, quantidade e preço
    for item in estoque:
        nome_produto = f"{item.especie} - {item.variedade} | Quantidade: {item.quantidade} | Preço: R$ {item.preco:.2f}"
        st.write(nome_produto)  # Exibir cada item formatado corretamente
    
    # Retornar um dicionário, se necessário, para uso posterior
    estoque_dict = {f"{item.especie} - {item.variedade}": item for item in estoque}
    return estoque_dict


# Função para exibir todas as vendas
def display_vendas(db: Session):
    vendas = get_all_vendas(db)
    st.write("## Lista de Vendas")
    if vendas:
        for venda in vendas:
            st.write(f"ID: {venda.id}, Data: {venda.data}, Comprador CPF: {venda.comprador_id}, "
                     f"Vendedor CPF: {venda.vendedor_id}, Preço Normal: {venda.preco_normal}, "
                     f"Desconto: {venda.desconto}, Preço Final: {venda.preco_final}, "
                     f"Forma de Pagamento: {venda.forma_pagamento}, Status de Pagamento: {venda.status_pagamento}")
    else:
        st.write("Nenhuma venda cadastrada.")


# Função para adicionar uma nova venda
def adicionar_venda(db: Session):
    st.write("## Adicionar uma nova venda")
    
    # Seleção do comprador e vendedor
    comprador_cpf = st.text_input("CPF do Comprador", key="comprador_cpf")
    vendedor_cpf = st.text_input("CPF do Vendedor", key="vendedor_cpf")
    
    # Buscar o cliente com base no CPF
    cliente = get_cliente(db, comprador_cpf)
    
    # Verificar o que está retornando da função get_cliente
    st.write(f"Resultado da busca do cliente: {cliente}")
    
    # Teste para verificar se o relacionamento com pessoa está funcionando
    if cliente:
        st.write(f"Endereço do cliente: {cliente.pessoa.endereco}")  # Teste explícito para ver se está acessando o endereço
    else:
        st.error("Cliente não encontrado!")    # Exibir estoque e permitir adicionar itens ao carrinho
    estoque_dict = display_estoque(db)
    carrinho = []

    # Seleção de produtos e quantidades
    for nome, item in estoque_dict.items():
        quantidade = st.number_input(f"Quantidade de {nome}", min_value=0, max_value=item.quantidade)
        if quantidade > 0:
            carrinho.append({'item': item, 'quantidade': quantidade})
    
    # Verificar o vendedor
    vendedor = get_funcionario(db, vendedor_cpf)
    if not vendedor:
        st.error("Vendedor não encontrado. Verifique o CPF e tente novamente.")
        return  # Interrompe o fluxo aqui também, se o vendedor não for encontrado

    # Calcular desconto e exibir o valor do desconto conseguido pelo cliente
    desconto_percentual = calcular_desconto(cliente)
    st.write(f"Desconto conseguido: {desconto_percentual}%")  # Exibir o desconto percentual para o cliente

    # Processamento final da venda
    if st.button("Finalizar Venda") and vendedor:
        preco_normal = sum([item['item'].preco * item['quantidade'] for item in carrinho])
        desconto = (preco_normal * desconto_percentual) / 100
        preco_final = preco_normal - desconto
        
        try:
            # Criar a venda com os CPFs sem formatação
            venda = create_venda(
                db=db,
                data=date.today(),
                comprador_id=cliente.cpf,  # CPF do cliente
                vendedor_id=vendedor.cpf,  # CPF do vendedor
                preco_normal=preco_normal,
                desconto=desconto,
                preco_final=preco_final,
                forma_pagamento="Dinheiro",
                status_pagamento="Pendente"
            )
            
            # Atualizar o estoque
            for item in carrinho:
                update_estoque_quantity(db, item['item'].especie, item['item'].variedade, item['quantidade'])

            st.success(f"Venda adicionada com sucesso! ID da venda: {venda.id} Preço Final: {preco_final}")
        
        except Exception as e:
            st.error(f"Erro ao adicionar venda: {str(e)}")



# Exibir a interface do Streamlit
st.title("Gerenciamento de Vendas")

# Opções do sistema
option = st.selectbox("Selecione a ação", ["Ver todas as vendas", "Adicionar venda", "Atualizar venda", "Deletar venda"])

# Inicializar a sessão do banco de dados
db = next(get_db())

# Lógica para cada opção
if option == "Ver todas as vendas":
    display_vendas(db)

elif option == "Adicionar venda":
    adicionar_venda(db)

elif option == "Atualizar venda":
    st.write("## Atualizar uma venda")

    venda_id = st.number_input("ID da venda", min_value=1)
    venda = get_venda(db, venda_id)
    if venda:
        st.write(f"Atualizando venda ID: {venda_id}")
        data = st.date_input("Data da venda", value=venda.data)
        comprador_cpf = st.text_input("CPF do Comprador", value=venda.comprador_id, key="comprador_cpf_update")
        vendedor_cpf = st.text_input("CPF do Vendedor", value=venda.vendedor_id, key="vendedor_cpf_update")
        preco_normal = st.number_input("Preço Normal", min_value=0, value=venda.preco_normal)
        desconto = st.number_input("Desconto", min_value=0, value=venda.desconto)
        preco_final = st.number_input("Preço Final", min_value=0, value=venda.preco_final)
        forma_pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão", "Pix"], index=["Dinheiro", "Cartão", "Pix"].index(venda.forma_pagamento))
        status_pagamento = st.selectbox("Status de Pagamento", ["Pendente", "Pago", "Cancelado"], index=["Pendente", "Pago", "Cancelado"].index(venda.status_pagamento))

        if st.button("Atualizar"):
            try:
                updated_venda = update_venda(db, venda_id, data, comprador_cpf, vendedor_cpf, preco_normal, desconto, preco_final, forma_pagamento, status_pagamento)
                st.success(f"Venda ID {updated_venda.id} atualizada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao atualizar venda: {str(e)}")
    else:
        st.error("Venda não encontrada!")

elif option == "Deletar venda":
    st.write("## Deletar uma venda")

    venda_id = st.number_input("ID da venda para deletar", min_value=1)

    if st.button("Deletar"):
        success = delete_venda(db, venda_id)
        if success:
            st.success(f"Venda ID {venda_id} deletada com sucesso!")
        else:
            st.error(f"Venda ID {venda_id} não encontrada!")
