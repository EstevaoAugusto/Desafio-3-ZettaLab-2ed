[Inicio](./../README.md) | [Data](./../data/README.md) | [Features](./../features/README.md) | [Notebooks](./../notebooks/README.md) | [Scripts](./../scripts/README.md) | [Reports](./../reports/README.md) | [Interactive Reports](./../interactive_reports/README.md) | [Dashboard](./../dashboard/README.md) | [Models](./../models/README.md) | [Metrics](./../metrics/README.md) | **<u>API</u>**

# 🔥 API de Queimadas — LightGBM + FastAPI

API REST para análise de queimadas com Machine Learning.  
Suporta dois modelos LightGBM: **Classificação de Intensidade** e **Predição de Queimadas**.

---

## 📁 Estrutura do Projeto

```
api/
├── main.py               # Entry point — FastAPI + routers
├── config_path.py        # Caminhos que a API tem acesso
├── README.md
├── schemas/
│   ├── schemas.py        # Modelos Pydantic (request/response)
├── routers/
│   ├── dados.py          # /dados  — leitura de CSV/Parquet
│   ├── modelos.py        # /modelos — listagem e info dos .joblib
│   ├── predicao.py       # /predicao — inferência
│   └── metricas.py       # /metricas — avaliação de eficiência
└── services/
    ├── dados_service.py      # Lógica de leitura de arquivos
    ├── modelos_service.py    # Carregamento e cache de modelos
    ├── predicao_service.py   # Execução de predições
    └── metricas_service.py   # Cálculo de métricas
```

---


---

## Execução com Docker

Para executar a API em um ambiente containerizado, utilize o Docker Compose conforme descrito no [README principal](../README.md#execução-com-docker-recomendado).

### Passos Rápidos:
1. **Construir a imagem**:
   ```bash
   docker-compose build
   ```

2. **Subir os serviços**:
   ```bash
   docker-compose up
   ```

3. **Acessar a API**:
   - Documentação: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

### Notas:
- A API roda na porta 8000 dentro do container.
- Alterações no código são refletidas em tempo real devido aos volumes configurados (Hot Reload).
- Os modelos e dados são persistidos via volumes para manter consistência entre execuções.

---

## 📡 Endpoints

### Status
| Método | Rota      | Descrição         |
|--------|-----------|-------------------|
| GET    | `/`       | Status da API     |
| GET    | `/health` | Health check      |

### Dados (`/dados`)
| Método | Rota              | Descrição                              |
|--------|-------------------|----------------------------------------|
| GET    | `/dados/info`     | Metadados do dataset (linhas, colunas) |
| GET    | `/dados/amostra`  | Primeiras N linhas                     |
| GET    | `/dados/listar`   | Lista CSVs e Parquets de um diretório  |
| POST   | `/dados/upload`   | Upload de arquivo .csv ou .parquet     |

### Modelos (`/modelos`)
| Método | Rota               | Descrição                             |
|--------|--------------------|---------------------------------------|
| GET    | `/modelos/listar`  | Lista .joblib de um diretório         |
| GET    | `/modelos/info`    | Detalhes de um modelo específico      |
| DELETE | `/modelos/cache`   | Limpa modelos carregados em memória   |

### Predição (`/predicao`)
| Método | Rota                  | Descrição                              |
|--------|-----------------------|----------------------------------------|
| POST   | `/predicao/`          | Predição via JSON                      |
| GET    | `/predicao/arquivo`   | Predição a partir de arquivo local     |

### Métricas (`/metricas`)
| Método | Rota                  | Descrição                              |
|--------|-----------------------|----------------------------------------|
| POST   | `/metricas/avaliar`   | Avalia eficiência do modelo            |

---

## 📋 Exemplos de Uso

### 1. Informações do dataset
```bash
curl "http://localhost:8000/dados/info?\
caminho=/dados/queimadas_treino.csv&formato=csv"
```

### 2. Listar modelos disponíveis
```bash
curl "http://localhost:8000/modelos/listar?diretorio=/modelos"
```

### 3. Predição de intensidade (classificação)
```bash
curl -X POST "http://localhost:8000/predicao/?caminho_modelo=/modelos/lgbm_classificacao.joblib" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_modelo": "classificacao",
    "dados": [
      {"feature1": 0.5, "feature2": 120.3, "feature3": 35.1},
      {"feature1": 1.2, "feature2": 98.7,  "feature3": 28.4}
    ]
  }'
```

### 4. Avaliação de eficiência (regressão)
```bash
curl -X POST "http://localhost:8000/metricas/avaliar?caminho_modelo=/modelos/lgbm_regressao.joblib" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_modelo": "regressao",
    "coluna_alvo": "area_queimada",
    "dados": [
      {"feature1": 0.5, "feature2": 120.3, "area_queimada": 15.2},
      {"feature1": 1.2, "feature2": 98.7,  "area_queimada": 8.6}
    ]
  }'
```

---

## 📊 Métricas Retornadas

### Classificação (Intensidade de Queimadas)
- **Acurácia** — percentual de predições corretas
- **Precisão / Recall / F1** — balanceado por classes (weighted)
- **ROC-AUC** — área sob a curva ROC
- **Matriz de Confusão** — erros por classe
- **Relatório por Classe** — métricas individuais por intensidade

### Regressão (Predição de Queimadas)
- **MAE** — erro médio absoluto
- **MSE / RMSE** — erro quadrático médio e raiz
- **R²** — coeficiente de determinação
- **MAPE** — erro percentual médio absoluto

---

## ⚙️ Observações

- Os modelos ficam **em cache** após o primeiro carregamento (sem recarregar a cada requisição).
- Use `DELETE /modelos/cache` para liberar memória após trocar de modelo.
- O campo `tipo_modelo` aceita `"classificacao"` ou `"regressao"`.
- Arquivos Parquet requerem a biblioteca `pyarrow` instalada.