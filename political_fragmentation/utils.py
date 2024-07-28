from typing import Optional
import numpy as np


def gini(x: list, weights: Optional[list] = None):
    if weights is None:
        weights = np.ones_like(x)
    if sum(weights) == 0:
        return 0
    weights_relative = [w / sum(weights) for w in weights]
    count = np.multiply.outer(weights_relative, weights_relative)
    mad = np.abs(np.subtract.outer(x, x) * count).sum() / count.sum()
    rmad = mad / np.average(x, weights=weights_relative)
    return 0.5 * rmad
