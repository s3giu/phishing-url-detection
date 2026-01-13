"""
Sprint 4: Lexical Feature Extraction (FAST / Vectorized)
Author: Sergiu Ionut Pascaru
Module: CMP600 - Dissertation

Description:
Extract lexical URL features (string-based only; no external lookups).

Features (10):
1) url_length
2) domain_length
3) path_length
4) digit_count
5) letter_count
6) special_char_count
7) digit_ratio
8) dot_count
9) slash_count
10) entropy (Shannon)
"""

import os
import math
import numpy as np
import pandas as pd
from collections import Counter


def calculate_entropy(url: str) -> float:
    """Shannon entropy of a URL string (0 if empty)."""
    s = "" if url is None else str(url)
    if len(s) == 0:
        return 0.0

    freq = Counter(s)
    n = len(s)

    ent = 0.0
    for c in freq.values():
        p = c / n
        if p > 0:
            ent -= p * math.log2(p)
    return float(ent)


def extract_features_dataframe(df: pd.DataFrame, url_column: str = "url") -> pd.DataFrame:
    """
    Fast extraction:
    - 9 features vectorized using pandas string ops (len/count/replace/split)
    - entropy computed with apply() (still the slowest, but acceptable)

    This implementation avoids urlparse() (faster, and avoids malformed URL parsing errors).
    """
    if url_column not in df.columns:
        raise KeyError(f"Missing '{url_column}' column in input DataFrame.")

    # Normalize
    s = df[url_column].astype(str).str.strip().str.lower()

    # Basic lengths
    url_length = s.str.len()

    # Remove scheme (http://, https://, etc.)
    no_scheme = s.str.replace(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", regex=True)

    # Domain extraction (approx, fast):
    # take part before first '/', remove userinfo, remove ports
    netloc = no_scheme.str.split("/", n=1).str[0].fillna("")
    netloc = netloc.str.split("@").str[-1]              # drop user:pass@
    netloc = netloc.str.replace(r"\]:\d+$", "]", regex=True)  # IPv6 + port
    netloc = netloc.str.replace(r":\d+$", "", regex=True)     # host:port

    domain_length = netloc.str.len()

    # Path extraction (after first '/'), stop at ? or #
    path_plus = no_scheme.str.split("/", n=1).str[1].fillna("")
    path_only = path_plus.str.split(r"[?#]", n=1).str[0].fillna("")
    path_length = path_only.str.len()

    # Counts (vectorized)
    digit_count = s.str.count(r"\d")
    letter_count = s.str.count(r"[a-z]")
    dot_count = s.str.count(r"\.")
    slash_count = s.str.count(r"/")

    # URL special chars count (your definition)
    special_char_pattern = r"[-_.~:/?#\[\]@!$&'()*+,;=%]"
    special_char_count = s.str.count(special_char_pattern)

    # Ratio
    digit_ratio = np.where(url_length > 0, digit_count / url_length, 0.0)

    # Entropy (per row)
    entropy = s.apply(calculate_entropy)

    features_df = pd.DataFrame({
        "url_length": url_length.astype(int),
        "domain_length": domain_length.astype(int),
        "path_length": path_length.astype(int),
        "digit_count": digit_count.astype(int),
        "letter_count": letter_count.astype(int),
        "special_char_count": special_char_count.astype(int),
        "digit_ratio": digit_ratio.astype(float),
        "dot_count": dot_count.astype(int),
        "slash_count": slash_count.astype(int),
        "entropy": entropy.astype(float),
    })

    return features_df


def build_feature_matrix(
    df: pd.DataFrame,
    url_column: str = "url",
    label_column: str = "label"
) -> pd.DataFrame:
    """
    Build model-ready matrix: 10 lexical features + label.
    Includes validation that output is numeric and has no missing values.
    """
    if label_column not in df.columns:
        raise KeyError(f"Missing '{label_column}' column in input DataFrame.")

    feats = extract_features_dataframe(df, url_column=url_column)
    feats["label"] = pd.to_numeric(df[label_column], errors="coerce").astype(int)

    if feats.isna().any().any():
        bad = feats.isna().sum().sort_values(ascending=False)
        raise ValueError(f"Validation failed: missing values present.\n{bad.head(10)}")

    return feats


def run_feature_pipeline(
    input_path: str = "data/processed/cleaned_urls_sprint3.csv",
    output_path: str = "data/processed/features_sprint4.csv"
) -> pd.DataFrame:
    """
    Script runner:
    Load cleaned URLs -> Extract features -> Save features_sprint4.csv
    """
    print("=" * 70)
    print("SPRINT 4: LEXICAL FEATURE EXTRACTION (FAST/VECTORIZED)")
    print("=" * 70)

    print(f"[1/3] Loading: {input_path}")
    df = pd.read_csv(input_path)
    print(f"      Rows: {len(df):,} | Cols: {len(df.columns)}")

    print("[2/3] Building feature matrix (10 features + label)...")
    Xy = build_feature_matrix(df, url_column="url", label_column="label")
    print(f"      Output shape: {Xy.shape[0]:,} x {Xy.shape[1]}")

    print(f"[3/3] Saving: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    Xy.to_csv(output_path, index=False)
    print("      Saved features_sprint4.csv")

    print("=" * 70)
    print("Sprint 4 feature extraction complete.")
    print("=" * 70)
    return Xy


if __name__ == "__main__":
    run_feature_pipeline()

