"""
FastAPI proxy: intercepts a prompt, scores it, blocks/flags/logs, then
(optionally) forwards to the real LLM call. Built Days 10-12.
Run with: uvicorn service.main:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
from detectors.heuristic import score as heuristic_score
from detectors.classifier import score as classifier_score

app = FastAPI(title="Injection Detection Firewall")


class PromptRequest(BaseModel):
    prompt: str


class PromptVerdict(BaseModel):
    prompt: str
    score: float
    verdict: str  ##"allow" | "flag" | "block"
    detector: str  ##which detector actually produced the final score


@app.post("/check", response_model=PromptVerdict)
def check_prompt(req: PromptRequest):
    h_score = heuristic_score(req.prompt)  ##cheap fast an near-perfect precision

    if h_score >= 0.5:
        ##heuristics fired with high confidence block immediately, skip the classifier
        return PromptVerdict(
            prompt=req.prompt,
            score=h_score,
            verdict="block",
            detector="heuristic"
        )

    ##heuristics didn't fire fall through to the deeper, more expensive check
    c_score = classifier_score(req.prompt)

    if c_score >= 0.7:
        verdict = "block"
    elif c_score >= 0.5:
        verdict = "flag"
    else:
        verdict = "allow"

    return PromptVerdict(
        prompt=req.prompt,
        score=c_score,
        verdict=verdict,
        detector="classifier"
    )
