# 💰 IntelliFinance – Sistema Interativo de Inteligência Financeira

O **IntelliFinance** é uma aplicação desenvolvida em **Python** utilizando **Streamlit** e **Plotly** para auxiliar no planejamento financeiro pessoal.

O sistema permite que o usuário insira informações sobre sua situação financeira atual, acompanhe indicadores importantes, simule cenários futuros e estime o tempo necessário para atingir metas financeiras.

Este projeto foi desenvolvido como complemento ao projeto **Plano de Inteligência Financeira**, agregando uma solução computacional interativa para apoio à tomada de decisão.

---

## 🚀 Funcionalidades

- 📋 Cadastro de renda mensal
- 💳 Cadastro de despesas por categoria
- 🏦 Cadastro de patrimônio inicial
- 📉 Cadastro de dívidas
- 🎯 Definição de metas financeiras
- 📈 Projeção patrimonial de curto, médio e longo prazo
- 📊 Dashboard interativo
- 💰 Cálculo automático de:
  - Saldo mensal
  - Taxa de poupança
  - Reserva financeira em meses
  - Endividamento relativo à renda
  - Score financeiro
- 📂 Upload de extrato CSV para categorização automática de gastos
- 📑 Exportação de projeções em CSV
- 📝 Geração automática de resumo para relatório

---

# 🖥️ Interface

O sistema é dividido em cinco módulos principais:

- 🏠 Visão Geral
- 📝 Entrada de Dados
- 📊 Análise de Gastos
- 📈 Projeções Financeiras
- 🎯 Metas e Recomendações

Cada módulo apresenta gráficos e indicadores atualizados automaticamente a partir dos dados informados pelo usuário.

---

# 📊 Indicadores Calculados

O sistema calcula automaticamente:

- Saldo mensal disponível
- Taxa de poupança
- Reserva financeira (em meses de despesas)
- Endividamento relativo à renda
- Participação dos gastos variáveis
- Score Financeiro (0–100)

---

# 📈 Projeções

A aplicação simula:

- Crescimento da renda;
- Crescimento das despesas;
- Evolução do patrimônio;
- Aportes mensais;
- Fluxo de caixa futuro;
- Prazo estimado para atingir metas financeiras.

---

# 🎯 Metas Financeiras

O usuário pode cadastrar metas como:

- Reserva de emergência;
- Viagem internacional;
- Compra de imóvel;
- Compra de veículo;
- Qualquer objetivo financeiro.

O sistema estima automaticamente o tempo necessário para atingir cada objetivo.

---

# 📂 Upload de Extrato Bancário

É possível importar um arquivo **CSV** contendo movimentações financeiras.

O sistema realiza uma categorização automática simples das transações por palavras-chave, gerando gráficos e análises dos gastos.

Categorias identificadas:

- Alimentação
- Transporte
- Compras Online
- Lazer
- Assinaturas
- Academia
- Outros

---

# 📚 Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Plotly

---

# 📦 Estrutura do Projeto

```text
IntelliFinance/
│
├── app.py
├── requirements.txt
├── README.md

```

---

# ▶️ Como executar

Clone o repositório:

```bash
git clone https://github.com/seuusuario/intellifinance.git
```

Entre na pasta:

```bash
cd intellifinance
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em:

```
http://localhost:8501
```

---

# 📋 Exemplo de Uso

1. Informe sua renda mensal;
2. Informe seu patrimônio atual;
3. Cadastre suas despesas;
4. Defina suas metas financeiras;
5. Execute a simulação;
6. Analise os gráficos e recomendações geradas.

---

# 📷 Exemplo de Dashboard

O dashboard apresenta:

- Indicadores financeiros;
- Distribuição dos gastos;
- Evolução patrimonial;
- Fluxo de caixa previsto;
- Progresso das metas;
- Recomendações automáticas.

---

# 🎓 Aplicação Acadêmica

Este sistema foi desenvolvido como solução computacional complementar ao projeto **Plano de Inteligência Financeira**, integrando conceitos de:

- Educação Financeira;
- Ciência de Dados;
- Visualização de Dados;
- Simulação Financeira;
- Desenvolvimento de Software.

---

# 👩‍💻 Autores

Projeto desenvolvido para a disciplina de **Planejamento Financeiro / Soluções Computacionais**.

Universidade Federal de Pernambuco (UFPE)

2026

---

# 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e educacionais.
