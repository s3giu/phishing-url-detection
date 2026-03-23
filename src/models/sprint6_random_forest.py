"""
Sprint 6: Random Forest Classifier (Ensemble Model)
Author: Sergiu Ionut Pascaru
Module: CMP600 – Dissertation

Objectives (Sprint 6):
1. Load the same stratified 80/20 train/test split used in Sprint 5.
2. Train a Random Forest classifier with hyperparameter tuning.
3. Evaluate with Confusion Matrix, Classification Report, and ROC Curve.
4. Report the False Positive Rate (FPR) and compare against LR baseline.
5. Save all evaluation artefacts to data/processed/.

CRISP-DM Phase: Modelling (Ensemble)
"""

import os
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    ConfusionMatrixDisplay,
)

FEATURES_PATH = "data/processed/features_sprint4.csv"
OUTPUT_DIR    = "data/processed"
RESULTS_FILE  = os.path.join(OUTPUT_DIR, "sprint6_results.txt")
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


def train_random_forest(X_train, y_train):
    """
    Random Forest with tuned hyperparameters:
    - n_estimators=200: enough trees for stable predictions
    - max_depth=20: prevents overfitting while capturing non-linear patterns
    - min_samples_leaf=5: smooths decision boundaries
    - class_weight='balanced': compensates for class imbalance
    - n_jobs=-1: uses all CPU cores for speed
    """
    print("\n[2/4] Training Random Forest (n_estimators=200, max_depth=20)...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    t0 = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - t0
    print(f"      Training complete in {elapsed:.2f}s")
    return model


def evaluate(model, X_test, y_test, feature_cols):
    print("\n[3/4] Evaluating Random Forest...")
    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

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
        f.write("SPRINT 6: RANDOM FOREST RESULTS\n")
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
        ax=ax, colorbar=True, cmap="Greens"
    )
    ax.set_title(
        f"Sprint 6: Random Forest – Confusion Matrix\n"
        f"Accuracy: {accuracy*100:.2f}%  |  FPR: {fpr_val*100:.2f}%  |  AUC: {roc_auc:.4f}",
        fontsize=10
    )
    plt.tight_layout()
    cm_path = os.path.join(OUTPUT_DIR, "09_sprint6_confusion_matrix.png")
    plt.savefig(cm_path, dpi=150)
    plt.close()

    # ROC Curve plot
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr_curve, tpr_curve, color="forestgreen", lw=2,
            label=f"Random Forest (AUC = {roc_auc:.4f})")
    ax.plot([0, 1], [0, 1], color="grey", lw=1, linestyle="--", label="Random classifier")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate (Recall)")
    ax.set_title("Sprint 6: ROC Curve – Random Forest")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    roc_path = os.path.join(OUTPUT_DIR, "10_sprint6_roc_curve.png")
    plt.savefig(roc_path, dpi=150)
    plt.close()

    # Feature Importance plot
    importances = model.feature_importances_
    imp_df = pd.DataFrame({"Feature": feature_cols, "Importance": importances})
    imp_df = imp_df.sort_values("Importance", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(imp_df["Feature"], imp_df["Importance"], color="forestgreen")
    ax.set_xlabel("Feature Importance (Gini)")
    ax.set_title("Sprint 6: Random Forest – Feature Importances")
    plt.tight_layout()
    imp_path = os.path.join(OUTPUT_DIR, "11_sprint6_feature_importances.png")
    plt.savefig(imp_path, dpi=150)
    plt.close()

    print(f"      Saved: {cm_path}")
    print(f"      Saved: {roc_path}")
    print(f"      Saved: {imp_path}")

    return {
        "accuracy": accuracy, "precision": precision,
        "recall": recall, "f1": f1, "fpr": fpr_val, "roc_auc": roc_auc,
        "TN": TN, "FP": FP, "FN": FN, "TP": TP,
        "fpr_curve": fpr_curve, "tpr_curve": tpr_curve,
    }


def run_sprint6_pipeline():
    print("=" * 60)
    print("SPRINT 6: RANDOM FOREST CLASSIFIER")
    print("=" * 60)
    X_train, X_test, y_train, y_test, feature_cols = load_and_split()
    model = train_random_forest(X_train, y_train)
    metrics = evaluate(model, X_test, y_test, feature_cols)
    print("\n[4/4] Sprint 6 complete.")
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
    run_sprint6_pipeline()
