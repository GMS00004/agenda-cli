"""Módulo responsável por salvar e carregar contatos em arquivo JSON."""

import json
import os

ARQUIVO_CONTATOS = "contatos.json"


def salvar_contatos(contatos):
    # Grava a lista de contatos no arquivo JSON com indentação legível
    with open(ARQUIVO_CONTATOS, "w", encoding="utf-8") as arquivo:
        json.dump(contatos, arquivo, indent=4, ensure_ascii=False)


def carregar_contatos():
    # Retorna lista vazia caso o arquivo ainda não exista
    if not os.path.exists(ARQUIVO_CONTATOS):
        return []

    with open(ARQUIVO_CONTATOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
