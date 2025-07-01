from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.sklearn
import numpy as np
from .pydantic_models import FeaturesRequest

app = FastAPI(title="Credit Risk Predictor")

# Load best model
model = mlflow.sklearn.load_model("exported_model")

@app.get("/")
def read_root():
    return {"message": "Credit Risk Model API running."}

@app.post("/predict")
def predict_risk(input: FeaturesRequest):
    try:
        X = np.array(list(input.features.values())).reshape(1, -1)
        prediction = model.predict(X)
        probability = model.predict_proba(X)[:, 1]  # Get the probability of the positive class
        prediction = prediction[0]  # Extract single prediction
        return {
            "is_credible": float(prediction),
            "probability": float(probability[0])
        }
    except Exception as e:
        return {"error": str(e)}
