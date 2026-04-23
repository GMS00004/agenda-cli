def formatar_telefone(digitos: str) -> str:
    """Formata um número de telefone brasileiro no padrão (XX) XXXXX-XXXX.

    Recebe uma string contendo apenas 11 dígitos (DDD + 9 dígitos do número)
    e devolve a representação formatada.
    """
    if not digitos:
        raise ValueError("O número de telefone não pode ser vazio.")
    if not digitos.isdigit():
        raise ValueError("O número de telefone deve conter apenas dígitos.")
    if len(digitos) != 11:
        raise ValueError("O número de telefone deve conter exatamente 11 dígitos.")

    ddd = digitos[0:2]
    prefixo = digitos[2:7]
    sufixo = digitos[7:11]
    return f"({ddd}) {prefixo}-{sufixo}"
