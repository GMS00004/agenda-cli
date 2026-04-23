"""Módulo responsável por salvar e carregar contatos em arquivo JSON."""

import json
import os

ARQUIVO_CONTATOS: str = "contatos.json"

_CATEGORIAS_VALIDAS: tuple[str, ...] = ("trabalho", "família", "amigos", "outros")
_CATEGORIA_PADRAO: str = "outros"


def salvar_contatos(contatos: list[dict]) -> None:
    """Grava a lista de contatos no arquivo JSON.

    Usa indentação de 2 espaços e preserva caracteres acentuados
    (ensure_ascii=False) para manter a legibilidade do arquivo.
    """
    with open(ARQUIVO_CONTATOS, "w", encoding="utf-8") as arquivo:
        json.dump(contatos, arquivo, indent=2, ensure_ascii=False)


def carregar_contatos() -> list[dict]:
    """Lê os contatos do arquivo JSON e devolve uma lista.

    Retorna lista vazia se o arquivo ainda não existir ou se estiver
    corrompido (JSON inválido). Também aplica normalização do campo
    `categoria` para garantir retrocompatibilidade: contatos antigos
    sem o campo, ou com valor fora das categorias oficiais, passam a
    ter `"outros"`. A normalização acontece apenas em memória — o
    arquivo só é reescrito em operações de salvamento normais.
    """
    if not os.path.exists(ARQUIVO_CONTATOS):
        return []

    try:
        with open(ARQUIVO_CONTATOS, "r", encoding="utf-8") as arquivo:
            contatos = json.load(arquivo)
    except json.JSONDecodeError:
        return []

    for contato in contatos:
        categoria_atual = contato.get("categoria")
        if isinstance(categoria_atual, str):
            categoria_normalizada = categoria_atual.strip().lower()
            if categoria_normalizada in _CATEGORIAS_VALIDAS:
                contato["categoria"] = categoria_normalizada
                continue
        contato["categoria"] = _CATEGORIA_PADRAO

    return contatos
