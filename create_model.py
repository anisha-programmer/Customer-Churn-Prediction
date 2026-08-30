import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Create a demo model with sample data
X = pd.DataFrame({
    'tenure': [12, 24, 36, 48, 60],
    'MonthlyCharges': [50, 75, 100, 125, 150],
    'TotalCharges': [600, 1800, 3600, 6000, 9000]
})

y = [0, 0, 1, 1, 1]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model and columns
joblib.dump(model, "churn_model.pkl")
joblib.dump(X.columns.tolist(), "model_columns.pkl")

print("✅ Model files created successfully!")
print(f"Columns: {X.columns.tolist()}")
