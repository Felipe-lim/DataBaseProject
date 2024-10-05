import streamlit as st
from css import css


st.markdown(css, unsafe_allow_html=True)
st.markdown(
    '<h1>Bem-vindo ao CLOROFILA TECH</h1>',
    unsafe_allow_html=True,
)
st.write("Somos um sistema de gerenciamento de floriculturas.")
st.write("Use a barra lateral para navegar")