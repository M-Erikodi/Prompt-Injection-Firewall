from datasets import load_dataset

# JailbreakBench
jbb_data = load_dataset("JailbreakBench/JBB-Behaviors", "behaviors")
print(jbb_data)
print(jbb_data["harmful"][0])   # inspect one row, check actual column names

# Alpaca (benign baseline)
alpaca_data = load_dataset("tatsu-lab/alpaca")
print(alpaca_data)
print(alpaca_data["train"][0])
