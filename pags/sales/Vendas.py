import streamlit as st
from controllers.venda import *
from controllers.carrinho import *
from controllers.cliente import *
from controllers.pessoas import *
from pags.sales.sale_user_register import user_register
from pags.sales.sales_aux import *
from pags.sales.search_and_pick import search_and_pick


# Função principal para exibir a venda
def display_vendas():
    user_confirmed = user_register()
    if user_confirmed:
        search_and_pick()

# Exibir a interface
display_vendas()
