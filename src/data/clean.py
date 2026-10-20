"""Cleans the raw Heart Disease dataset: handles missing values and encodes target.

Run as a script: python -m src.data.clean
"""
import argparse
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "data" / "raw" / "heart_disease.csv"
DEFAULT_OUTPUT = REPO_ROOT / "data" / "processed" / "heart_disease_clean.csv"

NUMERIC_COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]


def clean(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT) -> pd.DataFrame:
    """Load raw data, drop rows with missing values, encode features, binarize target."""
    df = pd.read_csv(input_path, na_values="?")

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=NUMERIC_COLUMNS + ["target"]).reset_index(drop=True)

    # Original target is 0 (no disease) or 1-4 (presence, by severity); binarize to 0/1.
    df["target"] = (df["target"].astype(int) > 0).astype(int)

    for column in NUMERIC_COLUMNS:
        df[column] = df[column].astype(float)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    df = clean(args.input, args.output)
    print(f"Saved cleaned dataset ({len(df)} rows) to {args.output}")


if __name__ == "__main__":
    main()
