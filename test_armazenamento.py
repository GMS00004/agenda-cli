"""Testes unitários para o módulo armazenamento."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import armazenamento
from armazenamento import carregar_contatos, salvar_contatos


class BaseArmazenamentoTest(unittest.TestCase):
    """Redireciona ARQUIVO_CONTATOS para um diretório temporário."""

    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory()
        self._caminho = os.path.join(self._tempdir.name, "contatos.json")
        self._patch = patch.object(armazenamento, "ARQUIVO_CONTATOS", self._caminho)
        self._patch.start()

    def tearDown(self) -> None:
        self._patch.stop()
        self._tempdir.cleanup()

    def _escrever_conteudo_bruto(self, conteudo: str) -> None:
        with open(self._caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)

    def _escrever_json(self, dados: list[dict]) -> None:
        with open(self._caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False)

    def _ler_conteudo_bruto(self) -> str:
        with open(self._caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read()


class TestCarregarContatos(BaseArmazenamentoTest):
    def test_retorna_lista_vazia_quando_arquivo_inexiste(self) -> None:
        self.assertEqual(carregar_contatos(), [])

    def test_retorna_lista_vazia_quando_json_corrompido(self) -> None:
        self._escrever_conteudo_bruto("{ isto não é json válido")
        self.assertEqual(carregar_contatos(), [])

    def test_normaliza_contato_sem_campo_categoria(self) -> None:
        self._escrever_json(
            [
                {
                    "nome": "Antigo",
                    "telefone": "(11) 99999-0000",
                    "email": "antigo@example.com",
                }
            ]
        )
        contatos = carregar_contatos()
        self.assertEqual(contatos[0]["categoria"], "outros")

    def test_normaliza_categoria_invalida(self) -> None:
        self._escrever_json(
            [
                {
                    "nome": "VIP",
                    "telefone": "(11) 99999-0000",
                    "email": "vip@example.com",
                    "categoria": "vip",
                }
            ]
        )
        contatos = carregar_contatos()
        self.assertEqual(contatos[0]["categoria"], "outros")

    def test_preserva_categoria_valida(self) -> None:
        self._escrever_json(
            [
                {
                    "nome": "Mãe",
                    "telefone": "(11) 99999-0000",
                    "email": "mae@example.com",
                    "categoria": "família",
                }
            ]
        )
        contatos = carregar_contatos()
        self.assertEqual(contatos[0]["categoria"], "família")

    def test_canonicaliza_categoria_em_caixa_alta(self) -> None:
        self._escrever_json(
            [
                {
                    "nome": "Chefe",
                    "telefone": "(11) 99999-0000",
                    "email": "chefe@example.com",
                    "categoria": "TRABALHO",
                }
            ]
        )
        contatos = carregar_contatos()
        self.assertEqual(contatos[0]["categoria"], "trabalho")

    def test_normaliza_categoria_nao_string(self) -> None:
        self._escrever_json(
            [
                {
                    "nome": "Estranho",
                    "telefone": "(11) 99999-0000",
                    "email": "estranho@example.com",
                    "categoria": None,
                }
            ]
        )
        contatos = carregar_contatos()
        self.assertEqual(contatos[0]["categoria"], "outros")


class TestSalvarContatos(BaseArmazenamentoTest):
    def test_salva_com_indent_2(self) -> None:
        salvar_contatos(
            [
                {
                    "nome": "Ana",
                    "telefone": "(11) 99999-0000",
                    "email": "ana@example.com",
                    "categoria": "outros",
                }
            ]
        )
        conteudo = self._ler_conteudo_bruto()
        # indent=2: abertura da lista, dois espaços para o objeto interno,
        # e quatro espaços para as chaves do objeto.
        self.assertIn("[\n  {\n", conteudo)
        self.assertIn('\n    "nome": "Ana"', conteudo)
        # Garante que não foi salvo com indent=4 (regressão contra o valor antigo).
        self.assertNotIn('\n        "nome"', conteudo)

    def test_salva_preservando_acentos(self) -> None:
        salvar_contatos(
            [
                {
                    "nome": "João",
                    "telefone": "(11) 99999-0000",
                    "email": "joao@example.com",
                    "categoria": "família",
                }
            ]
        )
        conteudo = self._ler_conteudo_bruto()
        self.assertIn("João", conteudo)
        self.assertIn("família", conteudo)
        self.assertNotIn("\\u", conteudo)

    def test_roundtrip_salvar_e_carregar(self) -> None:
        original = [
            {
                "nome": "Ana",
                "telefone": "(11) 99999-0000",
                "email": "ana@example.com",
                "categoria": "trabalho",
                "cadastrado_em": "2026-04-23T12:00:00+00:00",
            }
        ]
        salvar_contatos(original)
        self.assertEqual(carregar_contatos(), original)


if __name__ == "__main__":
    unittest.main()
