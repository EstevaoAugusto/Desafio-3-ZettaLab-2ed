[Inicio](../README.md) | [Data](../data/README.md) | [Features](../features/README.md) | **<u>Notebooks</u>** | [Scripts](../scripts/README.md) | [Reports](../reports/README.md) | [Interactive Reports](../interactive_reports/README.md) | [Dashboard](../dashboard/) | [Models](../models/README.md) | [Metrics](../metrics/README.md) | [API](../api/README.md)

# Notebooks Usados


## 1_pre_processamento.ipynb

Este notebook é responsável pela limpeza e padronização dos dados brutos recebidos via API e denúncias dos usuários. Ele lida com a tipagem das variáveis, tratamento de valores ausentes e a formatação rigorosa das coordenadas geográficas para garantir que a localização da ocorrência seja precisa. Aqui também é implementada a lógica de criptografia de senhas e segurança dos dados dos usuários.

## 2_eda.ipynb

Focado na Análise Exploratória de Dados, este notebook extrai os insights necessários para alimentar a Página de Histórico e os Indicadores da Home. Ele analisa a distribuição das queimadas por cidade no Norte de Minas, identifica a média de intensidade dos focos (baixa, média ou alta) e estuda o volume de denúncias ao longo do tempo (30, 60 e 90 dias) para validar os critérios de sucesso do monitoramento.

## 3_feature_engineering.ipynb

Este notebook cria as variáveis inteligentes que sustentam as regras de negócio do sistema. O destaque é a criação do algoritmo de Cluster de Mapa, que agrupa focos próximos para otimizar a visualização. Além disso, desenvolve a lógica de Validação Automática, que transforma denúncias individuais em um "alerta validado" caso três registros ocorram na mesma área, e calcula o Nível de Risco da região com base na densidade de focos ativos.

## 4_ai.ipynb

Destinado à inteligência analítica e modelos preditivos, este notebook processa o status das ocorrências e as imagens enviadas pelos usuários. Ele pode conter modelos para classificar automaticamente a intensidade do foco com base em evidências visuais ou prever a propagação do incêndio para auxiliar o Painel Operacional dos Bombeiros na tomada de decisão e priorização do atendimento.