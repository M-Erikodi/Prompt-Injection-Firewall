"""
Baseline heuristic detector: keyword/regex patterns, encoding checks, formatting anomalies.
Built in Week 2 (Days 3-5). Every rule added here should be re-run through
eval.harness.evaluate() so its precision/recall/FPR impact is measured immediately.
"""
import re

PATTERNS = [
    # TODO: expand this list during days 3-4.
    # Keep patterns specific enough to avoid false positives on benign prompts
    # that legitimately discuss instructions, roleplay, or encoding.

    r"ignore (all|any|the) (previous|prior|above) instructions",
    r"act as",
    r"act as if you are",
    r"you (will|must|should) (be|act|respond) as", 
    r"you are (now|no longer|not) ",
    r"you are",
    r"disregard (all|any) (previous|prior) (rules|instructions)",
    r"system prompt",
    r"jailbreak",
    r"write a (defamatory|malicious|harmful|illegal|offensive|unethical)",
    r"write (a|an) (sexist|racist|hateful|offensive|illegal|malicious|harmful|unethical|xenophobic)",
    r"(develop|draft|design|create|write) (a|an) (exploit|attack|malware|virus|trojan|worm|payload|backdoor|ransomware|keylogger|rootkit|sexist|racist|hateful|offensive|illegal|malicious|harmful|unethical|xenophobic)",
    r"(develop|draft|design|create|write) (exploit|attack|malware|virus|trojan|worm)",
]

COMPILED = [re.compile(p, re.IGNORECASE) for p in PATTERNS]


def score(prompt: str) -> float:
    """Returns a naive score in [0, 1] based on pattern hit count."""
    hits = sum(1 for p in COMPILED if p.search(prompt))
    if hits == 0:
        return 0.0
    return min(1.0, 0.3 + 0.2 * hits)


if __name__ == "__main__":
    from eval.harness import evaluate
    from data.load import load_all

    results = evaluate(score, load_all(), threshold=0.5)
    print(results)