"""Ponto de entrada da agenda-cli: menu interativo no terminal."""

from contatos import (
    adicionar_contato,
    listar_contatos,
    buscar_contato,
    remover_contato,
)


def exibir_menu():
    print("\n=== Agenda CLI ===")
    print("1 - Adicionar contato")
    print("2 - Listar contatos")
    print("3 - Buscar contato")
    print("4 - Remover contato")
    print("0 - Sair")


def exibir_contato(contato):
    print(f"- Nome: {contato['nome']}")
    print(f"  Telefone: {contato['telefone']}")
    print(f"  Email: {contato['email']}")


def opcao_adicionar():
    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()
    email = input("Email: ").strip()
    adicionar_contato(nome, telefone, email)
    print("Contato adicionado com sucesso!")


def opcao_listar():
    contatos = listar_contatos()
    if not contatos:
        print("Nenhum contato cadastrado.")
        return
    print(f"\n{len(contatos)} contato(s) encontrado(s):")
    for contato in contatos:
        exibir_contato(contato)


def opcao_buscar():
    nome = input("Nome a buscar: ").strip()
    encontrados = buscar_contato(nome)
    if not encontrados:
        print("Nenhum contato encontrado.")
        return
    print(f"\n{len(encontrados)} resultado(s):")
    for contato in encontrados:
        exibir_contato(contato)


def opcao_remover():
    nome = input("Nome do contato a remover: ").strip()
    removido = remover_contato(nome)
    if removido:
        print(f"Contato '{removido['nome']}' removido com sucesso.")
    else:
        print("Contato não encontrado.")


def main():
    # Loop principal do menu até o usuário escolher sair
    acoes = {
        "1": opcao_adicionar,
        "2": opcao_listar,
        "3": opcao_buscar,
        "4": opcao_remover,
    }

    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Encerrando a agenda. Até logo!")
            break

        acao = acoes.get(escolha)
        if acao:
            acao()
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
