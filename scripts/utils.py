"""
utils.py
-----------
Módulo de utilitários para workflow de ciência de dados.
Inclui: 
    - Arquivo entrada/saida
    - auxiliadores de dataframe
    - plotting, logging, timers, e utilitários comuns de préprocessamento.
"""

import zipfile
from typing import Optional
import time
import basedosdados as bd
import os
import shutil
import requests
from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import sys

current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
import config_path          # Módulo que salva todos os caminhos de diretórios utilizados no projeto

# -------------------------
#  Auxiliador de manipulação de requisição HTTP
# -------------------------
def download_file(url: str, file_name : str, save_path: Path = config_path.RAW_DATA_DIRECTORY_PATH):
    """
    Baixa o arquivo do URL e o salva no caminho local

    Args:
        url (str): URL do arquivo a ser baixado
        file_name (str): Nome do arquivo
        save_path (Path | str): Caminho onde o arquivo será salvo.
    
    Returns:
        Path do arquivo salvo
    """

    # Fazer requisição
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Acionar o erro se o download falhar

    # Salvar conteudo do arquivo localmente
    with open(f"{save_path}/{file_name}", 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Arquivo baixado e salvo em: {save_path}/{file_name}")
    return Path(save_path) / file_name

def check_contained_files_zip(zip_file_path: Path) -> list[str]:
    """
    Retorna uma lista de arquivos contido no ZIP
    
    Args:
        zip_file_path (Path): Caminho completo do arquivo ZIP.
    Returns:
        extracted_files (list[str]): Lista de arquivos contido no ZIP.
    """
    
    if not zip_file_path.exists():
        raise FileNotFoundError(f"ERRO: '{zip_file_path}' não existe")
    
    if not zip_file_path.is_file():
        raise FileNotFoundError(f"ERRO: '{zip_file_path}' não é um arquivo")
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        extracted_files = zip_ref.namelist()
    
    return extracted_files

# -----------------------------------
#  Descompactar arquivo Zip
# -----------------------------------
def unzip_and_clean(zip_file_path: Path, files_to_keep: Optional[list[str]] | str = 'all', extract_path: Path = config_path.RAW_DATA_DIRECTORY_PATH):
    """
    Descompacta um arquivo ZIP e remove todos os arquivos que você não quer

    Args:
        zip_file_path (Path): Caminho completo para salvar o ZIP (ex: "C:/temp/meuarquivo.zip").
        files_to_keep (list[str]): Nome do arquivo que queremos manter (ex: "importante.txt").
        extract_path (Path | str): Caminho do diretório em que o arquivo ZIP está localizado.
    Returns:
        kept_paths (list): Lista de caminhos dos arquivos mantidos.
    """
    
    if isinstance(files_to_keep, list) and len(files_to_keep) <= 0:
        raise ValueError(f"ERRO: Argumento 'files_to_keep' não possui tamanho maior que zero!")
    
    if not zip_file_path.exists():
        raise FileNotFoundError(f"ERRO: '{zip_file_path}' não existe")
    
    if not zip_file_path.is_file():
        raise FileNotFoundError(f"ERRO: '{zip_file_path}' não é um arquivo")
    
    # 1. Extrair todo o conteúdo
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        extracted_files = zip_ref.namelist()
        if files_to_keep == 'all':
            files_to_keep = extracted_files
        
    print(f"Arquivos extraídos em: {extract_path}")

    # 2. Percorrer todos os arquivos e remover os indesejados
    kept_paths = []

    for file in extracted_files:
        file_path = Path(extract_path) / file

        # ignora diretórios
        if file_path.is_dir():
            continue

        file_name = file_path.name

        if file_name in files_to_keep:
            kept_paths.append(file_path)
        else:
            file_path.unlink()
            print(f"Removido: {file_path}")
    
    
    try:
        zip_file_path.unlink()
        print(f"ZIP removido: {zip_file_path}")
    except Exception as e:
        print(f"ERRO ao remover ZIP: {e}")
    
    # 3. Retornar os arquivos que foram mantidos
    print(f"Arquivos mantidos: {kept_paths}")
    return kept_paths

# -----------------------------
# Auxiliadores de Dataframe
# -----------------------------
def describe_df(df: pd.DataFrame):
    """
    Imprime as informações, shape e descrição de um DataFrame
    """
    print(f"Shape: {df.shape}\n")
    print("Info:")
    print(df.info())
    print("\nDescription:")
    print(df.describe())

def missing_summary(df: pd.DataFrame):
    """
    Retorna os valores nulos e porcentagem por coluna
    """
    total = df.isnull().sum()
    percent = (total / len(df)) * 100
    return pd.DataFrame({'missing': total, 'percent': percent}).sort_values('percent', ascending=False)

# -----------------------------
# Auxiliadores de plotting
# -----------------------------
def plot_histogram(df: pd.DataFrame, col: list[str], bins: int = 30, figsize: Tuple[int, int] = (10, 6)):
    plt.figure(figsize=figsize)
    
    # Adicionando o KDE para ver a "forma" da distribuição
    ax = sns.histplot(df[col], bins=bins, kde=True, color='skyblue', edgecolor='black')
    
    # Adicionando linhas de média e mediana
    mean = df[col].mean()
    median = df[col].median()
    
    plt.axvline(mean, color='red', linestyle='--', label=f'Média: {mean:.2f}')
    plt.axvline(median, color='green', linestyle='-', label=f'Mediana: {median:.2f}')
    
    plt.title(f'Distribuição de {col}', fontsize=15)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

def plot_correlation(df: pd.DataFrame, figsize: Tuple[int, int] = (12, 10)):
    # Calcular apenas para colunas numéricas para evitar erros
    corr = df.select_dtypes(include=[np.number]).corr()
    
    # Criar uma máscara para esconder o triângulo superior (repetido)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    plt.figure(figsize=figsize)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='RdBu_r', 
                center=0, square=True, linewidths=.5, cbar_kws={"shrink": .8})
    
    plt.title('Matriz de Correlação (Triângulo Inferior)', fontsize=15)
    plt.show()

def plot_scatter(df: pd.DataFrame, x_col, y_col, hue = None, regression: bool =True):
    # Jointplot cria o scatter e os histogramas marginais simultaneamente
    kind = "reg" if regression else "scatter"
    
    g = sns.jointplot(data=df, x=x_col, y=y_col, hue=hue, kind=kind, 
                      height=8, ratio=5, marginal_kws=dict(bins=20, fill=True))
    
    g.figure.suptitle(f'Relação: {x_col} vs {y_col}', y=1.02, fontsize=15)
    plt.show()

# -----------------------------
# Auxiliadores de logging e timer
# -----------------------------
def log(message: str):
    """Simple logger."""
    print(f"[INFO] {message}")

def timer(func):
    """Decorator to time function execution."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} executed in {end-start:.2f} seconds")
        return result
    return wrapper

# -----------------------------
# Checagem de valores e estado do DataFrame
# -----------------------------
def ensure_columns(df: pd.DataFrame, columns: list[str]):
    """
    Checa se colunas existem no DataFrame, retorna um erro se não possuir
    """
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def unique_values_summary(df: pd.DataFrame, columns: list[str]):
    """
    Retorna o número de valores únicos por coluna especifica
    """
    return {col: df[col].nunique() for col in columns}

def value_counts_summary(df: pd.DataFrame, columns: list[str]):
    """
    Retorna a contagem de valores por múltiplas colunas
    """
    return {col: df[col].value_counts() for col in columns}