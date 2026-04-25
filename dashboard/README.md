[Inicio](../README.md) | [Data](../data/README.md) | [Features](../features/README.md) | [Notebooks](../notebooks/README.md) | [Scripts](../scripts/README.md) | [Reports](../reports/README.md) | [Interactive Reports](../interactive_reports/README.md) | **<u>Dashboard</u>** | [Models](../models/README.md) | [Metrics](../metrics/README.md) | [API](../api/README.md)

# 🖥️ MG Fire Intelligence Dashboard

Este diretório contém a interface visual interativa desenvolvida com **Dash (Plotly)**. O objetivo deste dashboard é centralizar os resultados da Análise Exploratória de Dados (EDA) e dos modelos de Machine Learning (LightGBM), permitindo uma visualização rápida e estratégica do risco de queimadas em Minas Gerais.

## 🚀 Como Iniciar o Dashboard

Para visualizar o painel interativo localmente, siga os passos abaixo:

### 1. Pré-requisitos

Certifique-se de que as dependências necessárias estão instaladas. Se ainda não instalou, execute o comando ```uv sync``` no diretório inicial do projeto.

### 2. Executação

Navegue até a pasta 'dashboard' e execute o comando abaixo:

```bash
python dashboard_base.py
```

### 3. Acesso

Após o comando, o terminal indicará que o servidor está rodando. Abra o seu navegador e acesse:

- ```http://127.0.0.1:8050/```

Caso queira acessar de forma online, o dashboard se encontra disponível no link abaixo:

- [Dashboard Integrado Queimadas](https://b626dd25-f7bd-4228-b435-1f6817531623.plotly.app/)

## O que este Dashboard monitora?

O painel foi desenhado para responder às três principais perguntas do projeto:

### 1. Indicadores de Performance (KPIs)

- Acurácia (R² de 0.65): Indica a confiabilidade do modelo de regressão.
- Erro Médio (MAE de 0.10): Mostra que a margem de erro na predição do índice de risco (0 a 1) é de apenas 10%.
- Ponto Crítico: Destaque para o mês de Setembro e para o bioma Cerrado.

### 2. Inteligência do Modelo (Feature Importance)

- Visualização clara de quais variáveis o modelo LightGBM mais valoriza para definir o risco.
- Geografia: Latitude e Longitude são os maiores preditores, provando a existência de "hotspots" recorrentes.
- Clima: Variáveis como DiaSemChuva e Precipitacao aparecem como gatilhos secundários importantes.

### 3. Dinâmica Temporal e de Solo

- Sazonalidade: Gráfico de barras destacando a explosão de área queimada no segundo semestre.
- Uso do Solo: Gráfico de rosca detalhando o impacto nas áreas de Agropecuária e Floresta.

### Central de Insights Integrada

Diferente de um dashboard estático, esta interface possui uma coluna dedicada a conclusões analíticas, traduzindo os gráficos em decisões:

- Priorização Geográfica: Foco em patrulhamento nas coordenadas identificadas como de alto risco.
- Prevenção Sazonal: Estratégias de combate intensificadas para a janela de Agosto-Outubro.
- Análise de Intensidade: Identificação de que o fogo em Setembro não é apenas mais frequente, mas 4x mais intenso.

## Tecnologias Utilizadas

- Python: Linguagem base.
- Dash: Framework para a estrutura web.
- Plotly: Engine para os gráficos interativos.
- Pandas: Manipulação dos dados processados.