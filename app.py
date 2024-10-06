import streamlit as st
from pags.Start.start import display_start
from pags.users.manager import display_manager
from pags.reports.report import display_report
from pags.orders.Compra import display_compras
from pags.orders.Estoque import show_estoque


def display_pages():
   st.sidebar.title("Navegação")
   page = st.sidebar.radio("Ir para:", ["Início", "Gerenciar Usuários","Relatórios", "Pedidos", "Estoque"])

   match page:
      case "Início":
         display_start()
      case "Gerenciar Usuários":
         display_manager()
      case "Relatórios":
         display_report()
      case "Pedidos":
         display_compras()
      case "Estoque":
         show_estoque()

def main():
   display_pages()

main()