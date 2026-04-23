import unittest

from utilidades import formatar_telefone


class TestFormatarTelefone(unittest.TestCase):
    def test_formata_celular_valido(self) -> None:
        self.assertEqual(formatar_telefone("11999990000"), "(11) 99999-0000")

    def test_formata_outro_ddd(self) -> None:
        self.assertEqual(formatar_telefone("21987654321"), "(21) 98765-4321")

    def test_rejeita_string_vazia(self) -> None:
        with self.assertRaises(ValueError):
            formatar_telefone("")

    def test_rejeita_nao_digitos(self) -> None:
        with self.assertRaises(ValueError):
            formatar_telefone("11abcdefghi")

    def test_rejeita_com_mascara(self) -> None:
        with self.assertRaises(ValueError):
            formatar_telefone("(11) 99999-0000")

    def test_rejeita_menos_de_11_digitos(self) -> None:
        with self.assertRaises(ValueError):
            formatar_telefone("1199990000")

    def test_rejeita_mais_de_11_digitos(self) -> None:
        with self.assertRaises(ValueError):
            formatar_telefone("119999900000")


if __name__ == "__main__":
    unittest.main()
