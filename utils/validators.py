import streamlit as st

def validate_input(fields):
    for field, value in fields.items():
        if not value or (isinstance(value, str) and value.strip() == ""):
            st.error(f"O campo '{field}' é obrigatório.")
            return False
    return True
