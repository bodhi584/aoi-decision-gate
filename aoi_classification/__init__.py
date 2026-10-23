"""Binary classification of automated optical inspection (AOI) alarms: true defect or false call."""
from .data import load, boards, feature_columns
from .model import FalseCallClassifier, threshold_for
from .simulation import simulate, summary
