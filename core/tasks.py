from celery import shared_task
from core.utils.cache_store import set_cache
from core.utils.metrics_store import get_metrics, log_metric
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import numpy as np, pandas as pd


@shared_task
def update_cache_task(key, data):
    set_cache(key, data)

@shared_task
def log_metrics_task(data):
    log_metric(data)

@shared_task
def retrain_model_task():
    data = get_metrics()
    
    if len(data) < 50:
        return "Not enough data to retrain"
    
    df = pd.DataFrame(data)
    X = df[["user_rate", "queue_length", "priority_score"]]
    y = df["decison"]

    model = RandomForestClassifier()
    model.fit(X,y)

    model_path = os.path.join("core","ml","model.pkl")
    joblib.dump(model,model_path)

    return "Model retrained sucessfully"
