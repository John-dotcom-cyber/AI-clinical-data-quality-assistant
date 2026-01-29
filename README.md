# AI Clinical Data Quality Assistant (CDQA)

AI Clinical Data Quality Assistant is a tool designed to automatically detect, explain and prioritize data quality issues in patient-level clinical datasets.

##  Objectives
- Identify structural, temporal and physiological inconsistencies
- Provide clear explanations for each anomaly
- Compute a global and domain-specific data quality score
- Offer a simple interface to upload, analyze and visualize results

##  Features (V1)
- CSV ingestion and schema validation
- Detection of:
  - impossible physiological values
  - temporal inconsistencies
  - duplicated patient-level entries
  - referential integrity issues
- Quality scoring
- Streamlit interface

##  Tech Stack
- Python
- Pandas
- Streamlit
- Pydantic (schema validation)
- Pytest

##  Roadmap
### V1 — Core Engine + Streamlit UI
- Data ingestion
- Rule-based anomaly detection
- Quality scoring
- Basic UI

### V2 — Configurable Rules + Reporting
- YAML rule configuration
- PDF/HTML reports
- Severity levels

### V3 — ML-based Anomaly Detection
- Unsupervised anomaly detection
- Pattern learning from historical datasets

### V4 — API + Integration
- REST API
- Integration with clinical data pipelines

##  License
MIT License
