# ⚡ PowerOn — Sistema de Gestão para Academia

Sistema de gestão para academia desenvolvido em **Python e Django**, utilizando **arquivos indexados** para persistência dos dados e **Árvore Binária de Busca (BST)** para indexação em memória.

O projeto foi desenvolvido como atividade acadêmica com o objetivo de aplicar conceitos de programação, estruturas de dados, persistência em arquivos e desenvolvimento web.

---

## 📋 Sobre o projeto

O **PowerOn** permite realizar o gerenciamento de uma academia por meio de uma interface web.

O sistema possui funcionalidades para:

- 👤 Gerenciamento de alunos;
- 👨‍🏫 Gerenciamento de professores;
- 🏋️ Gerenciamento de modalidades;
- 📋 Gerenciamento de matrículas;
- 📊 Relatório de faturamento;
- ⚖️ Cálculo de IMC;
- 🚦 Controle de limite de alunos por modalidade;
- 🔎 Busca utilizando índices em Árvore Binária;
- 💾 Persistência dos dados em arquivos `.dat`.

Os dados principais do sistema são armazenados em arquivos próprios, sem utilizar o Django ORM para essas entidades.

---

## 🎯 Objetivos

### Objetivo geral

Desenvolver um sistema de gestão para uma academia utilizando Python, Django, arquivos indexados e Árvore Binária de Busca.

### Objetivos específicos

- Implementar o cadastro de alunos;
- Implementar o cadastro de professores;
- Implementar o cadastro de modalidades;
- Implementar o cadastro de matrículas;
- Implementar operações de inclusão, consulta, alteração e exclusão;
- Armazenar os dados em arquivos `.dat`;
- Implementar índices utilizando Árvore Binária de Busca;
- Controlar o limite de alunos das modalidades;
- Calcular o IMC dos alunos;
- Exibir os relacionamentos entre as entidades;
- Gerar relatório de faturamento por modalidade.

---

## 🛠️ Tecnologias utilizadas

- **Python**
- **Django**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Arquivos binários `.dat`**
- **Árvore Binária de Busca**
- **Git e GitHub**

---

## 🏗️ Arquitetura do sistema

O projeto foi organizado separando as responsabilidades em diferentes camadas.

```text
┌─────────────────────────────┐
│       Interface Web         │
│      HTML / CSS / JS        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│            Views            │
│       Django Views          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          Services           │
│       Regras de negócio     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Persistência         │
│       Arquivos .dat         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Dados em disco        │
└─────────────────────────────┘