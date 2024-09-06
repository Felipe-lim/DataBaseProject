from sqlalchemy.orm import Session
from models import Carrinho

def update_carrinho(db: Session,
                    carrinho_id: int,
                    id_venda: int = None,
                    especie: str = None,
                    variedade: str = None,
                    quantidade: int = None):
    
    db_carrinho = get_carrinho(db, carrinho_id)
    if db_carrinho:
        if id_venda is not None:
            db_carrinho.id_venda = id_venda
        if especie is not None:
            db_carrinho.especie = especie
        if variedade is not None:
            db_carrinho.variedade = variedade
        if quantidade is not None:
            db_carrinho.quantidade = quantidade
        
        db.commit()
        db.refresh(db_carrinho)
    return db_carrinho
