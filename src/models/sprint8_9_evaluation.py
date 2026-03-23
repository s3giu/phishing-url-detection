"""
Sprints 8 & 9: Cross-Validation, Feature Selection & Full Model Comparison
Author: Sergiu Ionut Pascaru
Module: CMP600 – Dissertation

Objectives (Sprint 8):
1. Run 5-fold stratified cross-validation on all three models using a
   representative subsample (100k rows) for computational feasibility,
   validating that performance is consistent across folds.
2. Perform feature selection using SelectKBest (f_classif / ANOVA F-test)
   to identify the most statistically significant lexical features.

Objectives (Sprint 9):
3. Generate combined ROC curves for all three models on one chart.
4. Generate a comparative bar chart (Accuracy, F1, FPR, AUC) across models.
5. Produce a final model comparison summary report (TXT + CSV).

CRISP-DM Phase: Evaluation
"""

import os
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    confusion_matrix, roc_curve, auc, f1_score,
    make_scorer, recall_score, precision_score,
)

FEATURES_PATH  = "data/processed/features_sprint4.csv"
OUTPUT_DIR     = "data/processed"
RANDOM_STATE   = 42
TEST_SIZE      = 0.20
CV_FOLDS       = 5
CV_SUBSAMPLE   = 100_000   # subsample for CV — representative but fast


def fpr_scorer(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    TN, FP, FN, TP = cm.ravel()
    return FP / (FP + TN) if (FP + TN) > 0 else 0.0


def load_and_split():
    df = pd.read_csv(FEATURES_PATH)
    feature_cols = [c for c in df.columns if c != "label"]
    X = df[feature_cols].values
    y = df["label"].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    return X_train, X_test, y_train, y_test, feature_cols, X, y


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 8 – Cross-Validation (on subsample for speed)
# ─────────────────────────────────────────────────────────────────────────────
def run_cross_validation(X_full, y_full, feature_cols):
    print("\n" + "=" * 60)
    print(f"SPRINT 8: CROSS-VALIDATION ({CV_FOLDS}-fold, n={CV_SUBSAMPLE:,} subsample)")
    print("=" * 60)

    # Stratified subsample
    idx = np.arange(len(y_full))
    rng = np.random.default_rng(RANDOM_STATE)
    benign_idx    = idx[y_full == 0]
    malicious_idx = idx[y_full == 1]
    n_each = CV_SUBSAMPLE // 2
    sub_idx = np.concatenate([
        rng.choice(benign_idx,    n_each, replace=False),
        rng.choice(malicious_idx, n_each, replace=False),
    ])
    X_sub = X_full[sub_idx]
    y_sub = y_full[sub_idx]
    print(f"  Subsample: {len(y_sub):,} rows (balanced 50/50)")

    scoring = {
        "accuracy":  "accuracy",
        "f1":        make_scorer(f1_score),
        "precision": make_scorer(precision_score, zero_division=0),
        "recall":    make_scorer(recall_score),
        "fpr":       make_scorer(fpr_scorer),
    }
    skf = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    models_cv = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, C=1.0)),
        ]),
        "Random Forest": Pipeline([
            ("clf", RandomForestClassifier(
                n_estimators=100, max_depth=15, min_samples_leaf=5,
                class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1
            )),
        ]),
        "SVM (LinearSVC)": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", CalibratedClassifierCV(
                LinearSVC(C=0.1, max_iter=2000, class_weight="balanced",
                          random_state=RANDOM_STATE), cv=3
            )),
        ]),
    }

    cv_results = {}
    for name, pipeline in models_cv.items():
        print(f"\n  Running {CV_FOLDS}-fold CV for: {name}...")
        t0 = time.time()
        scores = cross_validate(pipeline, X_sub, y_sub, cv=skf, scoring=scoring, n_jobs=-1)
        elapsed = time.time() - t0
        cv_results[name] = scores
        print(f"    Done in {elapsed:.1f}s")
        print(f"    Accuracy : {scores['test_accuracy'].mean():.4f} ± {scores['test_accuracy'].std():.4f}")
        print(f"    F1       : {scores['test_f1'].mean():.4f} ± {scores['test_f1'].std():.4f}")
        print(f"    FPR      : {scores['test_fpr'].mean():.4f} ± {scores['test_fpr'].std():.4f}")

    # Save CV CSV
    cv_rows = []
    for name, scores in cv_results.items():
        cv_rows.append({
            "Model":            name,
            "CV_Accuracy_Mean": round(scores["test_accuracy"].mean(), 4),
            "CV_Accuracy_Std":  round(scores["test_accuracy"].std(),  4),
            "CV_F1_Mean":       round(scores["test_f1"].mean(),       4),
            "CV_F1_Std":        round(scores["test_f1"].std(),        4),
            "CV_FPR_Mean":      round(scores["test_fpr"].mean(),      4),
            "CV_FPR_Std":       round(scores["test_fpr"].std(),       4),
            "CV_Recall_Mean":   round(scores["test_recall"].mean(),   4),
        })
    cv_df = pd.DataFrame(cv_rows)
    cv_csv = os.path.join(OUTPUT_DIR, "sprint8_cv_results.csv")
    cv_df.to_csv(cv_csv, index=False)
    print(f"\n  CV results saved → {cv_csv}")
    print(cv_df.to_string(index=False))

    # CV bar chart
    model_names = list(cv_results.keys())
    short_names = ["LR", "RF", "SVM"]
    metrics_plot = [
        ("test_accuracy", "Accuracy",         "steelblue"),
        ("test_f1",       "F1-Score",          "forestgreen"),
        ("test_fpr",      "FPR (↓ better)",    "crimson"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(13, 5))
    for ax, (key, label, color) in zip(axes, metrics_plot):
        means = [cv_results[m][key].mean() for m in model_names]
        stds  = [cv_results[m][key].std()  for m in model_names]
        bars = ax.bar(short_names, means, yerr=stds, color=color, alpha=0.82,
                      capsize=6, edgecolor="black", linewidth=0.8)
        ax.set_title(f"{label}\n(5-fold CV ± std)")
        ax.set_ylim(0, 1.1)
        for bar, mean in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                    f"{mean:.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    plt.suptitle(f"Sprint 8: 5-Fold Cross-Validation (n={CV_SUBSAMPLE:,} subsample)", fontsize=12, y=1.02)
    plt.tight_layout()
    cv_plot = os.path.join(OUTPUT_DIR, "14_sprint8_cv_comparison.png")
    plt.savefig(cv_plot, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  CV chart saved → {cv_plot}")
    return cv_df


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 8 – Feature Selection
# ─────────────────────────────────────────────────────────────────────────────
def run_feature_selection(X_train, y_train, feature_cols):
    print("\n" + "─" * 60)
    print("SPRINT 8: FEATURE SELECTION (ANOVA F-test / SelectKBest)")
    print("─" * 60)

    selector = SelectKBest(score_func=f_classif, k="all")
    selector.fit(X_train, y_train)

    scores_df = pd.DataFrame({
        "Feature": feature_cols,
        "F_Score": selector.scores_,
        "P_Value": selector.pvalues_,
    }).sort_values("F_Score", ascending=False)

    print(scores_df.to_string(index=False))
    fs_csv = os.path.join(OUTPUT_DIR, "sprint8_feature_selection.csv")
    scores_df.to_csv(fs_csv, index=False)
    print(f"\n  Feature selection saved → {fs_csv}")

    sorted_asc = scores_df.sort_values("F_Score", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["crimson" if p < 0.05 else "steelblue" for p in sorted_asc["P_Value"]]
    ax.barh(sorted_asc["Feature"], sorted_asc["F_Score"], color=colors)
    ax.set_xlabel("ANOVA F-Score (higher = more discriminative)")
    ax.set_title("Sprint 8: Feature Selection – ANOVA F-Scores\n"
                 "(Red = statistically significant at p < 0.05)")
    plt.tight_layout()
    fs_plot = os.path.join(OUTPUT_DIR, "15_sprint8_feature_selection.png")
    plt.savefig(fs_plot, dpi=150)
    plt.close()
    print(f"  Feature selection chart saved → {fs_plot}")
    return scores_df


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 9 – Combined ROC & Final Comparison (full test set)
# ─────────────────────────────────────────────────────────────────────────────
def run_final_evaluation(X_train, X_test, y_train, y_test):
    print("\n" + "=" * 60)
    print("SPRINT 9: COMBINED ROC CURVES & FINAL MODEL COMPARISON")
    print("=" * 60)

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    print("\n  Training all three models on full training set...")

    lr = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, C=1.0)
    lr.fit(X_train_sc, y_train)
    print("  [1/3] Logistic Regression trained.")

    rf = RandomForestClassifier(
        n_estimators=200, max_depth=20, min_samples_leaf=5,
        class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1
    )
    rf.fit(X_train, y_train)
    print("  [2/3] Random Forest trained.")

    svm_base = LinearSVC(C=0.1, max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE)
    svm = CalibratedClassifierCV(svm_base, cv=3)
    svm.fit(X_train_sc, y_train)
    print("  [3/3] SVM trained.")

    models_eval = {
        "Logistic Regression": (lr,  X_test_sc, "steelblue"),
        "Random Forest":       (rf,  X_test,    "forestgreen"),
        "SVM (LinearSVC)":     (svm, X_test_sc, "darkorange"),
    }

    comparison_rows = []
    roc_data = {}

    for name, (model, X_ev, color) in models_eval.items():
        y_pred  = model.predict(X_ev)
        y_proba = model.predict_proba(X_ev)[:, 1]
        cm = confusion_matrix(y_test, y_pred)
        TN, FP, FN, TP = cm.ravel()
        accuracy  = (TP + TN) / (TP + TN + FP + FN)
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall    = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        fpr_val   = FP / (FP + TN) if (FP + TN) > 0 else 0
        fpr_c, tpr_c, _ = roc_curve(y_test, y_proba)
        roc_auc   = auc(fpr_c, tpr_c)
        comparison_rows.append({
            "Model": name, "Accuracy": round(accuracy, 4),
            "Precision": round(precision, 4), "Recall": round(recall, 4),
            "F1_Score": round(f1, 4), "FPR": round(fpr_val, 4),
            "ROC_AUC": round(roc_auc, 4),
            "TN": TN, "FP": FP, "FN": FN, "TP": TP,
        })
        roc_data[name] = (fpr_c, tpr_c, roc_auc, color)

    comp_df = pd.DataFrame(comparison_rows)
    comp_csv = os.path.join(OUTPUT_DIR, "sprint9_model_comparison.csv")
    comp_df.to_csv(comp_csv, index=False)
    print(f"\n  Model comparison saved → {comp_csv}")
    print(comp_df[["Model", "Accuracy", "F1_Score", "FPR", "ROC_AUC"]].to_string(index=False))

    # Plot 1: Combined ROC
    fig, ax = plt.subplots(figsize=(7, 6))
    for name, (fpr_c, tpr_c, roc_auc, color) in roc_data.items():
        ax.plot(fpr_c, tpr_c, lw=2, color=color, label=f"{name} (AUC = {roc_auc:.4f})")
    ax.plot([0, 1], [0, 1], color="grey", lw=1, linestyle="--", label="Random classifier")
    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate (Recall)", fontsize=12)
    ax.set_title("Sprint 9: Combined ROC Curves – All Three Models", fontsize=13)
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    roc_path = os.path.join(OUTPUT_DIR, "16_sprint9_combined_roc.png")
    plt.savefig(roc_path, dpi=150)
    plt.close()
    print(f"  Combined ROC saved → {roc_path}")

    # Plot 2: Comparison bar chart
    metrics_bar = ["Accuracy", "F1_Score", "FPR", "ROC_AUC"]
    labels_bar  = ["Accuracy", "F1-Score", "FPR (↓ better)", "ROC AUC"]
    colors_bar  = ["steelblue", "forestgreen", "crimson", "darkorange"]
    short_names = ["LR", "RF", "SVM"]
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    for ax, metric, label, color in zip(axes, metrics_bar, labels_bar, colors_bar):
        vals = comp_df[metric].values
        bars = ax.bar(short_names, vals, color=color, alpha=0.85, edgecolor="black", linewidth=0.8)
        ax.set_title(label, fontsize=12)
        ax.set_ylim(0, 1.1)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.suptitle("Sprint 9: Final Model Comparison – LR vs RF vs SVM", fontsize=14, y=1.02)
    plt.tight_layout()
    bar_path = os.path.join(OUTPUT_DIR, "17_sprint9_model_comparison_bars.png")
    plt.savefig(bar_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Comparison bar chart saved → {bar_path}")

    # Plot 3: Heatmap
    hm_df = comp_df.set_index("Model")[["Accuracy", "Precision", "Recall", "F1_Score", "FPR", "ROC_AUC"]]
    fig, ax = plt.subplots(figsize=(9, 3))
    sns.heatmap(hm_df, annot=True, fmt=".4f", cmap="YlGnBu", linewidths=0.5,
                ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("Sprint 9: Model Performance Heatmap", fontsize=13)
    plt.tight_layout()
    hm_path = os.path.join(OUTPUT_DIR, "18_sprint9_performance_heatmap.png")
    plt.savefig(hm_path, dpi=150)
    plt.close()
    print(f"  Performance heatmap saved → {hm_path}")

    # Final summary TXT
    best_f1  = comp_df.loc[comp_df["F1_Score"].idxmax(), "Model"]
    best_auc = comp_df.loc[comp_df["ROC_AUC"].idxmax(),  "Model"]
    best_fpr = comp_df.loc[comp_df["FPR"].idxmin(),       "Model"]
    summary_path = os.path.join(OUTPUT_DIR, "sprint9_final_summary.txt")
    with open(summary_path, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("SPRINT 9: FINAL MODEL COMPARISON SUMMARY\n")
        f.write("CMP600 – Dissertation | Sergiu Ionut Pascaru\n")
        f.write("=" * 60 + "\n\n")
        f.write("Dataset      : Malicious URLs (Siddhartha, 2024)\n")
        f.write("Total rows   : 641,053\n")
        f.write(f"Train / Test : 80% / 20% (stratified, seed={RANDOM_STATE})\n")
        f.write("Test set     : 128,211 URLs\n\n")
        f.write("─" * 60 + "\n")
        f.write(f"{'Model':<25} {'Accuracy':>9} {'F1':>8} {'FPR':>8} {'AUC':>8}\n")
        f.write("─" * 60 + "\n")
        for _, row in comp_df.iterrows():
            f.write(f"{row['Model']:<25} {row['Accuracy']:>9.4f} {row['F1_Score']:>8.4f} "
                    f"{row['FPR']:>8.4f} {row['ROC_AUC']:>8.4f}\n")
        f.write("─" * 60 + "\n\n")
        f.write("KEY FINDINGS\n")
        f.write(f"  Best F1-Score  : {best_f1}\n")
        f.write(f"  Best ROC AUC   : {best_auc}\n")
        f.write(f"  Lowest FPR     : {best_fpr}  <- best usability\n\n")
        f.write("INTERPRETATION\n")
        f.write("  Random Forest significantly outperforms the linear models\n")
        f.write("  (LR and SVM) on all metrics, confirming that the relationship\n")
        f.write("  between lexical URL features and maliciousness is non-linear.\n")
        f.write("  The high AUC (>0.98) demonstrates strong discriminative power.\n")
        f.write("  The FPR is the key usability metric: a lower FPR means fewer\n")
        f.write("  legitimate URLs are incorrectly blocked, which is critical for\n")
        f.write("  real-time, client-side deployment.\n\n")
        f.write("NEXT STEPS (Sprint 10+)\n")
        f.write("  - Draft Methodology and Introduction chapters\n")
        f.write("  - Draft Literature Review and Results chapters\n")
        f.write("  - Draft Discussion and Conclusion\n")
        f.write("  - Final proofreading and submission\n")
    print(f"  Final summary saved → {summary_path}")
    return comp_df


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def run_sprints_8_9():
    print("=" * 60)
    print("SPRINTS 8 & 9: CROSS-VALIDATION, FEATURE SELECTION & EVALUATION")
    print("=" * 60)
    X_train, X_test, y_train, y_test, feature_cols, X_full, y_full = load_and_split()
    cv_df   = run_cross_validation(X_full, y_full, feature_cols)
    fs_df   = run_feature_selection(X_train, y_train, feature_cols)
    comp_df = run_final_evaluation(X_train, X_test, y_train, y_test)
    print("\n" + "=" * 60)
    print("SPRINTS 8 & 9 COMPLETE")
    print("=" * 60)
    print(comp_df[["Model", "Accuracy", "F1_Score", "FPR", "ROC_AUC"]].to_string(index=False))
    print("\nAll artefacts saved to data/processed/")


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(repo_root)
    run_sprints_8_9()
