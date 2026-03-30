from core.ml.model import predict

def score_request(features):
    decision = predict(features)
    return decision