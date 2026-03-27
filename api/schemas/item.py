from pydantic import BaseModel

class PredictionInput(BaseModel):
    latitude: float
    longitude: float
    estado: str
    estacao: str

class PredictionOutput(BaseModel):
    probabilidade_queimada: float
    risco: str