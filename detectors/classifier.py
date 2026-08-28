"""
ML-based classifier: embeddings + logistic regression (fast baseline),
optionally a fine-tuned DistilBERT if the simple model underperforms.
Built in Week 3 (Days 6-9). Compare directly against detectors/heuristic.py
using the same eval.harness.evaluate() call for an apples-to-apples number.
"""


def score(prompt: str) -> float:
    raise NotImplementedError("Fill in during Days 6-9: embeddings/logreg or DistilBERT")
