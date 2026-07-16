from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.api.schemas import PredictRequest, PredictResponse
from app.api.inference import load_models, predict_ticket

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML models and TF-IDF vectors
    try:
        load_models()
    except Exception as e:
        print(f"Error loading models: {e}")
    yield
    # Shutdown: Clean up if needed (none required here)


app = FastAPI(
    title="Support Ticket Intelligence System API",
    description="Backend API for classifying support tickets, retrieving resolutions, and explaining predictions.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    try:
        results = predict_ticket(request.subject, request.description)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
