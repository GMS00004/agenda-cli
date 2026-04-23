# Agenda CLI

Uma agenda de contatos simples, executada via linha de comando, escrita em Python puro (sem dependências externas).

## Funcionalidades

- Adicionar contato (nome, telefone e email)
- Listar todos os contatos cadastrados
- Buscar contatos pelo nome
- Remover contato pelo nome
- Persistência automática em arquivo `contatos.json`

## Estrutura do projeto

```
agenda-cli/
├── main.py            # Ponto de entrada e menu interativo
├── contatos.py        # Operações sobre contatos (CRUD)
├── armazenamento.py   # Leitura e gravação do arquivo JSON
├── contatos.json      # Banco de dados local (criado automaticamente)
└── README.md
```

## Como executar

Requer Python 3.7 ou superior.

```bash
python main.py
```

Ao iniciar, um menu numerado será exibido no terminal. Basta digitar a opção desejada e seguir as instruções.

## Formato dos dados

Cada contato é armazenado como um objeto JSON:

```json
{
    "nome": "Maria Silva",
    "telefone": "(11) 99999-0000",
    "email": "maria@example.com"
}
```

## Autor
Projeto desenvolvido como exercício de aprendizado de Claude Code por Guilherme.