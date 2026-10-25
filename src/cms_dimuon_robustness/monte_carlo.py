"""Monte Carlo summaries; these functions do not perform a CMS resonance fit."""
from __future__ import annotations

import math
from dataclasses import dataclass

from scipy.stats import beta


@dataclass(frozen=True)
class BinomialEstimate:
    successes: int
    trials: int
    estimate: float
    lower: float
    upper: float
    confidence_level: float


def clopper_pearson(successes: int, trials: int, confidence_level: float = 0.95) -> BinomialEstimate:
    """Return an exact two-sided Clopper-Pearson interval for a binomial proportion.

    The interpretation depends on the experiment design. This utility cannot make an
    invalid generator or test statistically valid.
    """
    if isinstance(successes, bool) or isinstance(trials, bool):
        raise ValueError("successes and trials must be integers, not booleans")
    if not isinstance(successes, int) or not isinstance(trials, int):
        raise ValueError("successes and trials must be integers")
    if trials <= 0 or successes < 0 or successes > trials:
        raise ValueError("require trials > 0 and 0 <= successes <= trials")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must lie strictly between 0 and 1")

    tail = (1.0 - confidence_level) / 2.0
    lower = 0.0 if successes == 0 else float(beta.ppf(tail, successes, trials - successes + 1))
    upper = 1.0 if successes == trials else float(beta.ppf(1.0 - tail, successes + 1, trials - successes))
    return BinomialEstimate(successes, trials, successes / trials, lower, upper, confidence_level)


def approximate_trials_for_absolute_precision(
    target_probability: float, half_width: float, confidence_z: float = 1.96
) -> int:
    """Plan a binomial sample size using a normal-approximation half-width.

    This is a planning approximation, not a guarantee. Use exact intervals for final
    reporting and larger runs when probabilities are small or uncertain.
    """
    if not 0.0 < target_probability < 1.0:
        raise ValueError("target_probability must lie strictly between 0 and 1")
    if not 0.0 < half_width < 1.0:
        raise ValueError("half_width must lie strictly between 0 and 1")
    if not math.isfinite(confidence_z) or confidence_z <= 0:
        raise ValueError("confidence_z must be finite and positive")
    n = target_probability * (1.0 - target_probability) * (confidence_z / half_width) ** 2
    return math.ceil(n)
