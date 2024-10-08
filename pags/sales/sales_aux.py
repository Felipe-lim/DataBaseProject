import streamlit as st

# Função para resetar o session_state
def reset_session():
    if 'user_confirmed' in st.session_state:
        del st.session_state['user_confirmed']
    if 'user_data' in st.session_state:
        del st.session_state['user_data']
    if 'plants_result' in st.session_state:
        del st.session_state['plants_result']
    if 'selected_plants' in st.session_state:
        del st.session_state['selected_plants']

    st.rerun()
    st.success("Sessão resetada! Pronto para nova compra.")
    
