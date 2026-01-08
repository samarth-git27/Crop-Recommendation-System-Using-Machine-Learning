import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("data/Crop_recommendation.csv")

# Features and target
X = df[['N','P','K','temperature','humidity','ph','rainfall']]
y = df['label']

# Encode target labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Save encoder
joblib.dump(encoder, "models/label_encoder.pkl")

# Save processed data
X.to_csv("data/X.csv", index=False)
pd.DataFrame(y_encoded, columns=["target"]).to_csv("data/y.csv", index=False)

print("✅ Preprocessing completed successfully")
