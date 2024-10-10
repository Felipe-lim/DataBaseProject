import re
from datetime import datetime, date

def validar_texto(valor, campo, min_len=2, max_len=100):
    if not valor or len(valor.strip()) < min_len:
        return False, f"{campo} deve ter pelo menos {min_len} caracteres."
    if len(valor) > max_len:
        return False, f"{campo} deve ter no máximo {max_len} caracteres."
    return True, ""

def validar_nome(nome):
    if not nome:
        return False, "Nome é obrigatório."
    if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
        return False, "Nome deve conter apenas letras."
    return validar_texto(nome, "Nome")

def validar_endereco(endereco):
    return validar_texto(endereco, "Endereço", min_len=5)

def validar_email(email):
    if not email:
        return False, "Email é obrigatório."
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(padrao, email):
        return False, "Email inválido."
    return True, ""

def validar_telefone(telefone):
    if not telefone:
        return False, "Telefone é obrigatório."
    telefone_limpo = re.sub(r'\D', '', telefone)
    if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
        return False, "Telefone deve ter 10 ou 11 dígitos."
    return True, ""

def validar_cep(cep):
    if not cep:
        return False, "CEP é obrigatório."
    cep_limpo = re.sub(r'\D', '', cep)
    if len(cep_limpo) != 8:
        return False, "CEP deve ter 8 dígitos."
    return True, ""

def calcular_digito_cpf(cpf_parcial):
    multiplicadores1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma1 = sum(int(cpf_parcial[i]) * multiplicadores1[i] for i in range(9))
    resto1 = soma1 % 11
    primeiro_digito = 11 - resto1 if resto1 >= 2 else 0
    
    multiplicadores2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    cpf_parcial_com_primeiro = cpf_parcial + str(primeiro_digito)
    soma2 = sum(int(cpf_parcial_com_primeiro[i]) * multiplicadores2[i] for i in range(10))
    resto2 = soma2 % 11
    segundo_digito = 11 - resto2 if resto2 >= 2 else 0
    
    return str(primeiro_digito) + str(segundo_digito)

def calcular_digito_cnpj(cnpj_parcial):
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    soma = sum(int(cnpj_parcial[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    primeiro_digito = 0 if resto < 2 else 11 - resto
    
    cnpj_parcial += str(primeiro_digito)
    soma = sum(int(cnpj_parcial[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    segundo_digito = 0 if resto < 2 else 11 - resto
    
    return str(primeiro_digito) + str(segundo_digito)

def validar_cpf(cpf):
    if not cpf:
      return False, "CPF é obrigatório"

    cpf_limpo = re.sub(r'\D', '', cpf)
    
    if len(cpf_limpo) != 11 or len(set(cpf_limpo)) == 1:
        return False, "CPF inválido"
    
    cpf_parcial = cpf_limpo[:9]
    digitos_calculados = calcular_digito_cpf(cpf_parcial)

    if cpf_limpo[-2:] != digitos_calculados:
        return False, "CPF inválido"
    
    return True, "CPF válido"

def validar_cnpj(cnpj):
   if not cnpj:
      return False, "CNPJ é obrigatório."

   cnpj_limpo = re.sub(r'\D', '', cnpj)
   
   if len(cnpj_limpo) != 14 or len(set(cnpj_limpo)) == 1:
      return False, "CNPJ inválido"
   
   cnpj_parcial = cnpj_limpo[:12]
   digitos = calcular_digito_cnpj(cnpj_parcial)
   
   if cnpj_limpo[-2:] != digitos:
      return False, "CNPJ inválido"
   
   return True, "CNPJ válido"

def validar_data_nascimento(data_nascimento):
   if not data_nascimento:
      return False, "Data de nascimento é obrigatória."
   if not isinstance(data_nascimento, date):
      return False, "Data de nascimento inválida."
   hoje = date.today()
   idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
   if idade < 18:
      return False, "Funcionário deve ter pelo menos 18 anos."
   if idade > 130:
      return False, "Data de nascimento inválida."
   return True, ""

def validar_data(data, campo="Data", permitir_futuro=False):
    hoje = date.today()

    if not data:
      return False, f"{campo} é obrigatorio."
    
    if not isinstance(data, date):
      return False, f"{campo} deve ser uma data válida."
    
    if not permitir_futuro and data > hoje:
      return False, f"{campo} não pode ser uma data futura."
    
    return True, ""

def validar_salario(salario):
   if not salario:
      return False, "Salário é obrigatório."
   if salario < 0:
      return False, "Salário não pode ser negativo."
   return True, ""

def validar_numero(valor, campo, min_valor=0, max_valor=10**123):
    if not valor: 
      return False, f"{campo} é obrigatório."
    if valor < min_valor:
        return False, f"{campo} deve ter pelo menos {min_valor} {valor}"
    if valor > max_valor:
        return False, f"{campo} deve ter no máximo {max_valor} {valor}."
    return True, ""

def validar_genero(genero):
    opcoes_validas = ["Masculino", "Feminino", "Outro"]
    if not genero or genero not in opcoes_validas:
        return False, "Selecione um gênero válido."
    return True, ""

def validar_one_piece(opcao):
    opcoes_validas = ["Assiste", "Não assiste"]
    if not opcao or opcao not in opcoes_validas:
        return False, "Selecione uma opção válida para One Piece."
    return True, ""

def validar_forma_pagamento(opcao):
    opcoes_validas = ["dinheiro", "cartao", "boleto", "pix", "berries"]
    opcao = opcao.lower().replace('ã', 'a')
    if not opcao or opcao not in opcoes_validas:
        return False, "Forma de pagamento inválida"
    return True, ""

def normalizar_chave(chave):
    return chave.lower().replace('ç', 'c').replace('ã', 'a').replace('é', 'e').replace(' ', '_')

def validar_formulario(dados):
    dados_normalizados = {normalizar_chave(k): v for k, v in dados.items()}
    
    validacoes = {
        'nome': validar_nome,
        'endereco': validar_endereco,
        'email': validar_email,
        'telefone': validar_telefone,
        'cep': validar_cep,
    }
    
    if dados_normalizados.get('user_type') == "Cliente":
        validacoes.update({
            'cpf': validar_cpf,
            'time': lambda x: validar_texto(x, "Time"),
            'one_piece': validar_one_piece
        })
    elif dados_normalizados.get('user_type') == "Fornecedor":
        validacoes.update({
            'cnpj': validar_cnpj,
            'setor': lambda x: validar_texto(x, "Setor")
        })
    elif dados_normalizados.get('user_type') == "Funcionário":
        validacoes.update({
            'cpf': validar_cpf,
            'cargo': lambda x: validar_texto(x, "Cargo"),
            'genero': validar_genero,
            'nascimento': validar_data_nascimento,
            'naturalidade': lambda x: validar_nome(x),
            'salario': validar_salario
        })
    
    erros = {}
    for campo, validador in validacoes.items():
        valor = dados_normalizados.get(campo)
        valido, mensagem = validador(valor)
        if not valido:
            erros[campo] = mensagem
    
    return len(erros) == 0, erros

def validar_pedido(dados):
    dados_normalizados = {normalizar_chave(k): v for k, v in dados.items()}
    
    validacoes = {
        'data_compra': validar_data,
        'cnpj': validar_cnpj, 
        'especie': lambda x: validar_texto(x, "Espécie"),
        'variedade': lambda x: validar_texto(x, "Variedade"),
        'quantidade': lambda x: validar_numero(x, "Quantidade"),
        'custo': lambda x: validar_numero(x, "Custo Unitário"),
        'preco': lambda x: validar_numero(x, "Preço"),
        'forma_pagamento': validar_forma_pagamento
    }
    
    erros = {}
    for campo, validador in validacoes.items():
        valor = dados_normalizados.get(campo)
        valido, mensagem = validador(valor)
        if not valido:
            erros[campo] = mensagem
    
    return len(erros) == 0, erros

def validar_venda(dados):
    dados_normalizados = {normalizar_chave(k): v for k, v in dados.items()}
    
    validacoes = {
        'data_compra': validar_data,
        'cpf': validar_cpf,
        'cnpj': validar_cnpj, 
    }
    
    erros = {}
    for campo, validador in validacoes.items():
        valor = dados_normalizados.get(campo)
        valido, mensagem = validador(valor)
        if not valido:
            erros[campo] = mensagem
    
    return len(erros) == 0, erros


