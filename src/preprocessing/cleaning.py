"""
Sprint 3: Data Cleaning + Tokenization + Label Binarization (+ Evidence PNGs)
Author: Sergiu Ionut Pascaru
Module: CMP600 - Dissertation

Purpose (Sprint 3 objectives):
- Clean and standardize URL strings (remove missing, trim, lowercase, deduplicate).
- Tokenize URLs into components (domain/path/query/fragment) for later feature engineering.
- Convert the dataset’s multi-class labels into a binary target suitable for real-time detection:
    benign -> 0 (safe)
    phishing/defacement/malware -> 1 (malicious)
- Generate evidence plots (PNG) for Sprint 3 reporting, similar to Sprint 2.

Dataset (local, repo-relative):
- File: data/raw/malicious_phish.csv
- Columns expected: url, type
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlparse


# ---------------------------------------------------------------------
# Configuration: repo-relative paths
# ---------------------------------------------------------------------
RAW_DATA_PATH = "data/raw/malicious_phish.csv"
OUTPUT_PATH = "data/processed/cleaned_urls_sprint3.csv"
PLOTS_DIR = "data/processed"


# ---------------------------------------------------------------------
# Step 1: Load
# ---------------------------------------------------------------------
def load_raw_data(filepath: str = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Load the raw Malicious URLs dataset from CSV.

    Returns:
        pd.DataFrame with at least:
            - url: URL string
            - type: class label (benign/phishing/defacement/malware)
    """
    print(f"[1/6] Loading raw data: {filepath}")
    df = pd.read_csv(filepath)

    print(f"      Loaded: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"      Columns: {df.columns.tolist()}")

    required = {"url", "type"}
    missing = required - set(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}. Found: {df.columns.tolist()}")

    return df


# ---------------------------------------------------------------------
# Step 2: Clean URLs
# ---------------------------------------------------------------------
def clean_urls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize URL strings.

    Operations:
    - Drop missing URLs
    - Strip whitespace
    - Lowercase
    - Remove empty strings
    - Drop duplicate URLs

    Why:
    - Improves consistency and reduces noise for downstream tokenization/feature extraction.
    - Prevents duplicates from biasing evaluation.
    """
    print("[2/6] Cleaning URLs...")

    initial = len(df)
    df_clean = df.copy()

    df_clean = df_clean.dropna(subset=["url"])
    df_clean["url"] = df_clean["url"].astype(str).str.strip().str.lower()
    df_clean = df_clean[df_clean["url"] != ""]
    df_clean = df_clean.drop_duplicates(subset=["url"])

    final = len(df_clean)
    removed = initial - final

    print(f"      Initial: {initial:,}")
    print(f"      Final:   {final:,}")
    print(f"      Removed: {removed:,} ({(removed/initial*100):.2f}%)")

    return df_clean


# ---------------------------------------------------------------------
# Step 3: Binarize labels
# ---------------------------------------------------------------------
def binarize_labels(df: pd.DataFrame, label_column: str = "type") -> pd.DataFrame:
    """
    Convert multi-class labels into binary.

    Mapping:
    - benign -> 0
    - phishing/defacement/malware -> 1
    """
    print("[3/6] Binarizing labels...")

    df_bin = df.copy()
    df_bin[label_column] = df_bin[label_column].astype(str).str.strip().str.lower()
    df_bin["label"] = df_bin[label_column].apply(lambda x: 0 if x == "benign" else 1)

    total = len(df_bin)
    benign = int((df_bin["label"] == 0).sum())
    malicious = int((df_bin["label"] == 1).sum())

    print("      Binary label distribution:")
    print(f"      Benign (0):    {benign:,} ({benign/total*100:.2f}%)")
    print(f"      Malicious (1): {malicious:,} ({malicious/total*100:.2f}%)")

    return df_bin


# ---------------------------------------------------------------------
# Step 4: Tokenize URLs (safe parsing)
# ---------------------------------------------------------------------
def basic_tokenization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tokenize each URL into:
    - domain
    - path
    - query
    - fragment

    Robustness:
    - urlparse() can raise exceptions for malformed inputs (e.g., Invalid IPv6 URL).
    - This function catches exceptions so the pipeline never crashes.
    - Rows that fail parsing get empty tokens + parse_failed=1.
    """
    print("[4/6] Tokenizing URLs (domain/path/query/fragment)...")

    df_tok = df.copy()

    def parse_one(u: str):
        try:
            u = str(u)
            u_for_parse = u if "://" in u else "http://" + u
            p = urlparse(u_for_parse)
            return p.netloc, p.path, p.query, p.fragment, 0
        except Exception:
            return "", "", "", "", 1

    parts = df_tok["url"].apply(parse_one)
    df_tok["domain"] = parts.apply(lambda x: x[0])
    df_tok["path"] = parts.apply(lambda x: x[1])
    df_tok["query"] = parts.apply(lambda x: x[2])
    df_tok["fragment"] = parts.apply(lambda x: x[3])
    df_tok["parse_failed"] = parts.apply(lambda x: x[4])

    failed = int(df_tok["parse_failed"].sum())
    print(f"      Tokenization completed. parse_failed rows: {failed:,}")

    print("      Example tokens:")
    print(df_tok[["url", "domain", "path"]].head(3))

    return df_tok


# ---------------------------------------------------------------------
# Step 5: Save Sprint 3 plots (PNG)
# ---------------------------------------------------------------------
def save_sprint3_plots(df: pd.DataFrame, out_dir: str = PLOTS_DIR) -> None:
    """
    Save Sprint 3 evidence plots as PNG files in data/processed/.

    Plots:
    03_binary_label_distribution.png  -> counts of label 0/1
    04_parse_failed_distribution.png  -> counts of parse_failed 0/1
    05_url_length_by_label.png        -> boxplot of url_length grouped by label
    """
    print("[5/6] Saving Sprint 3 plots (PNG)...")
    os.makedirs(out_dir, exist_ok=True)

    # Plot 1: binary label distribution
    plt.figure(figsize=(6, 4))
    df["label"].value_counts().sort_index().plot(kind="bar", color=["seagreen", "crimson"])
    plt.title("Sprint 3: Binary label distribution")
    plt.xlabel("Label (0=benign, 1=malicious)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "03_binary_label_distribution.png"), dpi=300)
    plt.close()

    # Plot 2: tokenization parse failures
    plt.figure(figsize=(6, 4))
    df["parse_failed"].value_counts().sort_index().plot(kind="bar", color=["steelblue", "orange"])
    plt.title("Sprint 3: URL parse failures")
    plt.xlabel("parse_failed (0=ok, 1=failed)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "04_parse_failed_distribution.png"), dpi=300)
    plt.close()

    # Plot 3: URL length by label (boxplot)
    df_plot = df.copy()
    df_plot["url_length"] = df_plot["url"].astype(str).str.len()

    ax = df_plot.boxplot(column="url_length", by="label", figsize=(6, 4))
    ax.set_title("Sprint 3: URL length by label")
    ax.set_xlabel("Label (0=benign, 1=malicious)")
    ax.set_ylabel("URL length (characters)")
    plt.suptitle("")  # remove pandas automatic grouped-title
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "05_url_length_by_label.png"), dpi=300)
    plt.close()

    print("      Saved plots:")
    print(f"      - {os.path.join(out_dir, '03_binary_label_distribution.png')}")
    print(f"      - {os.path.join(out_dir, '04_parse_failed_distribution.png')}")
    print(f"      - {os.path.join(out_dir, '05_url_length_by_label.png')}")


# ---------------------------------------------------------------------
# Step 6: Save processed CSV
# ---------------------------------------------------------------------
def save_processed_data(df: pd.DataFrame, filepath: str = OUTPUT_PATH) -> None:
    """
    Save processed DataFrame to CSV in data/processed.

    Output includes:
    - original columns: url, type
    - derived columns: label, domain, path, query, fragment, parse_failed
    """
    print(f"[6/6] Saving processed data: {filepath}")

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)

    print(f"      Saved: {len(df):,} rows")


# ---------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------
def run_cleaning_pipeline(
    input_path: str = RAW_DATA_PATH,
    output_path: str = OUTPUT_PATH
) -> pd.DataFrame:
    """
    Run the full Sprint 3 pipeline end-to-end:
    Load -> Clean -> Binarize -> Tokenize -> Save PNGs -> Save CSV
    """
    print("=" * 70)
    print("SPRINT 3: DATA CLEANING + TOKENIZATION + BINARY LABELS (+ PNGs)")
    print("=" * 70)

    df = load_raw_data(input_path)
    df = clean_urls(df)
    df = binarize_labels(df, label_column="type")
    df = basic_tokenization(df)
    save_sprint3_plots(df)
    save_processed_data(df, output_path)

    print("\nValidation checks:")
    print(f"- Null urls: {int(df['url'].isna().sum())}")
    print(f"- Unique binary labels: {sorted(df['label'].unique())}")
    print(f"- parse_failed total: {int(df['parse_failed'].sum())}")

    print("=" * 70)
    print("Sprint 3 complete. Output ready for Sprint 4 feature engineering.")
    print("=" * 70)

    return df


if __name__ == "__main__":
    run_cleaning_pipeline()
