from sqlalchemy.orm import Session
from models import Carrinho


def create_carrinho(db: Session,
                    id_venda: int,
                    especie: str,
                    variedade: str,
                    quantidade: int):
    db_carrinho = Carrinho(id_venda=id_venda,
                           especie=especie,
                           variedade=variedade,
                           quantidade=quantidade)

    db.add(db_carrinho)
    db.commit()
    db.refresh(db_carrinho)
    return db_carrinho

