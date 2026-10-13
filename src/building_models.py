# --- imports ---
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# median baseline
def baseline_predict(train, test):
    by_pair = train.groupby(["transit_mode", "delay_reason"])["min_delay"].median()
    by_mode = train.groupby("transit_mode")["min_delay"].median()
    keys = pd.MultiIndex.from_frame(test[["transit_mode", "delay_reason"]])
    # tier 1: median of reason + mode
    pred = pd.Series(by_pair.reindex(keys).values, index=test.index)
    # tier 2: median of mode
    pred = pred.fillna(test["transit_mode"].map(by_mode))
    # tier 3: median of dataset
    return pred.fillna(train["min_delay"].median())

# evaluating models
def make_pipeline(model, CATEGORICAL, NUMERIC):
    prep = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=30,
                                                       sparse_output=False), CATEGORICAL),
        ("num", "passthrough", NUMERIC),
    ])
    return Pipeline([("prep", prep), ("model", model)])