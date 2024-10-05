from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from database.db import Base

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, index=True)
    endereco = Column(String)
    email = Column(String)
    telefone = Column(String)
    cep = Column(String)

    fornecedor = relationship("Fornecedor", back_populates="pessoa", uselist=False)
    cliente = relationship("Cliente", back_populates="pessoa", uselist=False)
    funcionario = relationship("Funcionario", back_populates="pessoa", uselist=False)

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    pessoa_id = Column(String, ForeignKey("pessoas.id"))
    cnpj = Column(String, primary_key=True, index=True)
    setor = Column(String)
    
    pessoa = relationship("Pessoa", back_populates="fornecedor")
    compras = relationship("Compra", back_populates="fornecedor")  # Corrigido para plural

class Cliente(Base):
    __tablename__ = "clientes"

    pessoa_id = Column(String, ForeignKey("pessoas.id"))
    cpf = Column(String, primary_key=True, index=True)
    time = Column(String) #atualizar no streamlit 
    one_piece = Column(String) #atualizar no streamlit 

    pessoa = relationship("Pessoa", back_populates="cliente")
    vendas = relationship("Venda", back_populates='cliente')  # Corrigido para plural


class Funcionario(Base):
    __tablename__ = "funcionarios"

    pessoa_id = Column(String, ForeignKey("pessoas.id"))
    cpf = Column(String, primary_key=True, index=True)
    cargo = Column(String)
    genero = Column(String)
    nascimento = Column(Date)
    naturalidade = Column(String)
    salario = Column(Integer)
    
    pessoa = relationship("Pessoa", back_populates="funcionario")
    vendas = relationship("Venda", back_populates="funcionario")  # Corrigido para plural

class Catalogo(Base):
    __tablename__ = "catalogo"

    especie = Column(String, index=True)
    variedade = Column(String)
    nome_popular = Column(String)
    origem = Column(String)
    ambiente = Column(String)
    cuidado = Column(String)
    utilidade = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint('especie', 'variedade'),
    )

    estoque = relationship("Estoque", back_populates="catalogo", uselist=False)  # Corrigido para False
    compras = relationship("Compra", back_populates="catalogo")  # Adicionado para definir o relacionamento inverso

class Estoque(Base):
    __tablename__ = "estoque"

    especie = Column(String)
    variedade = Column(String)
    quantidade = Column(Integer)
    fornecedor = Column(String)
    custo = Column(Integer)
    preco = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('especie', 'variedade'),
        ForeignKeyConstraint(['especie', 'variedade'], ['catalogo.especie', 'catalogo.variedade']),
    )

    catalogo = relationship("Catalogo", back_populates="estoque", uselist=False)  # Corrigido para False
    carrinho = relationship("Carrinho", back_populates="estoque")  # Adicionado para definir o relacionamento inverso

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date)
    comprador_id = Column(String, ForeignKey("clientes.cpf"))
    vendedor_id = Column(String, ForeignKey("funcionarios.cpf"))
    preco_normal = Column(Integer)
    desconto = Column(Integer)
    preco_final = Column(Integer)
    forma_pagamento = Column(String)
    status_pagamento = Column(String)

    cliente = relationship("Cliente", back_populates="vendas")  # Certifique-se de que está correto
    funcionario = relationship("Funcionario", back_populates="vendas")  # Certifique-se de que está correto
    carrinho = relationship("Carrinho", back_populates="venda")  # Certifique-se de que o relacionamento é singular

class Carrinho(Base):
    __tablename__ = "carrinho"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_venda = Column(Integer, ForeignKey("vendas.id"))
    especie = Column(String)
    variedade = Column(String)
    quantidade = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(['especie', 'variedade'], ['estoque.especie', 'estoque.variedade']),
    )

    estoque = relationship("Estoque", back_populates="carrinho")
    venda = relationship("Venda", back_populates="carrinho")
    
class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date)
    fornecedor_cnpj = Column(String, ForeignKey("fornecedores.cnpj"))
    quantidade = Column(Integer)
    especie = Column(String)
    variedade = Column(String)
    custo = Column(Integer)
    forma_pagamento = Column(String)

    __table_args__ = (
        ForeignKeyConstraint(['especie', 'variedade'], ['catalogo.especie', 'catalogo.variedade']),
    )

    fornecedor = relationship("Fornecedor", back_populates="compras")
    catalogo = relationship("Catalogo", back_populates="compras")
