"""
Shared schema for labeled prompts used across detectors and the eval harness.
Every dataset loader in data/ should normalize into this shape.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class LabeledPrompt:
    prompt: str
    label: int          # 1 = injection/jailbreak attempt, 0 = benign
    source: str          # e.g. "jailbreakbench", "hackaprompt", "alpaca"
    attack_type: Optional[str] = None  # e.g. "role_play", "encoding", "ignore_instructions", None if benign
