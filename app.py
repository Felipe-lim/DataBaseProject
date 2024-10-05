from pages.home import home
from pages.relatorios import page_relatorios
from pages.estoque import estoque_page  # Importar a nova página
import streamlit as st

from pages.home import home

# Sidebar navigation
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["Home", "Manage Users", "Relatórios", "Estoque"])


# Navigation logic
if page == "Home":
    home()
elif page == "Manage Users":
    manage_users_page()
elif page == "Relatórios":
    page_relatorios()
elif page == "Estoque":  # Adicione a condição para a página "Estoque"
    estoque_page()
