"""Testes unitários para o módulo contatos."""

import unittest
from datetime import datetime
from unittest.mock import patch

import contatos
from contatos import (
    adicionar_contato,
    buscar_contato,
    listar_contatos,
    listar_por_categoria,
    remover_contato,
)


class ArmazenamentoEmMemoria:
    """Substitui `salvar_contatos` e `carregar_contatos` por uma lista em memória.

    Evita que os testes toquem o arquivo `contatos.json` real.
    """

    def __init__(self, inicial: list[dict] | None = None) -> None:
        self.dados: list[dict] = list(inicial) if inicial else []

    def carregar(self) -> list[dict]:
        return list(self.dados)

    def salvar(self, contatos_novos: list[dict]) -> None:
        self.dados = list(contatos_novos)


class BaseContatosTest(unittest.TestCase):
    """Configura um armazenamento em memória para cada teste."""

    def setUp(self) -> None:
        self.storage = ArmazenamentoEmMemoria()
        self._patches = [
            patch.object(contatos, "carregar_contatos", side_effect=self.storage.carregar),
            patch.object(contatos, "salvar_contatos", side_effect=self.storage.salvar),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()


class TestAdicionarContato(BaseContatosTest):
    def test_adiciona_contato_valido(self) -> None:
        contato = adicionar_contato("Maria Silva", "11999990000", "maria@example.com")
        self.assertEqual(contato["nome"], "Maria Silva")
        self.assertEqual(contato["telefone"], "(11) 99999-0000")
        self.assertEqual(contato["email"], "maria@example.com")
        self.assertEqual(contato["categoria"], "outros")
        self.assertEqual(self.storage.dados, [contato])

    def test_registra_cadastrado_em_como_iso_8601(self) -> None:
        contato = adicionar_contato("Ana", "11999990000", "ana@example.com")
        self.assertIn("cadastrado_em", contato)
        # `fromisoformat` lança ValueError se o formato não for ISO 8601.
        datetime.fromisoformat(contato["cadastrado_em"])

    def test_remove_espacos_em_branco_nas_pontas(self) -> None:
        contato = adicionar_contato("  João  ", "11999990000", "  joao@example.com  ")
        self.assertEqual(contato["nome"], "João")
        self.assertEqual(contato["email"], "joao@example.com")

    def test_rejeita_nome_vazio(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("", "11999990000", "joao@example.com")

    def test_rejeita_nome_somente_espacos(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("    ", "11999990000", "joao@example.com")

    def test_rejeita_telefone_com_letras(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("João", "11abcdefghi", "joao@example.com")

    def test_rejeita_telefone_com_menos_de_11_digitos(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("João", "1199999", "joao@example.com")

    def test_rejeita_telefone_ja_formatado(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("João", "(11) 99999-0000", "joao@example.com")

    def test_rejeita_email_sem_arroba(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("João", "11999990000", "joaoexample.com")

    def test_rejeita_email_sem_ponto_apos_arroba(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("João", "11999990000", "joao@examplecom")

    def test_rejeita_email_vazio(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("João", "11999990000", "")

    def test_rejeita_email_sem_parte_local(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("João", "11999990000", "@example.com")

    def test_nao_persiste_quando_validacao_falha(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato("", "11999990000", "joao@example.com")
        self.assertEqual(self.storage.dados, [])

    def test_categoria_padrao_e_outros(self) -> None:
        contato = adicionar_contato("Ana", "11999990000", "ana@example.com")
        self.assertEqual(contato["categoria"], "outros")

    def test_adiciona_com_categoria_trabalho(self) -> None:
        contato = adicionar_contato(
            "Ana", "11999990000", "ana@example.com", categoria="trabalho"
        )
        self.assertEqual(contato["categoria"], "trabalho")
        self.assertEqual(self.storage.dados[0]["categoria"], "trabalho")

    def test_categoria_case_insensitive(self) -> None:
        contato = adicionar_contato(
            "Ana", "11999990000", "ana@example.com", categoria="TRABALHO"
        )
        self.assertEqual(contato["categoria"], "trabalho")

    def test_categoria_familia_com_acento(self) -> None:
        contato = adicionar_contato(
            "Ana", "11999990000", "ana@example.com", categoria="família"
        )
        self.assertEqual(contato["categoria"], "família")

    def test_rejeita_categoria_invalida(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato(
                "Ana", "11999990000", "ana@example.com", categoria="vip"
            )
        self.assertEqual(self.storage.dados, [])

    def test_rejeita_categoria_vazia(self) -> None:
        with self.assertRaises(ValueError):
            adicionar_contato(
                "Ana", "11999990000", "ana@example.com", categoria=""
            )

    def test_rejeita_familia_sem_acento(self) -> None:
        # Sem acento não é aceito: o menu numerado evita essa entrada,
        # mas a API deve continuar rigorosa com os valores oficiais.
        with self.assertRaises(ValueError):
            adicionar_contato(
                "Ana", "11999990000", "ana@example.com", categoria="familia"
            )


class TestListarContatos(BaseContatosTest):
    def test_lista_vazia_quando_sem_contatos(self) -> None:
        self.assertEqual(listar_contatos(), [])

    def test_lista_todos_contatos(self) -> None:
        adicionar_contato("Ana", "11999990000", "ana@example.com")
        adicionar_contato("Bruno", "21987654321", "bruno@example.com")
        resultado = listar_contatos()
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]["nome"], "Ana")
        self.assertEqual(resultado[1]["nome"], "Bruno")


class TestBuscarContato(BaseContatosTest):
    def setUp(self) -> None:
        super().setUp()
        adicionar_contato("Maria Silva", "11999990000", "maria@example.com")
        adicionar_contato("João Souza", "21987654321", "joao@example.com")
        adicionar_contato("Mariana Costa", "31988887777", "mariana@example.com")

    def test_busca_retorna_correspondencias_parciais(self) -> None:
        resultado = buscar_contato("mari")
        nomes = [c["nome"] for c in resultado]
        self.assertIn("Maria Silva", nomes)
        self.assertIn("Mariana Costa", nomes)
        self.assertNotIn("João Souza", nomes)

    def test_busca_sem_diferenciar_maiusculas(self) -> None:
        resultado = buscar_contato("JOÃO")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["nome"], "João Souza")

    def test_busca_sem_correspondencia_retorna_lista_vazia(self) -> None:
        self.assertEqual(buscar_contato("Pedro"), [])


class TestBuscarPorCategoria(BaseContatosTest):
    def setUp(self) -> None:
        super().setUp()
        adicionar_contato(
            "Ana Silva", "11999990000", "ana@example.com", categoria="trabalho"
        )
        adicionar_contato(
            "Ana Costa", "21987654321", "ana.c@example.com", categoria="amigos"
        )
        adicionar_contato(
            "Bruno", "31988887777", "bruno@example.com", categoria="trabalho"
        )

    def test_filtra_por_categoria(self) -> None:
        resultado = buscar_contato("ana", categoria="trabalho")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["nome"], "Ana Silva")

    def test_sem_filtro_mantem_comportamento_antigo(self) -> None:
        resultado = buscar_contato("ana")
        nomes = [c["nome"] for c in resultado]
        self.assertIn("Ana Silva", nomes)
        self.assertIn("Ana Costa", nomes)

    def test_filtro_com_categoria_case_insensitive(self) -> None:
        resultado = buscar_contato("ana", categoria="TRABALHO")
        self.assertEqual(len(resultado), 1)

    def test_categoria_invalida_levanta_erro(self) -> None:
        with self.assertRaises(ValueError):
            buscar_contato("ana", categoria="vip")

    def test_busca_sem_resultados_na_categoria(self) -> None:
        self.assertEqual(buscar_contato("ana", categoria="família"), [])


class TestListarPorCategoria(BaseContatosTest):
    def setUp(self) -> None:
        super().setUp()
        adicionar_contato(
            "Ana", "11999990000", "ana@example.com", categoria="trabalho"
        )
        adicionar_contato(
            "Bruno", "21987654321", "bruno@example.com", categoria="amigos"
        )
        adicionar_contato(
            "Carla", "31988887777", "carla@example.com", categoria="trabalho"
        )

    def test_retorna_apenas_da_categoria(self) -> None:
        resultado = listar_por_categoria("trabalho")
        nomes = [c["nome"] for c in resultado]
        self.assertEqual(sorted(nomes), ["Ana", "Carla"])

    def test_categoria_sem_contatos_retorna_lista_vazia(self) -> None:
        self.assertEqual(listar_por_categoria("família"), [])

    def test_categoria_invalida_levanta_erro(self) -> None:
        with self.assertRaises(ValueError):
            listar_por_categoria("vip")

    def test_aceita_categoria_em_caixa_diferente(self) -> None:
        resultado = listar_por_categoria("TRABALHO")
        self.assertEqual(len(resultado), 2)


class TestRemoverContato(BaseContatosTest):
    def test_remove_contato_existente(self) -> None:
        adicionar_contato("Ana", "11999990000", "ana@example.com")
        adicionar_contato("Bruno", "21987654321", "bruno@example.com")
        removido = remover_contato("Ana")
        self.assertIsNotNone(removido)
        self.assertEqual(removido["nome"], "Ana")
        self.assertEqual(len(self.storage.dados), 1)
        self.assertEqual(self.storage.dados[0]["nome"], "Bruno")

    def test_remove_sem_diferenciar_maiusculas(self) -> None:
        adicionar_contato("Ana", "11999990000", "ana@example.com")
        removido = remover_contato("ANA")
        self.assertIsNotNone(removido)
        self.assertEqual(self.storage.dados, [])

    def test_remover_inexistente_retorna_none(self) -> None:
        adicionar_contato("Ana", "11999990000", "ana@example.com")
        self.assertIsNone(remover_contato("Pedro"))
        self.assertEqual(len(self.storage.dados), 1)


if __name__ == "__main__":
    unittest.main()
