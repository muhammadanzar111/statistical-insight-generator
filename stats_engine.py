import numpy as np
import pandas as pd
from scipy import stats

def calculate_stats(data):
    """Calculates comprehensive descriptive statistics for a list of numerical values."""
    if not data or len(data) == 0:
        return {}

    count = len(data)
    mean = float(np.mean(data))
    median = float(np.median(data))
    
    # Calculate Mode
    mode_res = stats.mode(data, keepdims=True)
    mode_val = float(mode_res.mode[0]) if count > 0 else "N/A"

    std = float(np.std(data, ddof=1)) if count > 1 else 0.0
    variance = float(np.var(data, ddof=1)) if count > 1 else 0.0
    min_val = float(np.min(data))
    max_val = float(np.max(data))
    val_range = max_val - min_val

    q25, q75 = np.percentile(data, [25, 75])
    iqr = float(q75 - q25)

    lower_bound = q25 - (1.5 * iqr)
    upper_bound = q75 + (1.5 * iqr)
    outliers = [float(x) for x in data if x < lower_bound or x > upper_bound]

    return {
        "count": count,
        "mean": mean,
        "median": median,
        "mode": mode_val,
        "std": std,
        "variance": variance,
        "min": min_val,
        "max": max_val,
        "range": val_range,
        "iqr": iqr,
        "outliers": outliers
    }