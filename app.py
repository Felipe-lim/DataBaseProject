import streamlit as st

# Sidebar
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["Start", "Manage Users"])

# Placeholder functions for CRUD operations
def create_user(name, age):
    st.success(f"Usuário '{name}' com {age} anos foi criado com sucesso!")

def read_user(user_id):
    st.info(f"Detalhes do usuário de ID '{user_id}':")

def update_user(user_id, name, age):
    st.success(f"Usuário com ID:'{user_id}' foi atualizado para Nome: {name}, Idade: {age}.")

def delete_user(user_id):
    st.warning(f"Usuário com ID:'{user_id}' foi apagado com sucesso!")

# Main application content
if page == "Start":
    st.title("Bem-vindo ao CLOROFILA TECH")
    st.write("Somos um sistema de gerenciamento de ervas finas")
    st.write("Use a barra lateral para navegar")


elif page == "Manage Users":
    st.title("Gerenciar Usuários")
    
    operation = st.selectbox("Escolha sua operação", ["Create", "Read", "Update", "Delete"])
    
    if operation == "Create":
        st.subheader("Adicionar um novo usuário")
        name = st.text_input("Nome")
        age = st.number_input("Usuário", min_value=0, max_value=120)
        if st.button("Criar"):
            create_user(name, age)
    
    elif operation == "Read":
        st.subheader("Ler informações de um usuário")
        user_id = st.text_input("Digite o ID do usuário")
        if st.button("Obter informações"):
            read_user(user_id)
    
    elif operation == "Update":
        st.subheader("Atualizar informações de um usuário")
        user_id = st.text_input("Digite o ID do usuário")
        name = st.text_input("Novo nome")
        age = st.number_input("Nova idade", min_value=0, max_value=120)
        if st.button("Atualizar"):
            update_user(user_id, name, age)
    
    elif operation == "Delete":
        st.subheader("Deletar um usuário")
        user_id = st.text_input("Digite o ID do usuário")
        if st.button("Apagar"):
            delete_user(user_id)
