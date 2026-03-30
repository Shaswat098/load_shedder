import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

model = joblib.load(MODEL_PATH)

def predict(features):

    X = [[
        features["user_rate"],
        features["queue_length"],
        features["priority_score"]
    ]]

    return model.predict(X)[0]