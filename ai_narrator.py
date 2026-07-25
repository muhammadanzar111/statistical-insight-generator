def generate_narrative(stats):
    """Generates a rule-based narrative summary from calculated descriptive metrics."""
    if not stats:
        return "No data available to generate narrative insights."

    mean = stats["mean"]
    median = stats["median"]
    std = stats["std"]
    count = stats["count"]
    outliers = stats["outliers"]

    if abs(mean - median) < (0.1 * std if std > 0 else 0.1):
        symmetry_text = "The data appears roughly **symmetric**, as the mean and median are nearly identical."
    elif mean > median:
        symmetry_text = "The dataset is **right-skewed (positively skewed)**, indicating a tail of higher values pulling the mean above the median."
    else:
        symmetry_text = "The dataset is **left-skewed (negatively skewed)**, indicating a tail of lower values pulling the mean below the median."

    cv = (std / mean * 100) if mean != 0 else 0
    if cv < 15:
        variability_text = "Data points show **low variability**, clustered closely around the average."
    elif cv < 30:
        variability_text = "Data exhibits **moderate variability** relative to the mean."
    else:
        variability_text = "Data exhibits **high dispersion**, meaning values are widely spread out."

    if outliers:
        outlier_text = f"Anomalies detected: **{len(outliers)} outlier(s)** found using the 1.5 × IQR threshold ({', '.join([str(o) for o in outliers])})."
    else:
        outlier_text = "No severe statistical anomalies or outliers were identified."

    return (
        f"Based on **N = {count}** observations:\n\n"
        f"• **Distribution Shape:** {symmetry_text}\n"
        f"• **Spread & Consistency:** {variability_text} (Std Dev = {std:.2f}).\n"
        f"• **Outlier Status:** {outlier_text}"
    )
