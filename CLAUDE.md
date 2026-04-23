# Projeto: agenda-cli

Arquivo de contexto para Claude Code. Este projeto é uma agenda de contatos simples em Python, rodando via CLI.

---

## Stack
- Python 3.13
- Sem dependências externas (apenas biblioteca padrão)

## Convenções de código OBRIGATÓRIAS
- Todas as funções devem ter type hints completas (parâmetros e retorno)
- Todas as funções públicas devem ter docstring em português
- Nomes de variáveis e funções em português
- Indentação de 4 espaços, sem tabs

## Tratamento de erros
- Sempre tratar FileNotFoundError e JSONDecodeError no módulo armazenamento
- Validar entrada do usuário antes de salvar (não aceitar strings vazias)

## Testes
- Todo novo módulo de lógica deve ter um arquivo test_*.py correspondente
- Usar unittest (biblioteca padrão), não pytest

## Regras do projeto
- Nunca deletar contatos sem pedir confirmação interativa
- O arquivo contatos.json deve sempre ser salvo com indent=2 e ensure_ascii=False
- Mensagens para o usuário final sempre em português

## O que NÃO fazer
- Não adicionar bibliotecas externas sem discutir antes
- Não criar arquivos fora da pasta do projeto
