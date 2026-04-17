# train.py
# MedFlow Nexus - Sample Training Pipeline
# Purpose:
# Train models for:
# 1. Bed Occupancy Forecasting
# 2. ICU Demand Prediction
# 3. Equipment Utilization Prediction
# 4. Staff Shortage Risk Detection

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ======================================================
# LOAD DATASET
# ======================================================

# Example CSV:
# hospital_data.csv

df = pd.read_csv("hospital_data.csv")

print("Dataset Loaded Successfully")
print(df.head())

# ======================================================
# PREPROCESSING
# ======================================================

# Convert categorical columns
categorical_cols = ["district", "day_type", "season"]

encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Save encoders
joblib.dump(encoders, "encoders.pkl")

# ======================================================
# FEATURES
# ======================================================

features = [
    "district",
    "day_type",
    "season",
    "total_beds",
    "occupied_beds",
    "icu_beds",
    "staff_available",
    "ventilators_available",
    "daily_admissions",
    "daily_discharges"
]

X = df[features]

# ======================================================
# TARGET 1: NEXT DAY OCCUPANCY
# ======================================================

y_occ = df["next_day_occupancy"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_occ, test_size=0.2, random_state=42
)

model_occ = RandomForestRegressor(
    n_estimators=150,
    max_depth=10,
    random_state=42
)

model_occ.fit(X_train, y_train)

pred_occ = model_occ.predict(X_test)

mae_occ = mean_absolute_error(y_test, pred_occ)

print("\nOccupancy Forecast Model Trained")
print("MAE:", round(mae_occ, 2))

joblib.dump(model_occ, "models/occupancy_model.pkl")

# ======================================================
# TARGET 2: ICU DEMAND
# ======================================================

y_icu = df["next_day_icu_demand"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_icu, test_size=0.2, random_state=42
)

model_icu = RandomForestRegressor(
    n_estimators=120,
    max_depth=8,
    random_state=42
)

model_icu.fit(X_train, y_train)

pred_icu = model_icu.predict(X_test)

mae_icu = mean_absolute_error(y_test, pred_icu)

print("\nICU Demand Model Trained")
print("MAE:", round(mae_icu, 2))

joblib.dump(model_icu, "models/icu_model.pkl")

# ======================================================
# TARGET 3: EQUIPMENT SHORTAGE RISK
# ======================================================

# 0 = No Risk
# 1 = Risk

y_eq = df["equipment_shortage_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_eq, test_size=0.2, random_state=42
)

model_eq = RandomForestClassifier(
    n_estimators=120,
    max_depth=8,
    random_state=42
)

model_eq.fit(X_train, y_train)

pred_eq = model_eq.predict(X_test)

acc_eq = accuracy_score(y_test, pred_eq)

print("\nEquipment Risk Model Trained")
print("Accuracy:", round(acc_eq * 100, 2), "%")

joblib.dump(model_eq, "models/equipment_model.pkl")

# ======================================================
# TARGET 4: STAFF SHORTAGE ALERT
# ======================================================

y_staff = df["staff_shortage_alert"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_staff, test_size=0.2, random_state=42
)

model_staff = RandomForestClassifier(
    n_estimators=120,
    max_depth=8,
    random_state=42
)

model_staff.fit(X_train, y_train)

pred_staff = model_staff.predict(X_test)

acc_staff = accuracy_score(y_test, pred_staff)

print("\nStaff Shortage Model Trained")
print("Accuracy:", round(acc_staff * 100, 2), "%")

joblib.dump(model_staff, "models/staff_model.pkl")

# ======================================================
# FEATURE IMPORTANCE REPORT
# ======================================================

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model_occ.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nTop Features for Occupancy Prediction")
print(importance)

importance.to_csv("feature_importance.csv", index=False)

# ======================================================
# DONE
# ======================================================

print("\nAll Models Trained Successfully")
print("Saved Files:")
print("- models/occupancy_model.pkl")
print("- models/icu_model.pkl")
print("- models/equipment_model.pkl")
print("- models/staff_model.pkl")
print("- encoders.pkl")
print("- feature_importance.csv")
