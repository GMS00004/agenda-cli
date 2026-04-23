"""Módulo com as operações de gerenciamento de contatos."""

from datetime import datetime, timezone
from typing import Optional

from armazenamento import salvar_contatos, carregar_contatos
from utilidades import formatar_telefone


CATEGORIAS_VALIDAS: tuple[str, ...] = ("trabalho", "família", "amigos", "outros")
CATEGORIA_PADRAO: str = "outros"


def _validar_nome(nome: str) -> str:
    """Valida o nome informado e devolve a versão sem espaços nas pontas.

    Rejeita nomes vazios ou compostos apenas por espaços em branco.
    """
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise ValueError("O nome não pode ser vazio.")
    return nome_limpo


def _validar_email(email: str) -> str:
    """Valida o email informado e devolve a versão sem espaços nas pontas.

    O email deve conter '@' e pelo menos um '.' na parte do domínio
    (após o '@').
    """
    email_limpo = email.strip()
    if not email_limpo:
        raise ValueError("O email não pode ser vazio.")
    if "@" not in email_limpo:
        raise ValueError("O email deve conter '@'.")
    parte_local, _, dominio = email_limpo.partition("@")
    if not parte_local:
        raise ValueError("O email deve ter conteúdo antes do '@'.")
    if "." not in dominio:
        raise ValueError("O email deve conter pelo menos um '.' após o '@'.")
    return email_limpo


def _validar_categoria(categoria: str) -> str:
    """Valida a categoria e devolve a forma canônica (lowercase).

    Aceita qualquer combinação de caixa (ex.: "TRABALHO" vira "trabalho").
    Rejeita strings vazias ou valores fora de `CATEGORIAS_VALIDAS`.
    """
    categoria_limpa = categoria.strip().lower()
    if not categoria_limpa:
        raise ValueError("A categoria não pode ser vazia.")
    if categoria_limpa not in CATEGORIAS_VALIDAS:
        raise ValueError(
            "Categoria inválida. Use: trabalho, família, amigos ou outros."
        )
    return categoria_limpa


def adicionar_contato(
    nome: str,
    telefone: str,
    email: str,
    categoria: str = CATEGORIA_PADRAO,
) -> dict:
    """Adiciona um novo contato à agenda e persiste no arquivo.

    Valida os campos antes de salvar:
    - `nome`: não pode ser vazio (nem apenas espaços).
    - `telefone`: formatado por `utilidades.formatar_telefone`
      (requer exatamente 11 dígitos numéricos).
    - `email`: precisa conter '@' e pelo menos um '.' após o '@'.
    - `categoria`: precisa ser uma das quatro categorias oficiais
      (trabalho, família, amigos, outros). Default: "outros".

    Também registra o campo `cadastrado_em` com o timestamp ISO 8601
    (UTC) do momento de criação.
    """
    nome_validado = _validar_nome(nome)
    telefone_formatado = formatar_telefone(telefone)
    email_validado = _validar_email(email)
    categoria_validada = _validar_categoria(categoria)

    contatos = carregar_contatos()
    novo_contato = {
        "nome": nome_validado,
        "telefone": telefone_formatado,
        "email": email_validado,
        "categoria": categoria_validada,
        "cadastrado_em": datetime.now(timezone.utc).isoformat(),
    }
    contatos.append(novo_contato)
    salvar_contatos(contatos)
    return novo_contato


def listar_contatos() -> list[dict]:
    """Retorna todos os contatos cadastrados."""
    return carregar_contatos()


def buscar_contato(nome: str, categoria: Optional[str] = None) -> list[dict]:
    """Busca contatos cujo nome contenha o termo informado.

    A comparação por nome não diferencia maiúsculas de minúsculas e
    aceita correspondências parciais. Quando `categoria` é informada,
    também filtra os resultados por categoria (precisa ser uma das
    categorias oficiais, caso contrário levanta `ValueError`).
    """
    contatos = carregar_contatos()
    termo = nome.lower()
    resultados = [c for c in contatos if termo in c["nome"].lower()]
    if categoria is not None:
        categoria_validada = _validar_categoria(categoria)
        resultados = [c for c in resultados if c["categoria"] == categoria_validada]
    return resultados


def listar_por_categoria(categoria: str) -> list[dict]:
    """Retorna todos os contatos pertencentes à categoria informada.

    A categoria precisa ser uma das categorias oficiais (trabalho,
    família, amigos, outros); caso contrário, levanta `ValueError`.
    """
    categoria_validada = _validar_categoria(categoria)
    return [c for c in carregar_contatos() if c["categoria"] == categoria_validada]


def remover_contato(nome: str) -> Optional[dict]:
    """Remove o primeiro contato cujo nome corresponda ao informado.

    Retorna o contato removido, ou `None` caso nenhum seja encontrado.
    A comparação é feita sem diferenciar maiúsculas de minúsculas.
    """
    contatos = carregar_contatos()
    for i, contato in enumerate(contatos):
        if contato["nome"].lower() == nome.lower():
            removido = contatos.pop(i)
            salvar_contatos(contatos)
            return removido
    return None
