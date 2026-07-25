def generate_statistical_insights(stats_dict, dataset_label="Dataset"):
    """
    Generates dynamic executive insights using pure Python logic.
    """
    count = stats_dict['count']
    mean = stats_dict['mean']
    median = stats_dict['median']
    std_dev = stats_dict['std_dev']
    outliers = stats_dict['outliers']
    
    # Calculate Skewness Direction
    if abs(mean - median) < 0.01:
        skew = "symmetrical"
        skew_desc = "the mean and median are virtually identical, indicating a balanced distribution."
    elif mean > median:
        skew = "right-skewed (positively skewed)"
        skew_desc = f"the mean ({mean}) is higher than the median ({median}), likely pulled upward by higher values or outliers."
    else:
        skew = "left-skewed (negatively skewed)"
        skew_desc = f"the mean ({mean}) is lower than the median ({median}), indicating concentration on the higher end with lower extreme values."

    # Outlier Analysis Text
    if outliers:
        outlier_text = f"Identified extreme values in the dataset: `{outliers}`. These should be investigated to determine if they represent data entry errors or legitimate statistical anomalies."
    else:
        outlier_text = "No statistical outliers detected based on the 1.5x IQR rule. The distribution remains within typical boundaries."

    # Construct clean insights summary
    insights = f"""
### Executive Insights: {dataset_label}

**1. Central Tendency & Distribution**
* The dataset contains **{count} observations**.
* The distribution pattern is **{skew}**—{skew_desc}

**2. Dispersion & Variance**
* Standard Deviation: **{std_dev}**
* The spread around the center (mean: {mean}) shows moderate variance across sample data points ranging from **{stats_dict['min']}** to **{stats_dict['max']}**.

**3. Anomalies & Next Steps**
* {outlier_text}
* **Recommendation:** Use median values for central benchmarking if skewness is high, or standard mean if variance remains balanced.
"""
    return insights