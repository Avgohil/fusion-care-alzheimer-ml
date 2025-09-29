import joblib

feature_columns = joblib.load("models/stage1_input_features_clean.pkl")

# Handle different types
try:
    import pandas as pd
    import numpy as np
    if isinstance(feature_columns, pd.DataFrame):
        feature_columns = feature_columns.columns.tolist()
    elif isinstance(feature_columns, (np.ndarray, pd.Series)):
        feature_columns = feature_columns.flatten().tolist()
    elif isinstance(feature_columns, dict):
        feature_columns = list(feature_columns.keys())
except ImportError:
    pass

print("Feature columns:")
for col in feature_columns:
    print(col)
