"""Downloads the raw UCI Heart Disease (Cleveland) dataset.

Run as a script: python -m src.data.download
"""
import argparse
from pathlib import Path

import requests

UCI_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target",
]
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPO_ROOT / "data" / "raw" / "heart_disease.csv"


def download(output_path: Path = DEFAULT_OUTPUT, url: str = UCI_URL) -> Path:
    """Fetch the raw dataset and write it as a headered CSV at output_path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    header = ",".join(COLUMNS)
    body = response.text.strip()
    output_path.write_text(f"{header}\n{body}\n", encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--url", type=str, default=UCI_URL)
    args = parser.parse_args()
    path = download(args.output, args.url)
    print(f"Saved raw dataset to {path}")


if __name__ == "__main__":
    main()
