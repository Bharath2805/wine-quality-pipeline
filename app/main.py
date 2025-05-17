from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import os

app = FastAPI()

class Features(BaseModel):
    features: list

# Load model from local or GCS if needed
MODEL_PATH = "wine_quality_model.pkl"

if not os.path.exists(MODEL_PATH):
    from google.cloud import storage
    client = storage.Client()
    bucket = client.bucket("wine-quality-models-bucket")
    blob = bucket.blob(MODEL_PATH)
    blob.download_to_filename(MODEL_PATH)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
def predict(features: Features):
    X = np.array([features.features])
    prediction = model.predict(X)
    return {"predicted_quality": int(prediction[0])}
