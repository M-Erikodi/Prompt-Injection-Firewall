import joblib
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  ##loaded once, when this module is first imported
classifier = joblib.load("detectors/classifier_model.joblib")  ##loaded once, not retrained

def score(prompt: str) -> float:
    embedding = model.encode([prompt])  ##encode expects a list, even for one item
    prob = classifier.predict_proba(embedding)[:, 1]  ##column 1 = probability of attack
    return prob[0]  ##unwrap the single result from the batch of one
