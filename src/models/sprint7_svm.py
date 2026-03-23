"""
Sprint 7: Support Vector Machine (SVM) Classifier
Author: Sergiu Ionut Pascaru
Module: CMP600 – Dissertation

Objectives (Sprint 7):
1. Load the same stratified 80/20 train/test split used in Sprints 5 & 6.
2. Train a LinearSVC (linear kernel SVM) — optimal for large datasets (500k+ rows).
   CalibratedClassifierCV wraps it to enable probability estimates for ROC curves.
3. Evaluate with Confusion Matrix, Classification Report, and ROC Curve.
4. Report the False Positive Rate (FPR) and compare against LR and RF baselines.
5. Save all evaluation artefacts to data/processed/.

Note on kernel choice:
   RBF/poly kernels require O(n²) memory for the kernel matrix — infeasible at 500k rows.
   LinearSVC scales as O(n) and is the standard choice for high-volume text/URL classification.
   This is consistent with the real-time, low-latency design goal of the dissertation.

CRISP-DM Phase: Modelling (Kernel-based)
"""

import os
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    ConfusionMatrixDisplay,
)

FEATURES_PATH = "data/processed/features_sprint4.csv"
OUTPUT_DIR    = "data/processed"
RESULTS_FILE  = os.path.join(OUTPUT_DIR, "sprint7_results.txt")
RANDOM_STATE  = 42
TEST_SIZE     = 0.20


def load_and_split():
    print("[1/4] Loading feature matrix and splitting data...")
    df = pd.read_csv(FEATURES_PATH)
    feature_cols = [c for c in df.columns if c != "label"]
    X = df[feature_cols].values
    y = df["label"].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"      Train: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")
    return X_train, X_test, y_train, y_test, feature_cols


def train_svm(X_train, y_train):
    """
    LinearSVC with CalibratedClassifierCV:
    - C=0.1: regularisation strength (tuned to reduce overfitting)
    - max_iter=2000: sufficient convergence for this dataset
    - class_weight='balanced': compensates for class imbalance
    - CalibratedClassifierCV: adds Platt scaling to produce probability estimates
    """
    print("\n[2/4] Training SVM (LinearSVC + calibration)...")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    base_svm = LinearSVC(
        C=0.1,
        max_iter=2000,
        class_weight="balanced",
        random_state=RANDOM_STATE,
    )
    # Wrap with calibration to get predict_proba (needed for ROC curve)
    model = CalibratedClassifierCV(base_svm, cv=3)

    t0 = time.time()
    model.fit(X_train_scaled, y_train)
    elapsed = time.time() - t0
    print(f"      Training complete in {elapsed:.2f}s")
    return model, scaler


def evaluate(model, scaler, X_test, y_test, feature_cols):
    print("\n[3/4] Evaluating SVM...")
    X_test_scaled = scaler.transform(X_test)
    y_pred  = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]

    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = cm.ravel()

    accuracy  = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    fpr_val   = FP / (FP + TN) if (FP + TN) > 0 else 0

    fpr_curve, tpr_curve, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr_curve, tpr_curve)

    report = classification_report(y_test, y_pred, target_names=["Benign (0)", "Malicious (1)"])

    print(f"      Accuracy  : {accuracy*100:.2f}%")
    print(f"      F1-Score  : {f1:.4f}")
    print(f"      FPR       : {fpr_val*100:.2f}%")
    print(f"      ROC AUC   : {roc_auc:.4f}")
    print(f"\n{report}")

    # Save results TXT
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("SPRINT 7: SVM (LinearSVC) RESULTS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"  TN: {TN:,}  FP: {FP:,}  FN: {FN:,}  TP: {TP:,}\n\n")
        f.write(f"  Accuracy  : {accuracy:.4f} ({accuracy*100:.2f}%)\n")
        f.write(f"  Precision : {precision:.4f}\n")
        f.write(f"  Recall    : {recall:.4f}\n")
        f.write(f"  F1-Score  : {f1:.4f}\n")
        f.write(f"  FPR       : {fpr_val:.4f} ({fpr_val*100:.2f}%)\n")
        f.write(f"  ROC AUC   : {roc_auc:.4f}\n\n")
        f.write(report + "\n")

    # Confusion Matrix plot
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay(cm, display_labels=["Benign (0)", "Malicious (1)"]).plot(
        ax=ax, colorbar=True, cmap="Oranges"
    )
    ax.set_title(
        f"Sprint 7: SVM (LinearSVC) – Confusion Matrix\n"
        f"Accuracy: {accuracy*100:.2f}%  |  FPR: {fpr_val*100:.2f}%  |  AUC: {roc_auc:.4f}",
        fontsize=10
    )
    plt.tight_layout()
    cm_path = os.path.join(OUTPUT_DIR, "12_sprint7_confusion_matrix.png")
    plt.savefig(cm_path, dpi=150)
    plt.close()

    # ROC Curve plot
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr_curve, tpr_curve, color="darkorange", lw=2,
            label=f"SVM LinearSVC (AUC = {roc_auc:.4f})")
    ax.plot([0, 1], [0, 1], color="grey", lw=1, linestyle="--", label="Random classifier")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate (Recall)")
    ax.set_title("Sprint 7: ROC Curve – SVM (LinearSVC)")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    roc_path = os.path.join(OUTPUT_DIR, "13_sprint7_roc_curve.png")
    plt.savefig(roc_path, dpi=150)
    plt.close()

    print(f"      Saved: {cm_path}")
    print(f"      Saved: {roc_path}")

    return {
        "accuracy": accuracy, "precision": precision,
        "recall": recall, "f1": f1, "fpr": fpr_val, "roc_auc": roc_auc,
        "TN": TN, "FP": FP, "FN": FN, "TP": TP,
        "fpr_curve": fpr_curve, "tpr_curve": tpr_curve,
    }


def run_sprint7_pipeline():
    print("=" * 60)
    print("SPRINT 7: SVM (LinearSVC) CLASSIFIER")
    print("=" * 60)
    X_train, X_test, y_train, y_test, feature_cols = load_and_split()
    model, scaler = train_svm(X_train, y_train)
    metrics = evaluate(model, scaler, X_test, y_test, feature_cols)
    print("\n[4/4] Sprint 7 complete.")
    print("=" * 60)
    print(f"  Accuracy : {metrics['accuracy']*100:.2f}%")
    print(f"  F1-Score : {metrics['f1']:.4f}")
    print(f"  FPR      : {metrics['fpr']*100:.2f}%")
    print(f"  ROC AUC  : {metrics['roc_auc']:.4f}")
    print("=" * 60)
    return metrics


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(repo_root)
    run_sprint7_pipeline()
