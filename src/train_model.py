import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load processed data
X = pd.read_csv("data/X.csv")
y = pd.read_csv("data/y.csv")["target"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    random_state=42
)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/crop_model.pkl")

accuracy = model.score(X_test, y_test)
print(f"✅ Model trained with accuracy: {accuracy*100:.2f}%")
