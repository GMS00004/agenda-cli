"""Ponto de entrada da agenda-cli: menu interativo no terminal."""

from contatos import (
    CATEGORIAS_VALIDAS,
    adicionar_contato,
    buscar_contato,
    listar_contatos,
    listar_por_categoria,
    remover_contato,
)


def exibir_menu() -> None:
    """Imprime o menu principal da agenda."""
    print("\n=== Agenda CLI ===")
    print("1 - Adicionar contato")
    print("2 - Listar contatos")
    print("3 - Buscar contato")
    print("4 - Remover contato")
    print("5 - Listar por categoria")
    print("0 - Sair")


def exibir_contato(contato: dict) -> None:
    """Imprime os campos de um contato formatados para leitura."""
    print(f"- Nome: {contato['nome']}")
    print(f"  Telefone: {contato['telefone']}")
    print(f"  Email: {contato['email']}")
    print(f"  Categoria: {contato['categoria']}")


def _pedir_categoria() -> str:
    """Pede ao usuário que escolha uma categoria via submenu numerado.

    Mostra as quatro categorias oficiais e re-pergunta até receber uma
    escolha válida. Devolve a categoria na forma canônica (lowercase).
    """
    while True:
        print("\nEscolha a categoria:")
        for indice, nome in enumerate(CATEGORIAS_VALIDAS, start=1):
            print(f"{indice} - {nome}")
        escolha = input("Opção: ").strip()
        if escolha.isdigit():
            indice = int(escolha)
            if 1 <= indice <= len(CATEGORIAS_VALIDAS):
                return CATEGORIAS_VALIDAS[indice - 1]
        print("Opção inválida. Digite um número entre 1 e 4.")


def opcao_adicionar() -> None:
    """Lê os dados do usuário e adiciona um novo contato."""
    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()
    email = input("Email: ").strip()
    categoria = _pedir_categoria()
    adicionar_contato(nome, telefone, email, categoria)
    print("Contato adicionado com sucesso!")


def opcao_listar() -> None:
    """Exibe todos os contatos cadastrados."""
    contatos = listar_contatos()
    if not contatos:
        print("Nenhum contato cadastrado.")
        return
    print(f"\n{len(contatos)} contato(s) encontrado(s):")
    for contato in contatos:
        exibir_contato(contato)


def opcao_buscar() -> None:
    """Busca contatos pelo nome e imprime os resultados."""
    nome = input("Nome a buscar: ").strip()
    encontrados = buscar_contato(nome)
    if not encontrados:
        print("Nenhum contato encontrado.")
        return
    print(f"\n{len(encontrados)} resultado(s):")
    for contato in encontrados:
        exibir_contato(contato)


def opcao_remover() -> None:
    """Remove um contato pelo nome, após encontrá-lo."""
    nome = input("Nome do contato a remover: ").strip()
    removido = remover_contato(nome)
    if removido:
        print(f"Contato '{removido['nome']}' removido com sucesso.")
    else:
        print("Contato não encontrado.")


def opcao_listar_por_categoria() -> None:
    """Exibe os contatos de uma categoria escolhida pelo usuário."""
    categoria = _pedir_categoria()
    encontrados = listar_por_categoria(categoria)
    if not encontrados:
        print(f"Nenhum contato na categoria '{categoria}'.")
        return
    print(f"\n{len(encontrados)} contato(s) em '{categoria}':")
    for contato in encontrados:
        exibir_contato(contato)


def main() -> None:
    """Loop principal do menu até o usuário escolher sair."""
    acoes = {
        "1": opcao_adicionar,
        "2": opcao_listar,
        "3": opcao_buscar,
        "4": opcao_remover,
        "5": opcao_listar_por_categoria,
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
