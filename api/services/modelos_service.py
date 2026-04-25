from __future__ import annotations

import os
import joblib
from fastapi import HTTPException
import lightgbm
from api.config_path_api import MODELS_DIRECTORY_PATH
from api.schemas.schemas import InfoModelo, ListaModelos, TipoModelo

# ──────────────────────────────────────────────
#  Cache de modelos em memória
# ──────────────────────────────────────────────
_cache: dict = {}

MAPA_TIPO: dict[str, TipoModelo] = {
    "classificacao": TipoModelo.classificacao,
    "intensidade":   TipoModelo.classificacao,
    "regressao":     TipoModelo.regressao,
    "predicao":      TipoModelo.regressao,
}


def _inferir_tipo(nome_arquivo: str) -> TipoModelo:
    nome_lower = nome_arquivo.lower()
    for chave, tipo in MAPA_TIPO.items():
        if chave in nome_lower:
            return tipo
    return TipoModelo.classificacao


def carregar_modelo(nome_arquivo: str):
    caminho = MODELS_DIRECTORY_PATH / nome_arquivo

    if not caminho.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Modelo '{nome_arquivo}' não encontrado em {MODELS_DIRECTORY_PATH}",
        )

    chave = str(caminho)
    if chave not in _cache:
        try:
            raw = joblib.load(caminho)
            _cache[chave] = raw["modelo"] if isinstance(raw, dict) and "modelo" in raw else raw
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao carregar modelo '{nome_arquivo}': {str(e)}")

    return _cache[chave]


def obter_info_modelo(nome_arquivo: str) -> InfoModelo:
    caminho = MODELS_DIRECTORY_PATH / nome_arquivo

    if not caminho.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Modelo '{nome_arquivo}' não encontrado em {MODELS_DIRECTORY_PATH}",
        )

    tamanho_mb = round(caminho.stat().st_size / (1024 * 1024), 3)

    try:
        modelo = joblib.load(caminho)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao abrir '{nome_arquivo}': {str(e)}")

    tipo   = _inferir_tipo(nome_arquivo)
    feature_names: list | None = None
    num_features:  int  | None = None
    num_classes:   int  | None = None
    classes:       list | None = None

    try:
        estimador = list(modelo.named_steps.values())[-1] if hasattr(modelo, "named_steps") else modelo
        if hasattr(estimador, "feature_names_in_"):
            feature_names = list(estimador.feature_names_in_)
        if hasattr(estimador, "n_features_in_"):
            num_features = int(estimador.n_features_in_)
        if tipo == TipoModelo.classificacao:
            if hasattr(estimador, "n_classes_"):
                num_classes = int(estimador.n_classes_)
            if hasattr(estimador, "classes_"):
                classes = [str(c) for c in estimador.classes_]
    except Exception:
        pass

    chave = str(caminho)
    if chave not in _cache:
        _cache[chave] = modelo

    return InfoModelo(
        nome          = nome_arquivo,
        tipo          = tipo,
        caminho       = str(caminho),
        tamanho_mb    = tamanho_mb,
        num_features  = num_features,
        feature_names = feature_names,
        num_classes   = num_classes,
        classes       = classes,
    )


def listar_modelos() -> ListaModelos:
    if not MODELS_DIRECTORY_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Diretório de modelos não encontrado: {MODELS_DIRECTORY_PATH}",
        )

    arquivos = sorted(f for f in os.listdir(MODELS_DIRECTORY_PATH) if f.endswith(".joblib"))

    if not arquivos:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum arquivo .joblib encontrado em {MODELS_DIRECTORY_PATH}",
        )

    model_infos = [obter_info_modelo(arq) for arq in arquivos]

    return ListaModelos(
        total=len(model_infos),
        modelos=model_infos,
    )


def limpar_cache() -> dict:
    qtd = len(_cache)
    _cache.clear()
    return {"mensagem": f"{qtd} modelo(s) removido(s) do cache."}