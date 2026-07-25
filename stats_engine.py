import numpy as np
import pandas as pd
from scipy import stats

def calculate_stats(data):
    """Calculates comprehensive descriptive statistics including mode and variance."""
    if not data or len(data) == 0:
        return {}

    count = len(data)
    mean = float(np.mean(data))
    median = float(np.median(data))
    
    # Mode calculation
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

# --- Inferential Statistics Functions ---

def run_one_sample_ttest(data, mu_0=0.0):
    if len(data) < 2:
        return {"t_stat": 0.0, "p_value": 1.0, "interpretation": "Insufficient data (minimum 2 values required)."}
    t_stat, p_val = stats.ttest_1samp(data, popmean=mu_0)
    interp = f"Reject Null Hypothesis ($p = {p_val:.4f} < 0.05$): Sample mean is significantly different from $\\mu_0 = {mu_0}$." if p_val < 0.05 else f"Fail to Reject Null ($p = {p_val:.4f} \\ge 0.05$): No significant difference from $\\mu_0 = {mu_0}$."
    return {"t_stat": float(t_stat), "p_value": float(p_val), "interpretation": interp}

def run_independent_ttest(group1, group2):
    if len(group1) < 2 or len(group2) < 2:
        return {"t_stat": 0.0, "p_value": 1.0, "interpretation": "Insufficient data in groups."}
    t_stat, p_val = stats.ttest_ind(group1, group2)
    interp = f"Reject Null Hypothesis ($p = {p_val:.4f} < 0.05$): Significant difference between group means." if p_val < 0.05 else f"Fail to Reject Null ($p = {p_val:.4f} \\ge 0.05$): No significant difference between group means."
    return {"t_stat": float(t_stat), "p_value": float(p_val), "interpretation": interp}

def run_paired_ttest(group1, group2):
    if len(group1) != len(group2) or len(group1) < 2:
        return {"t_stat": 0.0, "p_value": 1.0, "interpretation": "Groups must have equal lengths (>1)."}
    t_stat, p_val = stats.ttest_rel(group1, group2)
    interp = f"Reject Null Hypothesis ($p = {p_val:.4f} < 0.05$): Significant mean difference between paired conditions." if p_val < 0.05 else f"Fail to Reject Null ($p = {p_val:.4f} \\ge 0.05$): No significant difference between paired conditions."
    return {"t_stat": float(t_stat), "p_value": float(p_val), "interpretation": interp}

def run_one_sample_ztest(data, mu_0=0.0, sigma=None):
    n = len(data)
    if n < 2:
        return {"z_stat": 0.0, "p_value": 1.0, "interpretation": "Insufficient data (minimum 2 values required)."}
    sample_mean = np.mean(data)
    std_dev = sigma if sigma is not None and sigma > 0 else np.std(data, ddof=1)
    z_stat = (sample_mean - mu_0) / (std_dev / np.sqrt(n))
    p_val = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    interp = f"Reject Null Hypothesis ($p = {p_val:.4f} < 0.05$): Sample mean is significantly different from $\\mu_0 = {mu_0}$." if p_val < 0.05 else f"Fail to Reject Null ($p = {p_val:.4f} \\ge 0.05$): No significant difference from $\\mu_0 = {mu_0}$."
    return {"z_stat": float(z_stat), "p_value": float(p_val), "interpretation": interp}

def run_two_sample_ztest(group1, group2, sigma1=None, sigma2=None):
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return {"z_stat": 0.0, "p_value": 1.0, "interpretation": "Insufficient data in groups."}
    m1, m2 = np.mean(group1), np.mean(group2)
    s1 = sigma1 if sigma1 is not None and sigma1 > 0 else np.std(group1, ddof=1)
    s2 = sigma2 if sigma2 is not None and sigma2 > 0 else np.std(group2, ddof=1)
    se = np.sqrt((s1**2 / n1) + (s2**2 / n2))
    z_stat = (m1 - m2) / se
    p_val = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    interp = f"Reject Null Hypothesis ($p = {p_val:.4f} < 0.05$): Significant difference between group means." if p_val < 0.05 else f"Fail to Reject Null ($p = {p_val:.4f} \\ge 0.05$): No significant difference between group means."
    return {"z_stat": float(z_stat), "p_value": float(p_val), "interpretation": interp}

def run_anova(*groups):
    if any(len(g) < 2 for g in groups) or len(groups) < 2:
        return {"f_stat": 0.0, "p_value": 1.0, "interpretation": "Need at least 2 groups with >1 observation each."}
    f_stat, p_val = stats.f_oneway(*groups)
    interp = f"Reject Null Hypothesis ($p = {p_val:.4f} < 0.05$): At least one group mean is significantly different." if p_val < 0.05 else f"Fail to Reject Null ($p = {p_val:.4f} \\ge 0.05$): No significant difference among group means."
    return {"f_stat": float(f_stat), "p_value": float(p_val), "interpretation": interp}

def run_chi_square(contingency_table):
    chi2, p_val, dof, _ = stats.chi2_contingency(contingency_table)
    interp = f"Reject Null Hypothesis ($p = {p_val:.4f} < 0.05$): Significant association between variables." if p_val < 0.05 else f"Fail to Reject Null ($p = {p_val:.4f} \\ge 0.05$): Variables are independent."
    return {"chi2_stat": float(chi2), "p_value": float(p_val), "dof": dof, "interpretation": interp}

def run_correlation(x, y):
    if len(x) != len(y) or len(x) < 2:
        return {"corr": 0.0, "p_value": 1.0, "interpretation": "Equal-sized numerical vectors required."}
    r, p_val = stats.pearsonr(x, y)
    interp = f"Pearson $r = {r:.4f}$. " + (f"Statistically significant linear correlation ($p = {p_val:.4f} < 0.05$)." if p_val < 0.05 else f"No statistically significant correlation ($p = {p_val:.4f} \\ge 0.05$).")
    return {"corr": float(r), "p_value": float(p_val), "interpretation": interp}

def run_levene_test(*groups):
    if any(len(g) < 2 for g in groups) or len(groups) < 2:
        return {"stat": 0.0, "p_value": 1.0, "interpretation": "Need at least 2 groups with >1 observation each."}
    stat, p_val = stats.levene(*groups)
    interp = f"Reject Null Hypothesis ($p = {p_val:.4f} < 0.05$): Variances are significantly different." if p_val < 0.05 else f"Fail to Reject Null ($p = {p_val:.4f} \\ge 0.05$): Variances are equal across groups."
    return {"stat": float(stat), "p_value": float(p_val), "interpretation": interp}