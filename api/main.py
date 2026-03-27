from fastapi import FastAPI
from routes import predict

app = FastAPI(
    title="API de Predição de Queimadas",
    description="Integração do modelo de Data Science com o sistema de software.",
    version="1.0.0"
)

# Inclui as rotas que criamos
app.include_router(predict.router, prefix="/v1", tags=["Machine Learning"])

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "online", "model_loaded": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)