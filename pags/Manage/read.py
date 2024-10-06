from utils import get_db, find_user_and_pessoa, get_all_pessoas, validate_input
import streamlit as st
import pandas as pd

def display_read(user_type):
   st.subheader("Ler informações de um usuário")
   read_option = st.radio(
      "Escolha uma opção",
      ["Buscar usuário específico", "Listar todas as pessoas"],
   )

   if read_option == "Buscar usuário específico":
      identifier = st.text_input("Digite o CPF ou CNPJ do usuário")
      if st.button("Obter informações"):
            if validate_input({"Identificador": identifier}):
               db = next(get_db())
               try:
                  user, pessoa = find_user_and_pessoa(db, identifier, user_type)

                  if user and pessoa:
                        data = {
                           "ID": [pessoa.id],
                           "Nome": [pessoa.nome],
                           "Endereço": [pessoa.endereco],
                           "Email": [pessoa.email],
                           "Telefone": [pessoa.telefone],
                           "CEP": [pessoa.cep],
                        }
                        for k, v in user.__dict__.items():
                           if not k.startswith("_"):
                              data[k] = [v]
                        df = pd.DataFrame(data)
                        st.table(df)
                  else:
                        st.warning("Usuário não encontrado.")
               except Exception as e:
                  st.error(f"Erro ao buscar usuário: {str(e)}")

   elif read_option == "Listar todas as pessoas":
      db = next(get_db())
      try:
            pessoas = get_all_pessoas(db)
            if pessoas:
               data = [
                  {
                        "ID": p.id,
                        "Nome": p.nome,
                        "Endereço": p.endereco,
                        "Email": p.email,
                        "Telefone": p.telefone,
                        "CEP": p.cep,
                  }
                  for p in pessoas
               ]
               df = pd.DataFrame(data)
               st.table(df)
            else:
               st.warning("Nenhuma pessoa encontrada.")
      except Exception as e:
            st.error(f"Erro ao listar pessoas: {str(e)}")