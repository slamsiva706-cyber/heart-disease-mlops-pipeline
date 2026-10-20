"""Generates EDA visualizations for the cleaned Heart Disease dataset.

Run as a script: python -m src.data.eda
"""
# ruff: noqa: I001
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "data" / "processed" / "heart_disease_clean.csv"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs" / "eda"


def generate_eda(input_path: Path = DEFAULT_INPUT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> list[Path]:
    """Produce histogram, correlation heatmap, and class-balance plots; return saved file paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_path)
    saved = []

    numeric_df = df.drop(columns=["target"])
    fig, axes = plt.subplots(4, 4, figsize=(16, 12))
    for ax, column in zip(axes.flat, numeric_df.columns):
        ax.hist(numeric_df[column], bins=20, color="steelblue")
        ax.set_title(column)
    for ax in axes.flat[len(numeric_df.columns):]:
        ax.axis("off")
    fig.suptitle("Feature Distributions")
    fig.tight_layout()
    hist_path = output_dir / "histograms.png"
    fig.savefig(hist_path)
    plt.close(fig)
    saved.append(hist_path)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")
    fig.tight_layout()
    heatmap_path = output_dir / "correlation_heatmap.png"
    fig.savefig(heatmap_path)
    plt.close(fig)
    saved.append(heatmap_path)

    fig, ax = plt.subplots(figsize=(5, 4))
    df["target"].value_counts().sort_index().plot(kind="bar", ax=ax, color=["seagreen", "indianred"])
    ax.set_title("Class Balance (0 = No Disease, 1 = Disease)")
    ax.set_xlabel("target")
    ax.set_ylabel("count")
    fig.tight_layout()
    class_balance_path = output_dir / "class_balance.png"
    fig.savefig(class_balance_path)
    plt.close(fig)
    saved.append(class_balance_path)

    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    paths = generate_eda(args.input, args.output_dir)
    for path in paths:
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
