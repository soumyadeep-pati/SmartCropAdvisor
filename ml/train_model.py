import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Load Dataset
df = pd.read_csv("ml/datasets/Crop_recommendation.csv")

# Features
X = df.drop("label", axis=1)

# Target
y = df["label"]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Model
model = RandomForestClassifier()

# Train Model
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# Save Model
joblib.dump(
    model,
    "ml/models/model.pkl"
)

print("Model Saved Successfully")