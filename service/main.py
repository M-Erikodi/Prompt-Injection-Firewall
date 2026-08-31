from fastapi import FastAPI
from pydantic import BaseModel
from detectors.heuristic import score as heuristic_score
from detectors.classifier import score as classifier_score
from service.db import init_db, log_request

app = FastAPI(title="Injection Detection Firewall")

init_db()  ##runs once, when the service starts


class PromptRequest(BaseModel):
    prompt: str


class PromptVerdict(BaseModel):
    prompt: str
    score: float
    verdict: str
    detector: str


@app.post("/check", response_model=PromptVerdict)
def check_prompt(req: PromptRequest):
    h_score = heuristic_score(req.prompt)

    if h_score >= 0.5:
        log_request(req.prompt, h_score, "block", "heuristic")
        return PromptVerdict(prompt=req.prompt, score=h_score, verdict="block", detector="heuristic")

    c_score = float(classifier_score(req.prompt))  ##convert numpy.float32 to plain python float

    if c_score >= 0.7:
        verdict = "block"
    elif c_score >= 0.5:
        verdict = "flag"
    else:
        verdict = "allow"

    log_request(req.prompt, c_score, verdict, "classifier")
    return PromptVerdict(prompt=req.prompt, score=c_score, verdict=verdict, detector="classifier")