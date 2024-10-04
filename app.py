from pages.home import home
from pages.relatorios import page_relatorios
from pages.estoque import estoque_page  # Importar a nova página
import streamlit as st
from pages.plants_page import plants_page
from pages.compras_page import compras_page  # Importar a página de compras

from pages.home import home

# Sidebar navigation
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["Home", "Manage Users", "Relatórios", "Estoque", "Plantas Cadastradas", "Compras"])


# Navigation logic
if page == "Home":
    home()
elif page == "Manage Users":
    manage_users_page()
elif page == "Relatórios":
    page_relatorios()
elif page == "Estoque":  
    estoque_page()
elif page == "Plantas Cadastradas":
    plants_page()  # Exibe a página de plantas
