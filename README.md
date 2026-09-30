# ⚡ PowerOn — Sistema de Gestão para Academia

Sistema web desenvolvido para gerenciamento de uma academia, permitindo controlar alunos, professores, modalidades e matrículas, além de disponibilizar consultas, cálculo de IMC e relatório de faturamento.

O projeto foi desenvolvido utilizando **Python e Django**, com uma arquitetura baseada em **arquivos indexados**, utilizando arquivos `.dat` para persistência dos dados e uma **Árvore Binária de Busca (ABB/BST)** mantida em memória para indexação e localização dos registros.

---

## 📋 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Objetivos](#-objetivos)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do sistema](#-arquitetura-do-sistema)
- [Estrutura de diretórios](#-estrutura-de-diretórios)
- [Entidades do sistema](#-entidades-do-sistema)
- [Arquivos indexados](#-arquivos-indexados)
- [Árvore Binária de Busca](#-árvore-binária-de-busca)
- [Persistência dos dados](#-persistência-dos-dados)
- [Regras de negócio](#-regras-de-negócio)
- [Cálculo de IMC](#-cálculo-de-imc)
- [Faturamento](#-faturamento)
- [Fluxo da aplicação](#-fluxo-da-aplicação)
- [Camadas do sistema](#-camadas-do-sistema)
- [Interface](#-interface)
- [Responsividade](#-responsividade)
- [Instalação](#-instalação)
- [Configuração do ambiente](#-configuração-do-ambiente)
- [Execução](#-execução)
- [Testes](#-testes)
- [Decisões de projeto](#-decisões-de-projeto)
- [Integridade dos dados](#-integridade-dos-dados)
- [Desafios encontrados](#-desafios-encontrados)
- [Possíveis melhorias](#-possíveis-melhorias)
- [Objetivo acadêmico](#-objetivo-acadêmico)
- [Autora](#-autora)

---

# 📌 Sobre o projeto

O **PowerOn** é um sistema web de gerenciamento de academia desenvolvido como projeto acadêmico.

A aplicação foi construída com o framework **Django**, utilizando **Python** como linguagem principal.

Um dos principais requisitos do projeto é a implementação de uma estrutura de **arquivos indexados**, na qual:

- os registros são armazenados em arquivos `.dat`;
- os dados permanecem armazenados no disco mesmo após o encerramento da aplicação;
- uma Árvore Binária de Busca é utilizada como estrutura de índice;
- a árvore permanece em memória durante a execução;
- o índice é reconstruído a partir dos registros armazenados quando a aplicação é iniciada;
- a posição física do registro no arquivo é utilizada para localizar o dado.

O projeto não utiliza o banco de dados relacional como mecanismo principal para armazenamento das entidades acadêmicas exigidas.

---

# 🎯 Objetivos

## Objetivo geral

Desenvolver um sistema web para gerenciamento de uma academia, permitindo controlar seus principais cadastros e operações administrativas por meio de uma interface simples e organizada.

## Objetivos específicos

- Cadastrar alunos;
- Consultar alunos;
- Alterar dados dos alunos;
- Excluir alunos;
- Cadastrar professores;
- Consultar professores;
- Alterar professores;
- Excluir professores;
- Cadastrar modalidades;
- Consultar modalidades;
- Alterar modalidades;
- Excluir modalidades;
- Realizar matrículas;
- Alterar matrículas;
- Excluir matrículas;
- Controlar o limite de alunos das modalidades;
- Controlar o total de alunos matriculados em cada modalidade;
- Calcular o IMC dos alunos;
- Apresentar o diagnóstico relacionado ao IMC;
- Gerar relatório de faturamento por modalidade;
- Utilizar arquivos indexados;
- Utilizar uma Árvore Binária de Busca como índice;
- Manter os dados persistentes em arquivos.

---

# 🚀 Funcionalidades

## 👤 Alunos

O sistema permite:

- Cadastro;
- Listagem;
- Consulta individual;
- Edição;
- Exclusão;
- Cálculo de IMC;
- Diagnóstico do IMC.

Os dados armazenados são:

| Campo | Descrição |
|---|---|
| Código | Identificador único do aluno |
| Nome | Nome completo |
| Data de nascimento | Data de nascimento |
| Peso | Peso do aluno |
| Altura | Altura do aluno |

---

## 👨‍🏫 Professores

O sistema permite:

- Cadastro;
- Listagem;
- Consulta;
- Edição;
- Exclusão.

Dados:

| Campo | Descrição |
|---|---|
| Código | Identificador do professor |
| Nome | Nome do professor |
| Endereço | Endereço |
| Telefone | Telefone |

---

## 🏋️ Modalidades

O sistema permite:

- Cadastro;
- Listagem;
- Consulta;
- Edição;
- Exclusão;
- Associação com professor;
- Controle de limite de alunos;
- Controle do total de alunos matriculados.

Dados:

| Campo | Descrição |
|---|---|
| Código da modalidade | Identificador |
| Descrição | Nome/descrição da modalidade |
| Código do professor | Professor responsável |
| Valor da aula | Valor cobrado por aula |
| Limite de alunos | Número máximo de alunos |
| Total de alunos | Quantidade atual de alunos |

Na interface, quando o código do professor é utilizado, o sistema também pode apresentar o **nome do professor associado**.

---

## 📋 Matrículas

O sistema permite:

- Cadastro;
- Listagem;
- Consulta;
- Edição;
- Exclusão;
- Controle de vagas;
- Associação entre aluno e modalidade;
- Controle da quantidade de aulas.

Dados:

| Campo | Descrição |
|---|---|
| Código da matrícula | Identificador |
| Código do aluno | Aluno matriculado |
| Código da modalidade | Modalidade escolhida |
| Quantidade de aulas | Quantidade de aulas contratadas |

Na interface, os códigos relacionados podem ser apresentados juntamente com suas respectivas descrições:

- Código do aluno → nome do aluno;
- Código da modalidade → descrição da modalidade.

---

# 🗂️ Arquivos indexados

Uma das principais características do PowerOn é a utilização de **arquivos indexados**.

Cada entidade possui seu próprio arquivo de dados.

```text
dados/
├── alunos.dat
├── professores.dat
├── modalidades.dat
└── matriculas.dat