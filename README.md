# ES-PI1-2026-T103-G01
# LAD.Py – Sistema de Votação Digital

Projeto Integrador I – Engenharia de Software  
PUC Campinas – 2026

---

## Descrição do Projeto

O **LAD.Py** é o backend de um sistema de votação digital. O projeto integra conhecimentos de **Lógica de Programação em Python**, **Manipulação de Bancos de Dados com SQL** e conceitos matemáticos de **Álgebra Linear** aplicados à proteção da informação.

O sistema é executado via terminal (linha de comando), sem interface gráfica, e contempla dois módulos principais:

- **Módulo de Gerenciamento:** cadastro, edição, remoção e listagem de eleitores e candidatos, com validação matemática de CPF e Título de Eleitor, geração de chave de acesso e criptografia de dados sensíveis.
- **Módulo de Votação:** abertura da urna, registro de votos, encerramento da votação, auditoria via logs de ocorrências e exibição de resultados.

---

## Integrantes

| Nome | GitHub |
|------|--------|
| *Bruno Lobo de Jesus* | *brunolobo-jesus* |
| *Cadu Martinez Spadari* | *Cadzss* |
| *Carlos Eduardo Marins Fonseca* | *Cadu-Marins* |
| *Gabriel Figueira Albasini* | *GabrielAlbasini* |
| *Leonardo Fonseca de Oliveira* | *leo-fonseca-oliveira* |



---

## Tecnologias Utilizadas

| Tecnologia / Ferramenta | Descrição |
|-------------------------|-----------|
| Python 3.x | Linguagem de programação principal |
| MySQL | Banco de dados relacional |
| mysql.connector | Biblioteca para conexão Python ↔ MySQL |
| datetime | Biblioteca para registro de data e hora |
| random, time, os | Bibliotecas auxiliares |
| Git + GitHub | Controle de versão e repositório |
| GitHub Projects | Gerenciamento de tarefas e apontamento de esforço |
| VSCode | IDE de desenvolvimento |

---

## Instruções para Execução do Sistema

### Pré-requisitos

- Python 3.x instalado
- MySQL instalado e em execução
- Biblioteca `mysql.connector` instalada:

```bash
pip install mysql-connector-python
```

### Configuração do Banco de Dados

1. Acesse o MySQL e crie o banco de dados do projeto:

```sql
CREATE DATABASE sistema_votacao;
```

2. Configure as credenciais de conexão no arquivo de configuração do projeto (host, usuário, senha e nome do banco).

### Executando o Sistema

1. Clone o repositório:

```bash
git clone https://github.com/GabrielAlbasini/ES-PI1-2026-T103-G01
cd ES-PI1-2026-T103-G01
```

2. Execute o arquivo principal:

```bash
python main.py
```

3. Ao iniciar, o sistema exibirá o menu principal com as opções:
   - **[1] Módulo de Gerenciamento** – cadastro e administração de eleitores e candidatos
   - **[2] Módulo de Votação** – abertura, votação, encerramento, auditoria e resultados

---
