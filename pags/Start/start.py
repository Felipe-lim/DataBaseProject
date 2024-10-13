import streamlit as st
from styles.css import css

def display_start():
   st.markdown(css, unsafe_allow_html=True)
   st.markdown(
      '<h1>Bem-vindo ao Clorofila</h1>',
      unsafe_allow_html=True,
   )
   st.write("Somos um sistema de gerenciamento para estabelerimentos de plantas e flores.")
   st.write("Use a barra lateral para navegar")