from pathlib import Path
from typing import Dict

import pandas as pd


REQUIRED_TABLES = ["patients", "visits", "labs"]


def load_csv_folder(folder_path: str) -> Dict[str, pd.DataFrame]:
    """
    Load required clinical tables (patients, visits, labs) from a folder of CSV files.

    Expected filenames:
    - patients.csv
    - visits.csv
    - labs.csv
    """
    folder = Path(folder_path)
    data = {}

    for table in REQUIRED_TABLES:
        file_path = folder / f"{table}.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required file: {file_path}")
        df = pd.read_csv(file_path)
        data[table] = df

    return data