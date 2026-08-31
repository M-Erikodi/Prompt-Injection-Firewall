# Prompt Injection Detection Firewall

A lightweight defense layer that sits between users and an LLM, scoring incoming
prompts for injection/jailbreak likelihood before they reach the model. Built to
explore both the security and ML sides of a real, unsolved problem in deployed
LLM applications.

## The Problem

Prompt injection is the #1 risk on OWASP's Top 10 for LLM Applications. Most
teams deploying chatbots, agents, or RAG systems have zero input-layer defense —
an attacker can hijack model behavior by hiding instructions in user input
("ignore previous instructions...") or in retrieved content the model reads.
This project builds a testable, evaluatable defense layer rather than assuming
the problem away.

## Architecture

Detection is layered, not single-stage:

1. **Heuristic layer** (regex/keyword patterns) runs first — fast, cheap,
   near-zero false positive rate. If it fires with high confidence, the
   request is blocked immediately.
2. **ML classifier** (sentence embeddings + logistic regression) runs only if
   heuristics pass the prompt through — slower, more expensive, but catches
   paraphrased/novel attacks heuristics structurally can't.

This mirrors real production security systems (WAFs, spam filters): cheap
deterministic rules filter the obvious cases; an expensive learned model only
runs when needed.

## Results

Evaluated on a combined dataset of ~1,900 labeled prompts (JailbreakBench,
JailbreakHub, Alpaca as benign baseline), with a held-out 20% test split for
the classifier.

| Detector | Precision | Recall | FPR |
|---|---|---|---|
| Heuristics | 99.89% | 60.27% | 0.25% |
| ML Classifier (threshold 0.7) | 98.94% | 92.69% | 3.75% |

Heuristics catch obvious, previously-seen phrasing with almost no false alarms,
but miss ~40% of real attacks by design — they can't generalize past exact
patterns. The classifier closes most of that gap by working on semantic
meaning rather than literal text, at a small, tunable cost in false positives.

## Red-Team Findings

Manually crafted adversarial variants were run against the live service to
test both layers under attack:

- **Paraphrasing**: heuristics caught 0/5 reworded attacks; the classifier
  still caught or flagged all 5, via semantic understanding rather than
  exact matching.
- **Character-spacing obfuscation** (`I-g-n-o-r-e...`): fully bypassed both
  layers. This is a genuine, unresolved gap.
- **Base64 / reversed text**: both scored in the "flag" range against the
  classifier — better resilience than expected, though the exact mechanism
  isn't fully understood.
- **Unicode homoglyphs**: defeated the specific word they targeted, but the
  overall prompt was still caught due to an untouched trigger phrase
  elsewhere in the same sentence.
- **Multi-turn attacks**: not testable — the service scores single prompts
  with no conversation memory, an explicit architectural limitation.

## Known Limitations

- No defense against character-level obfuscation (spacing, homoglyphs on
  every trigger word).
- No multi-turn context — each request is evaluated independently.
- One of the source datasets (JailbreakBench's "benign" split) contains
  ethically ambiguous content that isn't truly benign in the everyday sense,
  which inflates the classifier's measured false-positive rate somewhat.
- Classifier decisions aren't interpretable — no explanation for why a score
  was assigned, unlike heuristics where the matched pattern is known.

## Project Structure

    data/        — dataset loaders and caching
    detectors/   — heuristic rules and ML classifier
    eval/        — shared schema and precision/recall/FPR harness
    service/     — FastAPI proxy, SQLite logging, Streamlit dashboard
    notebooks/   — exploration, data analysis, red-team testing

## Running It

    pip install -r requirements.txt
    python -m detectors.train_classifier   # trains and saves the classifier
    uvicorn service.main:app --reload      # starts the API
    streamlit run service/dashboard.py     # starts the dashboard

## What I'd Do Next

- Fine-tune a small transformer (DistilBERT) instead of logistic regression
  over embeddings, to see if it closes the character-spacing gap.
- Add output-side checks (canary tokens to detect system prompt leakage).
- Extend to multi-turn conversation context.