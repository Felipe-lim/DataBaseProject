from utils import get_db, find_user_and_pessoa, get_all_pessoas, validate_input
import streamlit as st
import pandas as pd
from validate import validar_cnpj, validar_cpf 
from database.models import Pessoa, Cliente, Fornecedor, Funcionario
from sqlalchemy import case, func
from sqlalchemy.orm import aliased

def display_read(user_type):
   st.subheader("Ler informações de um usuário")
   read_option = st.radio(
      "Escolha uma opção",
      ["Buscar usuário específico", "Listar todas as pessoas"],
   )

   if read_option == "Buscar usuário específico":
      identifier = st.text_input("Digite o CPF ou CNPJ do usuário")
      if st.button("Obter informações"):
            status, error = validar_cnpj(identifier) or validar_cpf(identifier)
            if status:
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
            else:
               st.error(error)

   elif read_option == "Listar todas as pessoas":
      db = next(get_db())
      try:
         pessoas = view_pessoa_detalhada(db)  # Obtém os dados da view

         if pessoas:
            # Estrutura os dados em uma lista de dicionários
            data = [
                  {
                     "Nome": p.nome,
                     "Endereço": p.endereco,
                     "Email": p.email,
                     "Telefone": p.telefone,
                     "CEP": p.cep,
                     "Documento": p.documento,  # CPF ou CNPJ
                     "Tipo": p.tipo,  # Cliente, Fornecedor ou Funcionario
                  }
                  for p in pessoas
            ]

            # Cria um DataFrame do Pandas para exibir os dados
            df = pd.DataFrame(data)

            # Exibe a tabela no Streamlit
            st.markdown("### Detalhes das Pessoas")
            st.table(df)
         else:
            st.warning("Nenhuma pessoa encontrada.")
      except Exception as e:
         st.error(f"Erro ao listar pessoas: {str(e)}")




def view_pessoa_detalhada(db):
    cliente = aliased(Cliente)
    fornecedor = aliased(Fornecedor)
    funcionario = aliased(Funcionario)

    query = db.query(
        Pessoa.nome,
        Pessoa.endereco,
        Pessoa.email,
        Pessoa.telefone,
        Pessoa.cep,
        func.coalesce(cliente.cpf, funcionario.cpf, fornecedor.cnpj).label('documento'),
        case(
            (cliente.cpf != None, 'Cliente'),  
            (funcionario.cpf != None, 'Funcionario'), 
            else_='Fornecedor' 
        ).label('tipo')
    ).outerjoin(cliente, Pessoa.id == cliente.pessoa_id)\
     .outerjoin(funcionario, Pessoa.id == funcionario.pessoa_id)\
     .outerjoin(fornecedor, Pessoa.id == fornecedor.pessoa_id)

    return query.all()

