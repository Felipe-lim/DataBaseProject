from database.db import get_db
from controllers.cliente import *
from controllers.pessoas import *

def verify_discount(cliente_id):
    db = next(get_db())

    cliente = get_cliente(db, cliente_id)
    time = cliente.time
    time = time.lower()
    one_pice = cliente.one_piece

    pessoa = get_pessoa(db, cliente.pessoa_id)
    endereco = pessoa.endereco
    endereco = endereco.lower()

    if one_pice == "Assiste" or time == "flamengo" or endereco == "sousa":
        return True
    else:
        return False
