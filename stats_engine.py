import math

def calculate_summary_statistics(numbers):
    if not numbers:
        return None

    n = len(numbers)
    
    # 1. Calculate Mean
    mean = sum(numbers) / n
    
    # 2. Calculate Median
    sorted_nums = sorted(numbers)
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median = sorted_nums[n//2]
        
    # 3. Calculate Standard Deviation
    if n > 1:
        variance = sum((x - mean) ** 2 for x in numbers) / (n - 1)
        std_dev = math.sqrt(variance)
    else:
        variance = 0.0
        std_dev = 0.0
        
    # 4. Outlier Detection (|z-score| > 2)
    outliers = []
    if std_dev > 0:
        for x in numbers:
            z_score = (x - mean) / std_dev
            if abs(z_score) > 2:
                outliers.append(x)
                
    return {
        "count": n,
        "mean": round(mean, 2),
        "median": round(median, 2),
        "variance": round(variance, 2),
        "std_dev": round(std_dev, 2),
        "min": min(numbers),
        "max": max(numbers),
        "outliers": outliers
    }