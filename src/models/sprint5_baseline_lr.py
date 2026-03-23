"""
Sprint 5: Baseline Model – Logistic Regression
Author: Sergiu Ionut Pascaru
Module: CMP600 – Dissertation

Objectives (Sprint 5):
1. Load the feature matrix produced by Sprint 4 (features_sprint4.csv).
2. Split the data into Training (80%) and Testing (20%) sets with stratification.
3. Train a Logistic Regression baseline classifier.
4. Evaluate with Confusion Matrix, Classification Report, and ROC Curve.
5. Report the False Positive Rate (FPR) as the key usability metric.
6. Save all evaluation artefacts (PNG plots + results TXT) to data/processed/.

CRISP-DM Phase: Modelling (Baseline)
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for server/script use
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    ConfusionMatrixDisplay,
)
from sklearn.preprocessing import StandardScaler

# ─────────────────────────────────────────────
# Paths (repo-relative)
# ─────────────────────────────────────────────
FEATURES_PATH = "data/processed/features_sprint4.csv"
OUTPUT_DIR    = "data/processed"
RESULTS_FILE  = os.path.join(OUTPUT_DIR, "sprint5_results.txt")

RANDOM_STATE  = 42
TEST_SIZE     = 0.20   # 80 / 20 split


def load_features(path: str) -> pd.DataFrame:
    print(f"[1/5] Loading feature matrix: {path}")
    df = pd.read_csv(path)
    print(f"      Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"      Label distribution:\n{df['label'].value_counts().to_string()}")
    return df


def split_data(df: pd.DataFrame):
    """
    Stratified 80/20 train/test split.
    Stratification ensures the class ratio is preserved in both sets,
    which is critical given the class imbalance (benign ~67%, malicious ~33%).
    """
    print(f"\n[2/5] Splitting data (train={int((1-TEST_SIZE)*100)}% / test={int(TEST_SIZE*100)}%, stratified)...")

    feature_cols = [c for c in df.columns if c != "label"]
    X = df[feature_cols].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    print(f"      Training set : {X_train.shape[0]:,} rows")
    print(f"      Testing set  : {X_test.shape[0]:,} rows")
    print(f"      Train label dist – Benign: {(y_train==0).sum():,} | Malicious: {(y_train==1).sum():,}")
    print(f"      Test  label dist – Benign: {(y_test==0).sum():,}  | Malicious: {(y_test==1).sum():,}")

    return X_train, X_test, y_train, y_test, feature_cols


def train_logistic_regression(X_train, y_train):
    """
    Train a Logistic Regression model.
    Features are standardised (zero mean, unit variance) before training
    because Logistic Regression is sensitive to feature scale.
    """
    print("\n[3/5] Training Logistic Regression (baseline)...")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE,
        solver="lbfgs",
        C=1.0
    )

    t0 = time.time()
    model.fit(X_train_scaled, y_train)
    elapsed = time.time() - t0

    print(f"      Training complete in {elapsed:.2f}s")
    print(f"      Solver: {model.solver} | Iterations: {model.n_iter_[0]}")

    return model, scaler


def evaluate_model(model, scaler, X_test, y_test, feature_cols, out_dir: str):
    """
    Full evaluation:
    - Confusion Matrix (with FPR highlighted)
    - Classification Report
    - ROC Curve + AUC
    - Feature Coefficients bar chart
    """
    print("\n[4/5] Evaluating model...")

    X_test_scaled = scaler.transform(X_test)
    y_pred  = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]

    # ── Confusion Matrix values ──────────────────────────────────────────
    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = cm.ravel()

    accuracy  = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    fpr       = FP / (FP + TN) if (FP + TN) > 0 else 0   # KEY METRIC

    print(f"\n      ── Confusion Matrix ──────────────────")
    print(f"      TN (correct benign)  : {TN:,}")
    print(f"      FP (benign → malicious): {FP:,}  ← False Positives")
    print(f"      FN (missed malicious): {FN:,}")
    print(f"      TP (correct malicious): {TP:,}")
    print(f"\n      ── Key Metrics ───────────────────────")
    print(f"      Accuracy  : {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"      Precision : {precision:.4f}")
    print(f"      Recall    : {recall:.4f}")
    print(f"      F1-Score  : {f1:.4f}")
    print(f"      FPR       : {fpr:.4f} ({fpr*100:.2f}%)  ← KEY USABILITY METRIC")

    report = classification_report(y_test, y_pred, target_names=["Benign (0)", "Malicious (1)"])
    print(f"\n      Classification Report:\n{report}")

    # ── ROC Curve ────────────────────────────────────────────────────────
    fpr_curve, tpr_curve, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr_curve, tpr_curve)
    print(f"      ROC AUC   : {roc_auc:.4f}")

    # ── Save results TXT ─────────────────────────────────────────────────
    os.makedirs(out_dir, exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("SPRINT 5: LOGISTIC REGRESSION BASELINE RESULTS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Dataset       : {FEATURES_PATH}\n")
        f.write(f"Train/Test    : {int((1-TEST_SIZE)*100)}% / {int(TEST_SIZE*100)}% (stratified)\n")
        f.write(f"Random State  : {RANDOM_STATE}\n\n")
        f.write("── Confusion Matrix ──────────────────────────────────\n")
        f.write(f"  TN (correct benign)    : {TN:,}\n")
        f.write(f"  FP (benign→malicious)  : {FP:,}  ← False Positives\n")
        f.write(f"  FN (missed malicious)  : {FN:,}\n")
        f.write(f"  TP (correct malicious) : {TP:,}\n\n")
        f.write("── Key Metrics ───────────────────────────────────────\n")
        f.write(f"  Accuracy   : {accuracy:.4f} ({accuracy*100:.2f}%)\n")
        f.write(f"  Precision  : {precision:.4f}\n")
        f.write(f"  Recall     : {recall:.4f}\n")
        f.write(f"  F1-Score   : {f1:.4f}\n")
        f.write(f"  FPR        : {fpr:.4f} ({fpr*100:.2f}%)  ← KEY USABILITY METRIC\n")
        f.write(f"  ROC AUC    : {roc_auc:.4f}\n\n")
        f.write("── Classification Report ─────────────────────────────\n")
        f.write(report + "\n")
    print(f"\n      Results saved → {RESULTS_FILE}")

    # ── Plot 1: Confusion Matrix ──────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Benign (0)", "Malicious (1)"])
    disp.plot(ax=ax, colorbar=True, cmap="Blues")
    ax.set_title(
        f"Sprint 5: Logistic Regression – Confusion Matrix\n"
        f"Accuracy: {accuracy*100:.2f}%  |  FPR: {fpr*100:.2f}%  |  AUC: {roc_auc:.4f}",
        fontsize=10
    )
    plt.tight_layout()
    cm_path = os.path.join(out_dir, "06_sprint5_confusion_matrix.png")
    plt.savefig(cm_path, dpi=150)
    plt.close()
    print(f"      Confusion Matrix plot saved → {cm_path}")

    # ── Plot 2: ROC Curve ─────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr_curve, tpr_curve, color="steelblue", lw=2,
            label=f"Logistic Regression (AUC = {roc_auc:.4f})")
    ax.plot([0, 1], [0, 1], color="grey", lw=1, linestyle="--", label="Random classifier")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate (Recall)")
    ax.set_title("Sprint 5: ROC Curve – Logistic Regression Baseline")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    roc_path = os.path.join(out_dir, "07_sprint5_roc_curve.png")
    plt.savefig(roc_path, dpi=150)
    plt.close()
    print(f"      ROC Curve plot saved → {roc_path}")

    # ── Plot 3: Feature Coefficients ──────────────────────────────────────
    coefs = model.coef_[0]
    coef_df = pd.DataFrame({
        "Feature": feature_cols,
        "Coefficient": coefs
    }).sort_values("Coefficient", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["crimson" if c > 0 else "steelblue" for c in coef_df["Coefficient"]]
    ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Coefficient Value (positive = more malicious)")
    ax.set_title("Sprint 5: Logistic Regression – Feature Coefficients\n"
                 "(Red = increases malicious probability, Blue = decreases it)")
    plt.tight_layout()
    coef_path = os.path.join(out_dir, "08_sprint5_feature_coefficients.png")
    plt.savefig(coef_path, dpi=150)
    plt.close()
    print(f"      Feature Coefficients plot saved → {coef_path}")

    return {
        "accuracy": accuracy, "precision": precision,
        "recall": recall, "f1": f1, "fpr": fpr, "roc_auc": roc_auc,
        "TN": TN, "FP": FP, "FN": FN, "TP": TP
    }


def run_sprint5_pipeline():
    print("=" * 60)
    print("SPRINT 5: BASELINE MODEL – LOGISTIC REGRESSION")
    print("=" * 60)

    df = load_features(FEATURES_PATH)
    X_train, X_test, y_train, y_test, feature_cols = split_data(df)
    model, scaler = train_logistic_regression(X_train, y_train)
    metrics = evaluate_model(model, scaler, X_test, y_test, feature_cols, OUTPUT_DIR)

    print("\n[5/5] Sprint 5 complete.")
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Accuracy  : {metrics['accuracy']*100:.2f}%")
    print(f"  F1-Score  : {metrics['f1']:.4f}")
    print(f"  FPR       : {metrics['fpr']*100:.2f}%  ← baseline to beat in Sprints 6 & 7")
    print(f"  ROC AUC   : {metrics['roc_auc']:.4f}")
    print("=" * 60)
    print("Artefacts saved to data/processed/:")
    print("  sprint5_results.txt")
    print("  06_sprint5_confusion_matrix.png")
    print("  07_sprint5_roc_curve.png")
    print("  08_sprint5_feature_coefficients.png")
    print("=" * 60)
    return metrics


if __name__ == "__main__":
    # Allow running from repo root: python src/models/sprint5_baseline_lr.py
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(repo_root)
    run_sprint5_pipeline()
