import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure repo root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)

FEATURES_PATH = "data/processed/features_sprint4.csv"
PLOT_DIST = "data/processed/04_feature_distributions.png"
PLOT_CORR = "data/processed/05_feature_correlation.png"

PLOT_SAMPLE_N = 100_000
PLOT_RANDOM_STATE = 42


def main():
    print("=" * 70)
    print("SPRINT 4B: PLOT FEATURE DISTRIBUTIONS + CORRELATION")
    print("=" * 70)

    if not os.path.exists(FEATURES_PATH):
        raise FileNotFoundError(
            f"Missing {FEATURES_PATH}. Run build_features_sprint4.py first."
        )

    print(f"[1/4] Loading: {FEATURES_PATH}")
    Xy = pd.read_csv(FEATURES_PATH)
    print(f"      Rows: {len(Xy):,} | Cols: {len(Xy.columns)}")

    feature_cols = [c for c in Xy.columns if c != "label"]

    print("[2/4] Sampling for plots...")
    n = min(PLOT_SAMPLE_N, len(Xy))
    Xy_plot = Xy.sample(n=n, random_state=PLOT_RANDOM_STATE)
    print(f"      Plot sample: {len(Xy_plot):,} rows")

    print(f"[3/4] Saving: {PLOT_DIST}")
    os.makedirs(os.path.dirname(PLOT_DIST), exist_ok=True)
    plt.figure(figsize=(14, 10))
    for i, col in enumerate(feature_cols, 1):
        ax = plt.subplot(4, 3, i)
        sns.histplot(Xy_plot[col], bins=50, kde=False)
        ax.set_title(col)
    plt.tight_layout()
    plt.savefig(PLOT_DIST, dpi=300)
    plt.close()

    print(f"[4/4] Saving: {PLOT_CORR}")
    corr = Xy_plot[feature_cols].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.tight_layout()
    plt.savefig(PLOT_CORR, dpi=300)
    plt.close()

    print("=" * 70)
    print("Done: PNGs created.")
    print("=" * 70)


if __name__ == "__main__":
    main()
