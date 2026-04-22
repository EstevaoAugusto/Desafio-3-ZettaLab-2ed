from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict, Union
from enum import Enum
from pathlib import Path

# ──────────────────────────────────────────────
#  Enums
# ──────────────────────────────────────────────
class TipoModelo(str, Enum):
    classificacao = "classificacao"   # Classificação de Intensidade de Queimadas
    regressao     = "regressao"       # Predição de Queimadas


# ──────────────────────────────────────────────
#  Colunas do dataset fixo
# ──────────────────────────────────────────────
COLUNAS_DATASET = [
    "DataHora", "Satelite", "Pais", "Nome_UF", "Nome_Município",
    "Bioma", "DiaSemChuva", "Precipitacao", "RiscoFogo", "FRP",
    "Latitude", "Longitude", "Data", "Hora", "Ano", "Mes", "Dia",
    "Hora_decimal", "ID_UF", "ID_Município",
]

# Features numéricas usadas pelos modelos LightGBM
FEATURES_NUMERICAS = [
    "DiaSemChuva", "Precipitacao", "RiscoFogo", "FRP",
    "Latitude", "Longitude", "Ano", "Mes", "Dia",
    "Hora_decimal", "ID_UF", "ID_Município",
]

# Features categóricas
FEATURES_CATEGORICAS = [
    "Satelite", "Pais", "Nome_UF", "Nome_Município", "Bioma",
]

class FormatoArquivo(str, Enum):
    csv = "csv"
    parquet = "parquet"

# ──────────────────────────────────────────────
#  Dados
# ──────────────────────────────────────────────
class InfoDataset(BaseModel):
    nome:              str
    caminho:           Union[str, Path]
    linhas:            int
    colunas:           int
    tamanho_mb:        float
    colunas_nomes:     List[str]
    nulos_por_coluna:  Dict[str, int]
    periodo_inicio:    Optional[str] = None   # min de DataHora
    periodo_fim:       Optional[str] = None   # max de DataHora
    biomas_presentes:  Optional[List[str]] = None
    ufs_presentes:     Optional[List[str]] = None

    model_config = {"from_attributes": True}


class AmostraDataset(BaseModel):
    colunas:      List[str]
    dados:        List[Dict[str, Any]]
    total_linhas: int


class FiltrosDataset(BaseModel):
    """Parâmetros opcionais para filtrar o dataset antes de retornar."""
    ano:       Optional[int]   = Field(None, description="Filtrar por ano (ex: 2023)")
    mes:       Optional[int]   = Field(None, ge=1, le=12, description="Filtrar por mês (1-12)")
    bioma:     Optional[str]   = Field(None, description="Ex: 'Amazônia', 'Cerrado'")
    nome_uf:   Optional[str]   = Field(None, description="Ex: 'Mato Grosso'")
    risco_fogo_min: Optional[float] = Field(None, description="RiscoFogo mínimo")
    risco_fogo_max: Optional[float] = Field(None, description="RiscoFogo máximo")
    n_linhas:  int             = Field(100, ge=1, le=5000, description="Máx. de linhas retornadas")


# ──────────────────────────────────────────────
#  Modelos
# ──────────────────────────────────────────────
class InfoModelo(BaseModel):
    nome:           str
    tipo:           TipoModelo
    caminho:        Union[str, Path]
    tamanho_mb:     float
    num_features:   Optional[int]       = None
    feature_names:  Optional[List[str]] = None
    num_classes:    Optional[int]       = None   # só classificação
    classes:        Optional[List[Any]] = None   # só classificação

    model_config = {"from_attributes": True}


class ListaModelos(BaseModel):
    total:   int
    modelos: List[InfoModelo]


# ──────────────────────────────────────────────
#  Predição
# ──────────────────────────────────────────────
class EntradaPredicao(BaseModel):
    tipo_modelo: TipoModelo = Field(
        ...,
        description="'classificacao' = intensidade de queimadas | 'regressao' = predição de queimadas",
    )
    dados: List[Dict[str, Any]] = Field(
        ...,
        description=(
            "Lista de registros com as features do modelo. "
            f"Features numéricas esperadas: {FEATURES_NUMERICAS}"
        ),
    )


class ResultadoPredicao(BaseModel):
    tipo_modelo:    TipoModelo
    total_linhas:   int
    predicoes:      List[Any]
    probabilidades: Optional[List[List[float]]] = None  # só classificação
    classes:        Optional[List[str]]         = None  # só classificação


# ──────────────────────────────────────────────
#  Métricas
# ──────────────────────────────────────────────
class MetricasClassificacao(BaseModel):
    acuracia:          float
    precisao:          float
    recall:            float
    f1_score:          float
    roc_auc:           Optional[float]    = None
    matriz_confusao:   List[List[int]]
    relatorio_classes: Dict[str, Any]


class MetricasRegressao(BaseModel):
    mae:  float
    mse:  float
    rmse: float
    r2:   float
    mape: Optional[float] = None


class ResultadoMetricas(BaseModel):
    tipo_modelo:    TipoModelo
    modelo_arquivo: str
    metricas:       Dict[str, Any]


class EntradaAvaliacao(BaseModel):
    tipo_modelo:  TipoModelo
    coluna_alvo:  str = Field(
        ...,
        description="Nome da coluna com os valores reais (y_true). Ex: 'FRP' para regressão.",
    )
    dados: List[Dict[str, Any]] = Field(
        ...,
        description="Registros com features + coluna alvo.",
    )


# ──────────────────────────────────────────────
#  Respostas genéricas
# ──────────────────────────────────────────────
class Sucesso(BaseModel):
    mensagem: str

class Erro(BaseModel):
    detalhe: str
    codigo:  Optional[str] = None