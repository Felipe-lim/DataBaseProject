# Sistema de Gerenciamento para Floricultura

Este projeto é um sistema de gerenciamento para uma floricultura, desenvolvido utilizando **PostgreSQL** para o banco de dados e **Streamlit** para a interface web. O sistema permite gerenciar o estoque de flores, pedidos, clientes e muito mais, de forma eficiente e organizada.

## Desenvolvedores

- [Felipe Lima](github.com/felipe-lim)
- [Fernando D'ávila](github.com/taldofernando)
- [Victor Marques](github.com/victornw)

## Funcionalidades

- **Gerenciamento de Estoque**: Controle o estoque de flores disponíveis para venda, adicione novos produtos e monitore as quantidades.
- **Gerenciamento de Pedidos**: Crie e acompanhe o status de cada pedido.
- **Gerenciamento de Usuários**: Adicione e gerencie informações dos usuários, como nome, contato e outras informações relevantes.
- **Relatórios**: Gere relatórios sobre as vendas e estoque, visualizando dados históricos diretamente na interface do Streamlit.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação usada para desenvolver toda a lógica do backend e integração com o banco de dados.
- **PostgreSQL**: Sistema de banco de dados relacional utilizado para armazenar e gerenciar as informações de clientes, produtos e pedidos.
- **Streamlit**: Framework utilizado para construir a interface web interativa e visualizações de dados.
- **SQLAlchemy**: Biblioteca ORM para facilitar a comunicação com o banco de dados PostgreSQL.

## Instalação

### Requisitos

- Python 3.9+
- PostgreSQL 13+
- Streamlit 1.5+
- SQLAlchemy

### Passos para Rodar o Projeto Localmente

1. Clone este repositório:

    ```bash
    git clone https://github.com/Felipe-lim/DataBaseProject.git
    cd seu-projeto
    ```

2. Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate  # Windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados PostgreSQL e ajuste o arquivo `.env` com suas credenciais:

    ```bash
    DATABASE_URL=postgresql://usuario:senha@localhost:5432/floricultura
    ```

5. Crie as tabelas:

    ```bash
    python -m database.create_database
    ```

6. Rode o projeto:

    ```bash
    streamlit run app.py
    ```

7. Acesse a aplicação no navegador:

    ```
    http://localhost:8501
    ```

## Estrutura do Projeto

- **app.py**: Arquivo principal da aplicação Streamlit.
- **database/**: Configuração do banco de dados e modelos SQLAlchemy.
- **controllers**: CRUD das tabelas.
- **pags/**: Diretório contendo as diferentes páginas do sistema (ex.: estoque, pedidos, clientes).
- **requirements.txt**: Lista de dependências do projeto.


## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
