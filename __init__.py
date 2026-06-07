"""MeowLM — a tiny language model that thinks it's in charge."""

from .generate_data import generate_dataset
from .prepare_data import prepare
from .eval_cases import get_eval_cases

__all__ = ["generate_dataset", "prepare", "get_eval_cases"]
