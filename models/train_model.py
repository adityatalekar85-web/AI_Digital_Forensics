import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("datasets/sample_logs.csv")

print("Dataset Loaded Successfully\n")

# -----------------------------
# Convert Timestamp
# -----------------------------

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df["Year"] = df["Timestamp"].dt.year
df["Month"] = df["Timestamp"].dt.month
df["Day"] = df["Timestamp"].dt.day
df["Hour"] = df["Timestamp"].dt.hour

# Remove Timestamp
df.drop("Timestamp", axis=1, inplace=True)
# -----------------------------
# Encode Categorical Columns
# -----------------------------

encoders = {}

categorical_columns = [
    "Username",
    "IP_Address",
    "Country",
    "Login_Status",
    "Device",
    "OS",
    "Browser",
    "Attack_Type",
    "Threat_Label"
]

for col in categorical_columns:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
# -----------------------------
# Check Remaining Object Columns
# -----------------------------

print("\nRemaining Object Columns:")
print(df.select_dtypes(include="object").columns.tolist())

# -----------------------------
# Features & Target
# -----------------------------

X = df.drop(columns=["Threat_Label", "Log_ID"])

y = df["Threat_Label"]

# -----------------------------
# Train Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Train Model
# -----------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Prediction
# -----------------------------

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("\n" + "=" * 40)
print(f"Model Accuracy : {accuracy:.2f}")
print("=" * 40)

# -----------------------------
# Save Model
# -----------------------------

joblib.dump(model, "models/cyber_model.pkl")

print("✅ Model Saved Successfully")

joblib.dump(encoders, "models/encoders.pkl")

print("✅ Encoders Saved Successfully")