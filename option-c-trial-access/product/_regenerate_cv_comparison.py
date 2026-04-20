"""Regenerate model_comparison_cv.csv without running the full option-c pipeline.

This is a standalone re-execution of the Aim 2 modeling cells from option-c.qmd
(Section 8). It loads county_modeling_final.csv and fits Elastic Net, Random
Forest, and XGBoost under the same 5-fold CV scheme in both SES-only and Full
configurations, then writes the comparison table to:

    option-c-trial-access/product/data/modified/temp/model_comparison_cv.csv

Reproducing it from scratch takes ~10-25 minutes depending on CPU.
"""

from __future__ import annotations
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, RandomizedSearchCV, cross_val_predict
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

PRODUCT_DIR = Path(__file__).resolve().parent
DATA_MOD = PRODUCT_DIR / "data" / "modified"
TEMP = DATA_MOD / "temp"
TEMP.mkdir(parents=True, exist_ok=True)

print(f"Loading {DATA_MOD / 'county_modeling_final.csv'}")
county_df = pd.read_csv(DATA_MOD / "county_modeling_final.csv")
print(f"County dataset: {county_df.shape[0]} rows, {county_df.shape[1]} columns")

target = "places_diabetes"
county_df["log_trials"] = np.log1p(county_df["trials_per_100k"])
county_df["log_dist"]   = np.log1p(county_df["dist_nearest_trial_km"])
county_df["log_pop"]    = np.log(county_df["pop_total"])

access_vars = ["log_trials", "log_dist"]
ses_vars = [
    "log_pop", "pct_poverty", "median_hh_income", "gini_index",
    "pct_uninsured", "pct_unemployed", "pct_bachelors_plus",
    "pct_no_vehicle", "pct_no_internet", "pct_nhblack", "pct_hispanic",
]
all_predictors = access_vars + ses_vars

cols = [target] + all_predictors
df_model = county_df[cols].dropna().copy()
print(f"Complete cases: {len(df_model)} / {len(county_df)}")

y = df_model[target].values
X = df_model[all_predictors].values
scaler = StandardScaler()
X_sc = scaler.fit_transform(X)

cv = KFold(n_splits=5, shuffle=True, random_state=42)

# ---------------- Full-feature Elastic Net ----------------
t0 = time.time()
enet = ElasticNetCV(
    l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9],
    n_alphas=100, cv=cv, random_state=42, max_iter=10000,
)
enet.fit(X_sc, y)
y_pred = cross_val_predict(enet, X_sc, y, cv=cv)
rmse = float(np.sqrt(mean_squared_error(y, y_pred)))
mae  = float(mean_absolute_error(y, y_pred))
r2   = float(r2_score(y, y_pred))
print(f"[{time.time()-t0:.1f}s] Elastic Net (Full) R²={r2:.4f}")

# ---------------- Full-feature Random Forest (tuned) ----------------
t0 = time.time()
X_raw = df_model[all_predictors].values
rf_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42, n_jobs=-1),
    param_distributions={
        "n_estimators":     [200, 500, 800],
        "max_depth":        [None, 10, 20, 30],
        "min_samples_leaf": [1, 2, 4],
        "max_features":     ["sqrt", "log2", 0.5],
    },
    n_iter=30, cv=cv, scoring="r2", random_state=42, n_jobs=-1, verbose=0,
)
rf_search.fit(X_raw, y)
best_rf = rf_search.best_estimator_
y_pred_rf = cross_val_predict(best_rf, X_raw, y, cv=cv)
rmse_rf = float(np.sqrt(mean_squared_error(y, y_pred_rf)))
mae_rf  = float(mean_absolute_error(y, y_pred_rf))
r2_rf   = float(r2_score(y, y_pred_rf))
print(f"[{time.time()-t0:.1f}s] Random Forest (Full) R²={r2_rf:.4f}")

# ---------------- Full-feature XGBoost (tuned) ----------------
t0 = time.time()
xgb_search = RandomizedSearchCV(
    XGBRegressor(random_state=42, verbosity=0),
    param_distributions={
        "n_estimators":     [200, 500, 800],
        "learning_rate":    [0.01, 0.05, 0.1, 0.2],
        "max_depth":        [3, 5, 7],
        "subsample":        [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0],
        "min_child_weight": [1, 3, 5],
    },
    n_iter=30, cv=cv, scoring="r2", random_state=42, n_jobs=-1, verbose=0,
)
xgb_search.fit(X_raw, y)
best_xgb = xgb_search.best_estimator_
y_pred_xgb = cross_val_predict(best_xgb, X_raw, y, cv=cv)
rmse_xgb = float(np.sqrt(mean_squared_error(y, y_pred_xgb)))
mae_xgb  = float(mean_absolute_error(y, y_pred_xgb))
r2_xgb   = float(r2_score(y, y_pred_xgb))
print(f"[{time.time()-t0:.1f}s] XGBoost (Full) R²={r2_xgb:.4f}")

# ---------------- SES-only variants ----------------
t0 = time.time()
X_ses_sc  = scaler.fit_transform(df_model[ses_vars].values)
X_ses_raw = df_model[ses_vars].values

enet_ses = ElasticNetCV(
    l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9],
    n_alphas=100, cv=cv, random_state=42, max_iter=10000,
)
enet_ses.fit(X_ses_sc, y)
y_pred_ses_enet = cross_val_predict(enet_ses, X_ses_sc, y, cv=cv)
r2_ses_enet   = float(r2_score(y, y_pred_ses_enet))
rmse_ses_enet = float(np.sqrt(mean_squared_error(y, y_pred_ses_enet)))
mae_ses_enet  = float(mean_absolute_error(y, y_pred_ses_enet))

rf_ses = RandomForestRegressor(**rf_search.best_params_, random_state=42, n_jobs=-1)
y_pred_ses_rf = cross_val_predict(rf_ses, X_ses_raw, y, cv=cv)
r2_ses_rf   = float(r2_score(y, y_pred_ses_rf))
rmse_ses_rf = float(np.sqrt(mean_squared_error(y, y_pred_ses_rf)))
mae_ses_rf  = float(mean_absolute_error(y, y_pred_ses_rf))

xgb_ses = XGBRegressor(**xgb_search.best_params_, random_state=42, verbosity=0)
y_pred_ses_xgb = cross_val_predict(xgb_ses, X_ses_raw, y, cv=cv)
r2_ses_xgb   = float(r2_score(y, y_pred_ses_xgb))
rmse_ses_xgb = float(np.sqrt(mean_squared_error(y, y_pred_ses_xgb)))
mae_ses_xgb  = float(mean_absolute_error(y, y_pred_ses_xgb))
print(f"[{time.time()-t0:.1f}s] SES-only refits done")

# ---------------- Comparison table ----------------
model_comparison = pd.DataFrame({
    "Model":    ["Elastic Net", "Elastic Net",
                 "Random Forest", "Random Forest",
                 "XGBoost", "XGBoost"],
    "Features": ["SES-only", "Full",
                 "SES-only", "Full",
                 "SES-only", "Full"],
    "RMSE":     [rmse_ses_enet, rmse,
                 rmse_ses_rf, rmse_rf,
                 rmse_ses_xgb, rmse_xgb],
    "MAE":      [mae_ses_enet, mae,
                 mae_ses_rf, mae_rf,
                 mae_ses_xgb, mae_xgb],
    "R²":       [r2_ses_enet, r2,
                 r2_ses_rf, r2_rf,
                 r2_ses_xgb, r2_xgb],
})

out_path = TEMP / "model_comparison_cv.csv"
model_comparison.to_csv(out_path, index=False)
print("\n" + model_comparison.to_string(index=False))
print(f"\nSaved: {out_path}")
