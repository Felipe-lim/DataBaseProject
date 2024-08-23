import streamlit as st
import streamlit.components.v1 as components

# Custom CSS for styling with animated background
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(90deg, #CCFF00, #FF00FF);
        padding: 10px;
        border-radius: 10px;
    }

    .stButton > button {
        background-color: black;
        color: white;
    }

    .stButton > button:hover {
        background-color: rgba(6, 12, 139, 0.0)
    
    }

    .stSidebar > div > div {
        background: linear-gradient(90deg, #ADD8E6, #000000);
    }

    .gradient-text {
        background: linear-gradient(90deg, #ADD8E6, #000000);
        -webkit-background-clip: text;
        color: transparent;
        font-size: 2.5em;
        font-weight: bold;
    }


    @keyframes move {
        100% {
            transform: translate3d(0, 0, 1px) rotate(360deg);
        }
    }

    .background {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        background: #000000;
        overflow: hidden;
    }

    .background span {
        width: 20vmin;
        height: 20vmin;
        border-radius: 20vmin;
        backface-visibility: hidden;
        position: absolute;
        animation: move;
        animation-duration: 45;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
    }

    .background span:nth-child(0) {
        color: #62c668;
        top: 1%;
        left: 77%;
        animation-duration: 39s;
        animation-delay: -24s;
        transform-origin: 22vw -14vh;
        box-shadow: -40vmin 0 5.506908077253626vmin currentColor;
    }
    .background span:nth-child(1) {
        color: #14885b;
        top: 77%;
        left: 43%;
        animation-duration: 27s;
        animation-delay: -20s;
        transform-origin: 18vw -17vh;
        box-shadow: 40vmin 0 5.5102515703699835vmin currentColor;
    }
    .background span:nth-child(2) {
        color: #62c668;
        top: 90%;
        left: 49%;
        animation-duration: 17s;
        animation-delay: -14s;
        transform-origin: -15vw -4vh;
        box-shadow: -40vmin 0 5.661700322235795vmin currentColor;
    }
    .background span:nth-child(3) {
        color: #14885b;
        top: 33%;
        left: 81%;
        animation-duration: 15s;
        animation-delay: -21s;
        transform-origin: -3vw -9vh;
        box-shadow: -40vmin 0 5.90205683198467vmin currentColor;
    }
    .background span:nth-child(4) {
        color: #225920;
        top: 66%;
        left: 18%;
        animation-duration: 44s;
        animation-delay: -47s;
        transform-origin: -9vw 24vh;
        box-shadow: 40vmin 0 5.7064626292345vmin currentColor;
    }
    .background span:nth-child(5) {
        color: #62c668;
        top: 49%;
        left: 42%;
        animation-duration: 27s;
        animation-delay: -8s;
        transform-origin: 20vw -11vh;
        box-shadow: -40vmin 0 5.375868295343019vmin currentColor;
    }
    .background span:nth-child(6) {
        color: #14885b;
        top: 79%;
        left: 31%;
        animation-duration: 30s;
        animation-delay: -44s;
        transform-origin: 17vw -11vh;
        box-shadow: -40vmin 0 5.306301417535052vmin currentColor;
    }
    .background span:nth-child(7) {
        color: #225920;
        top: 68%;
        left: 97%;
        animation-duration: 40s;
        animation-delay: -3s;
        transform-origin: -3vw -20vh;
        box-shadow: -40vmin 0 5.802130690688492vmin currentColor;
    }
    .background span:nth-child(8) {
        color: #62c668;
        top: 57%;
        left: 12%;
        animation-duration: 46s;
        animation-delay: -36s;
        transform-origin: -6vw -15vh;
        box-shadow: 40vmin 0 5.204428843063982vmin currentColor;
    }
    .background span:nth-child(9) {
        color: #62c668;
        top: 81%;
        left: 84%;
        animation-duration: 25s;
        animation-delay: -12s;
        transform-origin: 1vw -20vh;
        box-shadow: 40vmin 0 5.123146852554518vmin currentColor;
    }
    .background span:nth-child(10) {
        color: #14885b;
        top: 52%;
        left: 16%;
        animation-duration: 25s;
        animation-delay: -50s;
        transform-origin: -23vw -15vh;
        box-shadow: 40vmin 0 5.300210532013148vmin currentColor;
    }
    .background span:nth-child(11) {
        color: #14885b;
        top: 21%;
        left: 68%;
        animation-duration: 20s;
        animation-delay: -14s;
        transform-origin: 2vw 16vh;
        box-shadow: -40vmin 0 5.122360565094997vmin currentColor;
    }
    .background span:nth-child(12) {
        color: #14885b;
        top: 27%;
        left: 100%;
        animation-duration: 46s;
        animation-delay: -6s;
        transform-origin: -13vw -14vh;
        box-shadow: -40vmin 0 5.079720748024921vmin currentColor;
    }
    .background span:nth-child(13) {
        color: #62c668;
        top: 41%;
        left: 66%;
        animation-duration: 6s;
        animation-delay: -29s;
        transform-origin: -20vw 14vh;
        box-shadow: 40vmin 0 5.583210168495979vmin currentColor;
    }
    .background span:nth-child(14) {
        color: #62c668;
        top: 47%;
        left: 56%;
        animation-duration: 50s;
        animation-delay: -43s;
        transform-origin: 2vw -4vh;
        box-shadow: 40vmin 0 5.224377439415478vmin currentColor;
    }
    .background span:nth-child(15) {
        color: #62c668;
        top: 58%;
        left: 39%;
        animation-duration: 40s;
        animation-delay: -36s;
        transform-origin: -3vw -12vh;
        box-shadow: -40vmin 0 5.822827080362911vmin currentColor;
    }
    .background span:nth-child(16) {
        color: #225920;
        top: 73%;
        left: 44%;
        animation-duration: 33s;
        animation-delay: -41s;
        transform-origin: -18vw 6vh;
        box-shadow: 40vmin 0 5.121471693797897vmin currentColor;
    }
    .background span:nth-child(17) {
        color: #225920;
        top: 12%;
        left: 62%;
        animation-duration: 41s;
        animation-delay: -12s;
        transform-origin: 25vw 9vh;
        box-shadow: -40vmin 0 5.26512217947064vmin currentColor;
    }
    .background span:nth-child(18) {
        color: #62c668;
        top: 34%;
        left: 63%;
        animation-duration: 23s;
        animation-delay: -31s;
        transform-origin: -24vw 3vh;
        box-shadow: -40vmin 0 5.630823125707148vmin currentColor;
    }
    .background span:nth-child(19) {
        color: #225920;
        top: 54%;
        left: 44%;
        animation-duration: 37s;
        animation-delay: -38s;
        transform-origin: -9vw 19vh;
        box-shadow: -40vmin 0 5.346281718221651vmin currentColor;
    }
    </style>
    <div class="background">
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
       <span></span>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["Start", "Manage Users"])

# Functions for user management
def create_user(name, age):
    st.success(f"Usuário '{name}' com {age} anos foi criado com sucesso!")

def read_user(user_id):
    st.info(f"Detalhes do usuário de ID '{user_id}':")

def update_user(user_id, name, age):
    st.success(f"Usuário com ID:'{user_id}' foi atualizado para Nome: {name}, Idade: {age}.")

def delete_user(user_id):
    st.warning(f"Usuário com ID:'{user_id}' foi apagado com sucesso!")

# Page content
if page == "Start":
    st.markdown('<h1 class="gradient-text">Bem-vindo ao CLOROFILA TECH</h1>', unsafe_allow_html=True)
    st.write("Somos um sistema de gerenciamento de ervas finas")
    st.write("Use a barra lateral para navegar")

elif page == "Manage Users":
    st.markdown('<h1 class="gradient-text">Gerenciar Usuários</h1>', unsafe_allow_html=True)

    operation = st.selectbox("Escolha sua operação", ["Create", "Read", "Update", "Delete"])

    user_type = st.radio("Escolha o tipo de usuário", ["Cliente", "Fornecedor", "Funcionário"])

    if operation == "Create":
        st.subheader("Adicionar um novo usuário")
        name = st.text_input("Nome")
        age = st.number_input("Idade do Usuário", min_value=0, max_value=120)
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
