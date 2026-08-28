from eval.schema import LabeledPrompt
from datasets import load_dataset
import json
import os
from dataclasses import asdict

CACHE_PATH = "data/processed/combined.json"

## JailbreakBench
##jbb_data = load_dataset("JailbreakBench/JBB-Behaviors", "behaviors")
##print(jbb_data)
##print(jbb_data["harmful"][0])   ## inspect one row, check actual column names

## Alpaca (benign baseline)
##alpaca_data = load_dataset("tatsu-lab/alpaca")
##print(alpaca_data)
##print(alpaca_data["train"][0])



def load_jailbreakbench():
    """
    Load the JailbreakBench dataset and normalize both its splits
    (harmful + benign) into a single list of LabeledPrompt objects.
    """
    jbb_data = load_dataset("JailbreakBench/JBB-Behaviors", "behaviors")
    results = []

    ## JailbreakBench ships two splits with identical columns — the label
    ## comes from *which split* a row is in, not from a column inside it.
    for split, label in [("harmful", 1), ("benign", 0)]:
        for row in jbb_data[split]:
            ## Only harmful rows have a meaningful attack category;
            ## benign rows get None since "attack type" doesn't apply to them.
            attack_type = row["Category"] if label == 1 else None
            results.append(LabeledPrompt(
                prompt=row["Goal"],
                label=label,
                source="jailbreakbench",
                attack_type=attack_type
            ))

    return results

def load_jailbreakhub():
    jbh_data = load_dataset("walledai/JailbreakHub")
    results = []
    for row in jbh_data["train"]:
        if not row["jailbreak"]:
            continue
        results.append(LabeledPrompt(
            prompt=row["prompt"],
            label=1,
            source="jailbreakhub",
            attack_type=row["platform"]
        ))
    return results


def load_benign():
    """
    Load a random sample of benign (non-attack) prompts from Alpaca,
    used to measure false positives alongside the attack data above.
    """
    alpaca_data = load_dataset("tatsu-lab/alpaca")

    ## Alpaca only has one split ("train") with 52,002 rows
    ## so shuffle (randomize order) then take the first 300.
    ## seed=42 makes the "random" sample reproducible across runs.
    sampled = alpaca_data["train"].shuffle(seed=42).select(range(300))

    results = []
    for row in sampled:
        results.append(LabeledPrompt(
            prompt=row["instruction"],
            label=0,               ## everything here is benign by definition
            source="alpaca",
            attack_type=None       ## no such thing as an attack type on a benign prompt
        ))
    return results


def load_all():
    """Combine JailbreakBench (attacks + its own benign set) and Alpaca (benign) into one dataset."""

    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            raw_data = json.load(f)
        return [LabeledPrompt(**row) for row in raw_data]

    data = load_jailbreakbench() + load_benign()

    with open(CACHE_PATH, "w") as f:
        json.dump([asdict(item) for item in data], f, indent=2)

    return data

    return load_jailbreakbench() + load_benign()


## Only runs when this file is executed directly (e.g. `python -m data.load`),
## not when another file imports load_jailbreakbench/load_benign/load_all from it.
if __name__ == "__main__":
    data = load_all()
    print(len(data))    ## should be 500 (200 from jailbreakbench + 300 from alpaca)
    print(data[0])      ## first row — should be a jailbreakbench harmful example
    print(data[-1])     ## last row — should be an alpaca benign example






