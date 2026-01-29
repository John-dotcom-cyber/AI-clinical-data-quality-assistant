import pandas as pd


def compute_quality_score(anomalies: pd.DataFrame, total_records: int) -> float:
    """
    Very simple V1 scoring:
    - score = 100 - (k * anomaly_rate)
    where anomaly_rate = nb_anomalies / total_records
    """
    if total_records == 0:
        return 100.0

    nb_anomalies = len(anomalies)
    anomaly_rate = nb_anomalies / total_records

    k = 100  # scaling factor
    score = max(0.0, 100.0 - k * anomaly_rate)
    return round(score, 2)
