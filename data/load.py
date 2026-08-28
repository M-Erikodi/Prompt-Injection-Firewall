"""
Loaders that pull raw datasets and normalize them into eval.schema.LabeledPrompt.
Built Days 1-2. Add one function per source; keep raw downloads in data/raw/,
normalized/combined output in data/processed/.
"""
from typing import List
from eval.schema import LabeledPrompt


def load_jailbreakbench() -> List[LabeledPrompt]:
    # TODO: pull via `datasets` lib or manual download into data/raw/
    raise NotImplementedError


def load_benign(source: str = "alpaca") -> List[LabeledPrompt]:
    # TODO: benign baseline for false-positive measurement
    raise NotImplementedError


def load_all() -> List[LabeledPrompt]:
    """Combine all sources into one labeled dataset."""
    data = []
    # data += load_jailbreakbench()
    # data += load_benign()
    return data
