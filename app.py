import streamlit as st
from pags.Start.start import display_start
from pags.Manage.manager import display_manager
from pags.reports.report import display_report
from pags.orders.Compra import display_compras


def display_pages():
   st.sidebar.title("Navegação")
   page = st.sidebar.radio("Ir para:", ["Start", "Manage Users","Relatórios", "Orders"])

   match page:
      case "Start":
         display_start()
      case "Manage Users":
         display_manager()
      case "Relatórios":
         display_report()
      case "Orders":
         display_compras()

def main():
   display_pages()

main()