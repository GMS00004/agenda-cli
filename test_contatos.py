"""Testes unitários para o módulo contatos."""

import unittest
from datetime import datetime
from unittest.mock import patch

import contatos
from contatos import (
    adicionar_contato,
    buscar_contato,
    listar_contatos,
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
