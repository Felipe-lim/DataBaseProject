from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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

class Cliente(Base):
    __tablename__ = "clientes"

    pessoa_id = Column(String, ForeignKey("pessoas.id"))
    cpf = Column(String, primary_key=True, index=True)

    pessoa = relationship("Pessoa", back_populates="cliente")

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
