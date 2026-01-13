import os
import sys
import pandas as pd

# Ensure repo root is on sys.path (so "import src...." works)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)

from src.features.lexical_features import build_feature_matrix

INPUT_PATH = "data/processed/cleaned_urls_sprint3.csv"
OUTPUT_PATH = "data/processed/features_sprint4.csv"


def main():
    print("=" * 70)
    print("SPRINT 4A: BUILD FEATURES CSV")
    print("=" * 70)

    print(f"[1/3] Loading: {INPUT_PATH}")
    df = pd.read_csv(INPUT_PATH)
    print(f"      Rows: {len(df):,}")

    print("[2/3] Building feature matrix...")
    Xy = build_feature_matrix(df, url_column="url", label_column="label")
    print(f"      Output shape: {Xy.shape[0]:,} x {Xy.shape[1]}")

    print(f"[3/3] Saving: {OUTPUT_PATH}")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    Xy.to_csv(OUTPUT_PATH, index=False)

    print("=" * 70)
    print("Done: data/processed/features_sprint4.csv created.")
    print("=" * 70)


if __name__ == "__main__":
    main()
