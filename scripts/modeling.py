"""
modeling.py
---------------
Módulo de manipulação e criação de modelos de Machine Learning/IA
Inclui: 
    - Salvamento e Carregamento de objetos via Pickle e Joblib.
    - Entre outros.
"""

import os
import pickle
import joblib
from pathlib import Path
import sys

current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
import config_path          # Módulo que salva todos os caminhos de diretórios utilizados no projeto

# -----------------------------
# Auxiliadores de escrita e carregamento de arquivos
# -----------------------------
def save_pickle(obj, file_name: str):
    """
    Salvando objeto Python num arquivo atráves do Pickle.
    
    Parameters:
        obj: Python Object
        file_name: Nome do arquivo, deve incluir o tipo '.pkl'.
    Returns:
        None
    """
    if not file_name.endswith('.pkl'):
        raise SyntaxError(f"ERRO: Arquivo {file_name} não possui no final o tipo '.pkl'")
    
    caminho_completo = os.path.join(config_path.MODELS_DIRECTORY_PATH, file_name)
    with open(caminho_completo, 'wb') as f:
        pickle.dump(obj, f)
    
    print(f"Pickle salvou o modelo em '{config_path.MODELS_DIRECTORY_PATH}/{file_name}'")

def load_pickle(file_name: str):
    """
    Carrega um objeto Python de um arquivo pickle.
    
    args:
        file_name (str): Nome do arquivo '.pkl'.
    
    returns
        model: Objeto Python
    """
    
    if not file_name.endswith('pkl'):
        raise SyntaxError(f"ERRO: Arquivo {file_name} não possui no final o tipo '.pkl'")
    
    if not os.path.exists(f"{config_path.MODELS_DIRECTORY_PATH}/{file_name}"):
        raise FileNotFoundError(f"Arquivo não encontrado: {config_path.MODELS_DIRECTORY_PATH}/{file_name}")
    
    try:
        caminho_completo = os.path.join(config_path.MODELS_DIRECTORY_PATH, file_name)
        with open(caminho_completo, 'rb') as f:
            model = pickle.load(f)
            print(f"Pickle carregou o modelo em '{config_path.MODELS_DIRECTORY_PATH}/{file_name}'")
            return model
    except Exception as e:
        print(f"Erro ao processar o arquivo {file_name}: {e}")

def save_joblib(modelo, nome_arquivo: str):
    """
    Salva um modelo de Machine Learning (Scikit-Learn/Joblib) no disco.

    Args:
        modelo: O objeto do modelo treinado.
        nome_arquivo (str): Nome do arquivo.

    Returns:
        bool: True se salvo com sucesso, False se houver erro.
    """
    if not nome_arquivo.endswith('.joblib'):
        raise SyntaxError(f"ERRO: Arquivo {nome_arquivo} não possui no final o tipo '.joblib'")
    
    if not os.path.exists(f"{config_path.MODELS_DIRECTORY_PATH}"):
        raise FileNotFoundError(f"Caminho de diretório não existe: {config_path.MODELS_DIRECTORY_PATH}")
    
    caminho_completo = os.path.join(config_path.MODELS_DIRECTORY_PATH, nome_arquivo)
    joblib.dump(modelo, caminho_completo)
    print(f"Joblib salvou o modelo em: {nome_arquivo}")

def load_joblib(nome_arquivo: str):
    """
    Carrega um modelo a partir de um arquivo .joblib.
    
    args:
        nome_arquivo (str): Nome do arquivo
    """
    if not nome_arquivo.endswith('.joblib'):
        raise SyntaxError(f"ERRO: Arquivo {nome_arquivo} não possui no final o tipo '.joblib'")
    
    if not os.path.exists(f"{config_path.MODELS_DIRECTORY_PATH}/{nome_arquivo}"):
        raise FileNotFoundError(f"Arquivo {nome_arquivo} não existe no diretório 'models'")
    
    try:
        caminho_completo = os.path.join(config_path.MODELS_DIRECTORY_PATH, nome_arquivo)
        modelo = joblib.load(caminho_completo)
        print(f"Modelo carregado de: {nome_arquivo}")
        return modelo
    except Exception as e:
        print(f"Erro inesperado ocorreu: {e}")

def ensure_dir(path: Path | str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)