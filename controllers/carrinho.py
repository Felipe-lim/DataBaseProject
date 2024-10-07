from sqlalchemy.orm import Session
from database.models import Carrinho


def create_carrinho(db: Session,
                    id_venda: int,
                    especie: str,
                    variedade: str,
                    fornecedor: str,
                    custo: int,
                    quantidade: int):
    # Criar um novo objeto Carrinho
    db_carrinho = Carrinho(id_venda=id_venda,
                           especie=especie,
                           variedade=variedade,
                           fornecedor=fornecedor,
                           custo=custo,
                           quantidade=quantidade)

    # Adicionar o novo carrinho ao banco de dados
    db.add(db_carrinho)
    db.commit()
    db.refresh(db_carrinho)  # Atualizar o objeto com os dados salvos no banco de dados
    return db_carrinho



def get_carrinho(db: Session, carrinho_id: int):
    return db.query(Carrinho).filter(Carrinho.id == carrinho_id).first()


def update_carrinho(db: Session,
                    carrinho_id: int,
                    id_venda: int = None,
                    especie: str = None,
                    variedade: str = None,
                    fornecedor: str = None,
                    custo: int = None,
                    quantidade: int = None):
    
    # Buscar o carrinho pelo ID
    db_carrinho = get_carrinho(db, carrinho_id)
    
    # Se o carrinho existir, atualize os campos informados
    if db_carrinho:
        if id_venda is not None:
            db_carrinho.id_venda = id_venda
        if especie is not None:
            db_carrinho.especie = especie
        if variedade is not None:
            db_carrinho.variedade = variedade
        if fornecedor is not None:
            db_carrinho.fornecedor = fornecedor
        if custo is not None:
            db_carrinho.custo = custo
        if quantidade is not None:
            db_carrinho.quantidade = quantidade
        
        # Fazer o commit e atualizar os dados
        db.commit()
        db.refresh(db_carrinho)
    return db_carrinho



def delete_carrinho(db: Session, carrinho_id: int):
    # Buscar o carrinho pelo ID
    db_carrinho = get_carrinho(db, carrinho_id)
    
    # Se o carrinho existir, deletá-lo
    if db_carrinho:
        db.delete(db_carrinho)
        db.commit()
        return True
    return False

