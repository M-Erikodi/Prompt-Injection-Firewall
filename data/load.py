from eval.schema import LabeledPrompt
from datasets import load_dataset

# JailbreakBench
jbb_data = load_dataset("JailbreakBench/JBB-Behaviors", "behaviors")
print(jbb_data)
print(jbb_data["harmful"][0])   # inspect one row, check actual column names

# Alpaca (benign baseline)
alpaca_data = load_dataset("tatsu-lab/alpaca")
print(alpaca_data)
print(alpaca_data["train"][0])


def load_jailbreakbench():
    results = []

    for split, label in [("harmful", 1), ("benign", 0)]:
        for row in jbb_data[split]:
            attack_type = row["Category"] if label == 1 else None
            results.append(LabeledPrompt(prompt=row["Goal"], label=label, source="jailbreakbench", attack_type=attack_type))

    return results

results = load_jailbreakbench()
print(len(results)) ##should be 200 (100 harmful + 100 benign)
print(results[0])   ## inspect the first LabeledPrompt
print(results[-1])  ## inspect the last one, should be from the benign split