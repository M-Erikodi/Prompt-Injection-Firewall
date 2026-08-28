"""
FastAPI proxy: intercepts a prompt, scores it, blocks/flags/logs, then
(optionally) forwards to the real LLM call. Built Days 10-12.
Run with: uvicorn service.main:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Injection Detection Firewall")


class PromptRequest(BaseModel):
    prompt: str


class PromptVerdict(BaseModel):
    prompt: str
    score: float
    verdict: str  # "allow" | "flag" | "block"


@app.post("/check", response_model=PromptVerdict)
def check_prompt(req: PromptRequest):
    # TODO: swap in real detector(s) from detectors/
    detector_score = 0.0
    verdict = "block" if detector_score >= 0.8 else "flag" if detector_score >= 0.5 else "allow"
    # TODO: log to sqlite for the dashboard
    return PromptVerdict(prompt=req.prompt, score=detector_score, verdict=verdict)
