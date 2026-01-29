import streamlit as st
import pandas as pd

from pathlib import Path
from typing import Dict

from src.rules.clinical_rules import run_all_rules
from src.scoring.quality_scoring import compute_quality_score


st.set_page_config(
    page_title="AI Clinical Data Quality Assistant",
    layout="wide",
)


st.title("AI Clinical Data Quality Assistant (CDQA)")
st.write("Upload your clinical CSV files and run an automated data quality analysis.")


def load_uploaded_files(uploaded_files) -> Dict[str, pd.DataFrame]:
    data = {}
    for f in uploaded_files:
        name = Path(f.name).stem.lower()
        if name in ["patients", "visits", "labs"]:
            data[name] = pd.read_csv(f)
    return data


with st.sidebar:
    st.header("Upload clinical data")
    uploaded_files = st.file_uploader(
        "Upload patients.csv, visits.csv, labs.csv",
        type=["csv"],
        accept_multiple_files=True,
    )

    run_button = st.button("Run quality analysis")


if run_button:
    if not uploaded_files:
        st.error("Please upload at least patients.csv, visits.csv and labs.csv.")
    else:
        data = load_uploaded_files(uploaded_files)

        missing = [t for t in ["patients", "visits", "labs"] if t not in data]
        if missing:
            st.error(f"Missing required tables: {', '.join(missing)}")
        else:
            st.success("Data loaded successfully. Running rules...")

            anomalies = run_all_rules(data)

            total_records = (
                len(data["patients"]) + len(data["visits"]) + len(data["labs"])
            )
            score = compute_quality_score(anomalies, total_records)

            st.subheader("Global data quality score")
            st.metric("Score", f"{score} / 100")

            st.subheader("Detected anomalies")
            if anomalies.empty:
                st.success("No anomalies detected with current rules.")
            else:
                st.dataframe(anomalies)