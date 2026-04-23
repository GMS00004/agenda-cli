"""Módulo com as operações de gerenciamento de contatos."""

from armazenamento import salvar_contatos, carregar_contatos


def adicionar_contato(nome, telefone, email):
    # Adiciona um novo contato à agenda e persiste no arquivo
    contatos = carregar_contatos()
    novo_contato = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
    }
    contatos.append(novo_contato)
    salvar_contatos(contatos)
    return novo_contato


def listar_contatos():
    # Retorna todos os contatos cadastrados
    return carregar_contatos()


def buscar_contato(nome):
    # Busca contatos cujo nome contenha o termo informado (sem diferenciar maiúsculas)
    contatos = carregar_contatos()
    termo = nome.lower()
    return [c for c in contatos if termo in c["nome"].lower()]


def remover_contato(nome):
    # Remove o primeiro contato cujo nome corresponda exatamente ao informado
    contatos = carregar_contatos()
    for i, contato in enumerate(contatos):
        if contato["nome"].lower() == nome.lower():
            removido = contatos.pop(i)
            salvar_contatos(contatos)
            return removido
    return None
