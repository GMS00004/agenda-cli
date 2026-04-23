# Agenda CLI

Uma agenda de contatos simples, executada via linha de comando, escrita em Python puro (sem dependências externas).

## Funcionalidades

- Adicionar contato (nome, telefone, email e categoria)
- Listar todos os contatos cadastrados
- Buscar contatos pelo nome (com filtro opcional por categoria via API)
- Remover contato pelo nome
- Listar contatos filtrando por categoria
- Persistência automática em arquivo `contatos.json`

## Estrutura do projeto

```
agenda-cli/
├── main.py              # Ponto de entrada e menu interativo
├── contatos.py          # Operações sobre contatos (CRUD) e validação
├── armazenamento.py     # Leitura e gravação do arquivo JSON
├── utilidades.py        # Funções auxiliares (ex.: formatação de telefone)
├── test_contatos.py     # Testes de contatos.py
├── test_armazenamento.py# Testes de armazenamento.py
├── test_utilidades.py   # Testes de utilidades.py
├── contatos.json        # Banco de dados local (criado automaticamente)
└── README.md
```

## Como executar

Requer Python 3.9 ou superior (usa `list[dict]` e `tuple[str, ...]` nativos).

```bash
python main.py
```

Ao iniciar, um menu numerado será exibido no terminal. Basta digitar a opção desejada e seguir as instruções.

## Rodando os testes

```bash
python -m unittest discover -v
```

## Categorias

Cada contato pertence a uma das quatro categorias oficiais:

- `trabalho`
- `família`
- `amigos`
- `outros` (padrão)

Ao adicionar um contato, o menu apresenta um submenu numerado (1 a 4) para escolha da categoria, evitando ambiguidade de acentuação ou caixa.

### Retrocompatibilidade

Contatos pré-existentes em `contatos.json` que **não** tenham o campo `categoria`, ou que tenham um valor fora das quatro categorias oficiais, são automaticamente tratados como `"outros"` ao serem carregados. O arquivo só é reescrito com o campo corrigido na próxima operação de salvamento (adicionar ou remover contato).

## Formato dos dados

Cada contato é armazenado como um objeto JSON:

```json
{
  "nome": "Maria Silva",
  "telefone": "(11) 99999-0000",
  "email": "maria@example.com",
  "categoria": "trabalho",
  "cadastrado_em": "2026-04-23T12:34:56+00:00"
}
```

O arquivo é salvo com indentação de 2 espaços e preserva caracteres acentuados (`ensure_ascii=False`).

## Autor
Projeto desenvolvido como exercício de aprendizado de Claude Code por Guilherme.
