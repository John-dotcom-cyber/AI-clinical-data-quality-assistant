from typing import Dict, List

import pandas as pd


def check_referential_integrity(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    anomalies = []

    patients = data["patients"]
    visits = data["visits"]
    labs = data["labs"]

    patient_ids = set(patients["patient_id"])

    # Visits
    for _, row in visits.iterrows():
        if row["patient_id"] not in patient_ids:
            anomalies.append({
                "table": "visits",
                "patient_id": row["patient_id"],
                "type": "referential_integrity",
                "field": "patient_id",
                "message": "Visit references a non-existing patient_id",
                "severity": "high",
            })

    # Labs
    for _, row in labs.iterrows():
        if row["patient_id"] not in patient_ids:
            anomalies.append({
                "table": "labs",
                "patient_id": row["patient_id"],
                "type": "referential_integrity",
                "field": "patient_id",
                "message": "Lab record references a non-existing patient_id",
                "severity": "high",
            })

    return pd.DataFrame(anomalies)


def check_temporal_rules(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    anomalies = []

    patients = data["patients"].copy()
    visits = data["visits"].copy()
    labs = data["labs"].copy()

    # Cast dates
    for df, cols in [
        (patients, ["birth_date", "inclusion_date"]),
        (visits, ["visit_date"]),
        (labs, ["lab_date"]),
    ]:
        for c in cols:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    patients_indexed = patients.set_index("patient_id")

    # Birth < inclusion
    for _, row in patients.iterrows():
        if pd.isna(row["birth_date"]) or pd.isna(row["inclusion_date"]):
            continue
        if row["birth_date"] >= row["inclusion_date"]:
            anomalies.append({
                "table": "patients",
                "patient_id": row["patient_id"],
                "type": "temporal_inconsistency",
                "field": "birth_date/inclusion_date",
                "message": "Birth date is not before inclusion date",
                "severity": "high",
            })

    # Visits after inclusion
    for _, row in visits.iterrows():
        pid = row["patient_id"]
        if pid not in patients_indexed.index:
            continue
        inclusion_date = patients_indexed.loc[pid, "inclusion_date"]
        if pd.isna(row["visit_date"]) or pd.isna(inclusion_date):
            continue
        if row["visit_date"] < inclusion_date:
            anomalies.append({
                "table": "visits",
                "patient_id": pid,
                "type": "temporal_inconsistency",
                "field": "visit_date",
                "message": "Visit date is before inclusion date",
                "severity": "medium",
            })

    # Labs after inclusion
    for _, row in labs.iterrows():
        pid = row["patient_id"]
        if pid not in patients_indexed.index:
            continue
        inclusion_date = patients_indexed.loc[pid, "inclusion_date"]
        if pd.isna(row["lab_date"]) or pd.isna(inclusion_date):
            continue
        if row["lab_date"] < inclusion_date:
            anomalies.append({
                "table": "labs",
                "patient_id": pid,
                "type": "temporal_inconsistency",
                "field": "lab_date",
                "message": "Lab date is before inclusion date",
                "severity": "medium",
            })

    return pd.DataFrame(anomalies)


def check_physiological_ranges(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    anomalies: List[dict] = []

    labs = data["labs"].copy()

    # Simple hard-coded rules V1
    for _, row in labs.iterrows():
        lab_type = row.get("lab_type")
        value = row.get("lab_value")
        pid = row.get("patient_id")

        if pd.isna(value):
            continue

        if lab_type == "glucose":  # mg/dL
            if value < 40 or value > 600:
                anomalies.append({
                    "table": "labs",
                    "patient_id": pid,
                    "type": "physiological_out_of_range",
                    "field": "lab_value",
                    "message": f"Glucose value {value} mg/dL is physiologically implausible",
                    "severity": "high",
                })

        if lab_type == "creatinine":  # mg/dL
            if value < 0.2 or value > 15:
                anomalies.append({
                    "table": "labs",
                    "patient_id": pid,
                    "type": "physiological_out_of_range",
                    "field": "lab_value",
                    "message": f"Creatinine value {value} mg/dL is physiologically implausible",
                    "severity": "high",
                })

        if lab_type == "hbA1c":  # %
            if value < 3 or value > 18:
                anomalies.append({
                    "table": "labs",
                    "patient_id": pid,
                    "type": "physiological_out_of_range",
                    "field": "lab_value",
                    "message": f"HbA1c value {value}% is physiologically implausible",
                    "severity": "medium",
                })

    return pd.DataFrame(anomalies)


def run_all_rules(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Run all rule sets and return a unified anomalies dataframe.
    """
    dfs = []

    for func in [check_referential_integrity, check_temporal_rules, check_physiological_ranges]:
        df = func(data)
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return pd.DataFrame(columns=["table", "patient_id", "type", "field", "message", "severity"])

    return pd.concat(dfs, ignore_index=True)