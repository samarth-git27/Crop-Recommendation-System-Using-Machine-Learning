from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI(
    title="Crop Recommendation API",
    description="ML-powered crop recommendation system",
    version="1.0"
)

model = joblib.load("models/crop_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")

@app.post("/predict")
def predict_crop(
    N: float,
    P: float,
    K: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float
):
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    prediction = model.predict(features)
    crop = encoder.inverse_transform(prediction)[0]

    return {
        "recommended_crop": crop
    }
