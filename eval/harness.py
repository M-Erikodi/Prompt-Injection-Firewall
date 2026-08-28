"""
Evaluation harness for scoring any detector against the labeled dataset.

A "detector" is any callable: (prompt: str) -> float
  Returns a score in [0, 1] representing injection/jailbreak likelihood.
  Thresholding into a binary verdict happens inside the harness so every
  detector is compared on equal footing (and thresholds can be tuned per model).

Usage:
    from eval.harness import evaluate
    from detectors.heuristic import score as heuristic_score

    results = evaluate(heuristic_score, dataset, threshold=0.5)
    print(results)  # {"precision": ..., "recall": ..., "fpr": ..., "f1": ...}
"""
from typing import Callable, List
from eval.schema import LabeledPrompt


def evaluate(
    detector: Callable[[str], float],
    dataset: List[LabeledPrompt],
    threshold: float = 0.5,
) -> dict:
    tp = fp = tn = fn = 0

    for item in dataset:
        score = detector(item.prompt)
        predicted = 1 if score >= threshold else 0

        if predicted == 1 and item.label == 1:
            tp += 1
        elif predicted == 1 and item.label == 0:
            fp += 1
        elif predicted == 0 and item.label == 0:
            tn += 1
        else:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    fpr = fp / (fp + tn) if (fp + tn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "fpr": round(fpr, 4),
        "f1": round(f1, 4),
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "n": len(dataset),
        "threshold": threshold,
    }
