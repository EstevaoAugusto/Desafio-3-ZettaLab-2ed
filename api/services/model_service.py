import joblib
import os
from pathlib import Path
import config_path

# Caminho para a pasta models que está fora da api/
MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "modelo_final.pkl"
SCALER_PATH = Path(__file__).resolve().parents[3] / "models" / "scaler.joblib"

class ModelService:
    def __init__(self):
        # Carrega o modelo uma única vez ao iniciar a API
        self.model = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)

    def predict(self, data):
        # Transforma o input do Pydantic em array para o modelo
        features = [[data.latitude, data.longitude]] # Exemplo simplificado
        features_scaled = self.scaler.transform(features)
        
        prediction = self.model.predict(features_scaled)
        prob = self.model.predict_proba(features_scaled)[0][1]
        
        return {
            "probabilidade_queimada": round(prob, 2),
            "risco": "Alto" if prob > 0.7 else "Baixo"
        }

# Instância única (Singleton) para não sobrecarregar a memória
model_service = ModelService()