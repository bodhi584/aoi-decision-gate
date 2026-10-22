"""AI decision gate for false-call reduction after automated optical inspection (AOI)."""
from .data import load, boards, feature_columns
from .model import Gate, threshold_for
from .replay import replay, summary
