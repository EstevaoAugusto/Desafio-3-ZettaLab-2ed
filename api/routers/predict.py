from fastapi import APIRouter
from schemas.item import PredictionInput, PredictionOutput
from services.model_service import model_service

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
def make_prediction(payload: PredictionInput):
    result = model_service.predict(payload)
    return result