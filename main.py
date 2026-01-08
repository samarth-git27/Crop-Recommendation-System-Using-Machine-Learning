from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("models/crop_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")

@app.post("/predict")
def predict_crop(data: dict):
    features = np.array([[ 
        data["N"], data["P"], data["K"],
        data["temperature"], data["humidity"],
        data["ph"], data["rainfall"]
    ]])
    prediction = model.predict(features)
    crop = encoder.inverse_transform(prediction)[0]
    return {"recommended_crop": crop}
