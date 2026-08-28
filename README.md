# injection-firewall

A lightweight, testable defense layer against prompt injection and jailbreak
attempts in LLM-powered applications. Sits between the user and the LLM API
call, scores incoming prompts for injection likelihood, and blocks/flags/logs
accordingly.

## Structure

- `data/` — raw + processed datasets (attack prompts + benign baseline)
- `detectors/` — heuristic rules (Week 2) and ML classifier (Week 3)
- `eval/` — shared schema + evaluation harness (precision/recall/FPR)
- `service/` — FastAPI proxy + dashboard (Week 4)
- `notebooks/` — exploratory analysis, red-team logs (Week 5)
- `tests/` — unit tests

## Status

Scaffolded. See ROADMAP.md for the day-by-day plan.

## Quickstart (once populated)

```bash
pip install -r requirements.txt
uvicorn service.main:app --reload
```
