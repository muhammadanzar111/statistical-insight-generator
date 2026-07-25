def generate_narrative(stats):
    if not stats:
        return "No data available for analysis."

    mode_str = f"{stats['mode']:.2f}" if isinstance(stats.get('mode'), (int, float)) else str(stats.get('mode', 'N/A'))

    narrative = f"""
- **Central Tendency:** The dataset has a mean of **{stats.get('mean', 0.0):.2f}**, a median of **{stats.get('median', 0.0):.2f}**, and a mode of **{mode_str}**.
- **Variability & Dispersion:** The standard deviation is **{stats.get('std', 0.0):.2f}** with a sample variance of **{stats.get('variance', 0.0):.2f}**, indicating the overall spread of values around the mean.
- **Range & Outliers:** Values range from **{stats.get('min', 0.0):.2f}** to **{stats.get('max', 0.0):.2f}** (Total Range: **{stats.get('range', 0.0):.2f}**). There are **{len(stats.get('outliers', []))}** potential outlier(s) detected using the $1.5 \\times \\text{{IQR}}$ rule.
    """
    return narrative