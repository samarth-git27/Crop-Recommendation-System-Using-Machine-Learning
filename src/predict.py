import joblib
import numpy as np

model = joblib.load("models/crop_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")

# Sample input
sample = np.array([[90, 42, 43, 20.8, 82.0, 6.5, 200]])

prediction = model.predict(sample)
crop = encoder.inverse_transform(prediction)

print("🌱 Recommended Crop:", crop[0])
