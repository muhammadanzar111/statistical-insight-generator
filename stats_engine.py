import numpy as np
from scipy import stats

def calculate_stats(data):
    """Calculates comprehensive descriptive statistics for a list of numerical values."""
    if not data:
        return {}

    count = len(data)
    mean = float(np.mean(data))
    median = float(np.median(data))
    std = float(np.std(data, ddof=1)) if count > 1 else 0.0
    min_val = float(np.min(data))
    max_val = float(np.max(data))
    val_range = max_val - min_val

    q25, q75 = np.percentile(data, [25, 75])
    iqr = float(q75 - q25)

    # 1.5 * IQR Outlier Detection Rule
    lower_bound = q25 - (1.5 * iqr)
    upper_bound = q75 + (1.5 * iqr)
    outliers = [float(x) for x in data if x < lower_bound or x > upper_bound]

    return {
        "count": count,
        "mean": mean,
        "median": median,
        "std": std,
        "min": min_val,
        "max": max_val,
        "range": val_range,
        "iqr": iqr,
        "outliers": outliers
    }

def run_ttest(data, mu_0=0.0):
    """Performs a One-Sample t-test against a hypothesized population mean (mu_0)."""
    if len(data) < 2:
        return {
            "t_stat": 0.0,
            "p_value": 1.0,
            "interpretation": "Insufficient data to perform t-test (at least 2 observations required)."
        }

    t_stat, p_value = stats.ttest_1samp(data, popmean=mu_0)

    if p_value < 0.05:
        interpretation = f"Reject the null hypothesis ($p = {p_value:.4f} < 0.05$). There is a statistically significant difference from $\\mu_0 = {mu_0}$."
    else:
        interpretation = f"Fail to reject the null hypothesis ($p = {p_value:.4f} \\ge 0.05$). There is no statistically significant difference from $\\mu_0 = {mu_0}$."

    return {
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "interpretation": interpretation
    }