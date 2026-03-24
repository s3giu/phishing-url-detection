# Phishing URL Detection – CMP600 Dissertation

**Author:** Sergiu Ionut Pascaru (Student ID: 2310-111729)  
**Module:** CMP600 – Dissertation  
**Institution:** Newcastle College Group (University of Northumbria)  
**Supervisor:** Oti Edema  
**Timeline:** November 2025 – May 2026  
**Status:** ✅ Sprints 1–9 Complete | 🔄 Sprint 10 (Dissertation Write-up) In Progress

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Research Question](#research-question)
3. [Dataset](#dataset)
4. [Methodology](#methodology)
5. [Project Structure](#project-structure)
6. [Getting Started](#getting-started)
7. [Sprint Progress](#sprint-progress)
8. [Results Summary](#results-summary)
9. [Key Findings](#key-findings)
10. [References](#references)

---

## Project Overview

This project implements a machine learning pipeline to detect phishing URLs in real time using **lexical URL features only** — structural and statistical properties extracted directly from the URL string, without querying any external services, DNS lookups, or page content analysis.

The core motivation is to build a **client-side, real-time phishing detector** that can operate with minimal latency. By relying solely on lexical features, the model can classify a URL in milliseconds, making it suitable for browser extensions, email filters, and network-level security tools.

The study follows the **CRISP-DM** (Cross-Industry Standard Process for Data Mining) framework and compares three machine learning classifiers:

| Classifier | Type | Rationale |
|---|---|---|
| Logistic Regression | Linear baseline | Establishes a performance floor; interpretable coefficients |
| Random Forest | Non-linear ensemble | Captures complex feature interactions; robust to noise |
| SVM (LinearSVC) | Kernel-based linear | Strong theoretical foundations; comparison with LR |

---

## Research Question

> *"Can machine learning models trained exclusively on lexical URL features achieve sufficiently low False Positive Rates (FPR) for real-time, client-side phishing detection?"*

The **False Positive Rate (FPR)** is the primary evaluation metric, as falsely blocking legitimate URLs is a critical usability failure in real-world deployment.

---

## Dataset

**Malicious URLs Dataset** — Siddhartha (2024), Kaggle  
Source: https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset

| Property | Value |
|---|---|
| Raw records | 651,191 URLs |
| After cleaning | 641,053 URLs |
| Original classes | benign, phishing, defacement, malware |
| Binary target | benign (0) vs malicious (1) |
| Class distribution | ~57% benign, ~43% malicious |
| Train / Test split | 80% / 20% stratified (seed=42) |
| Training set | 512,842 URLs |
| Test set | 128,211 URLs |

---

## Methodology

**Framework:** CRISP-DM (Chapman et al., 2000)

```
Sprint 1  → Business Understanding   (project setup, tools, proposal)
Sprint 2  → Data Understanding       (EDA, distributions, class balance)
Sprint 3  → Data Preparation         (cleaning, deduplication, binarization)
Sprint 4  → Data Preparation         (lexical feature engineering → 10 features)
Sprint 5  → Modelling                (Logistic Regression baseline)
Sprint 6  → Modelling                (Random Forest)
Sprint 7  → Modelling                (SVM / LinearSVC)
Sprint 8  → Evaluation               (5-fold cross-validation, ANOVA feature selection)
Sprint 9  → Evaluation               (final comparison, combined ROC curves, heatmap)
Sprint 10+→ Deployment               (dissertation write-up, submission)
```

### Feature Engineering (Sprint 4)

Ten lexical features were extracted from each URL string:

| Feature | Description |
|---|---|
| `url_length` | Total character length of the URL |
| `domain_length` | Character length of the domain component |
| `path_length` | Character length of the URL path |
| `dot_count` | Number of dots (`.`) in the full URL |
| `slash_count` | Number of forward slashes (`/`) |
| `digit_count` | Number of numeric digits |
| `digit_ratio` | Ratio of digits to total characters |
| `letter_count` | Number of alphabetic characters |
| `special_char_count` | Count of special characters (`@`, `-`, `_`, `=`, `?`, `&`, `%`) |
| `entropy` | Shannon entropy of the URL string (measures randomness/obfuscation) |

---

## Project Structure

```
phishing-url-detection/
├── data/
│   ├── raw/                          # Original Kaggle CSV (not tracked in git)
│   └── processed/                    # Cleaned data, feature matrix, all plots
│       ├── features_sprint4.csv      # 641,053 × 10 feature matrix (ML input)
│       ├── 01_label_distribution.png
│       ├── 02_url_length_distribution.png
│       ├── 03_binary_label_distribution.png
│       ├── 04_feature_distributions.png
│       ├── 05_feature_correlation.png
│       ├── 06_sprint5_confusion_matrix.png
│       ├── 07_sprint5_roc_curve.png
│       ├── 08_sprint5_feature_coefficients.png
│       ├── 09_sprint6_confusion_matrix.png
│       ├── 10_sprint6_roc_curve.png
│       ├── 11_sprint6_feature_importances.png
│       ├── 12_sprint7_confusion_matrix.png
│       ├── 13_sprint7_roc_curve.png
│       ├── 14_sprint8_cv_comparison.png
│       ├── 15_sprint8_feature_selection.png
│       ├── 16_sprint9_combined_roc.png
│       ├── 17_sprint9_model_comparison_bars.png
│       ├── 18_sprint9_performance_heatmap.png
│       ├── sprint5_results.txt
│       ├── sprint6_results.txt
│       ├── sprint7_results.txt
│       ├── sprint8_cv_results.csv
│       ├── sprint8_feature_selection.csv
│       ├── sprint9_model_comparison.csv
│       └── sprint9_final_summary.txt
├── notebooks/                        # Jupyter notebooks (EDA, exploration)
├── src/
│   ├── preprocessing/
│   │   └── cleaning.py               # Sprint 3: data cleaning pipeline
│   ├── features/
│   │   └── lexical_features.py       # Sprint 4: feature extraction
│   └── models/
│       ├── sprint5_baseline_lr.py    # Sprint 5: Logistic Regression baseline
│       ├── sprint6_random_forest.py  # Sprint 6: Random Forest
│       ├── sprint7_svm.py            # Sprint 7: SVM (LinearSVC)
│       └── sprint8_9_evaluation.py  # Sprints 8–9: CV + final comparison
├── docs/                             # Proposal, log book, assessment brief
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/s3giu/phishing-url-detection.git
cd phishing-url-detection
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Download the dataset from Kaggle:
   - Go to: https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset
   - Download and extract `malicious_urls.csv`
   - Place it in `data/raw/` folder

### Running the Pipeline

Run each sprint script in order from the project root:

```bash
# Sprint 3: Data Cleaning
python src/preprocessing/cleaning.py

# Sprint 4: Feature Engineering (generates features_sprint4.csv)
python src/features/lexical_features.py

# Sprint 5: Logistic Regression Baseline
python src/models/sprint5_baseline_lr.py

# Sprint 6: Random Forest
python src/models/sprint6_random_forest.py

# Sprint 7: SVM (LinearSVC)
python src/models/sprint7_svm.py

# Sprints 8-9: Cross-Validation + Final Comparison
python src/models/sprint8_9_evaluation.py
```

All output plots are saved to `data/processed/` and results to `.txt`/`.csv` files in the same directory.

---

## Sprint Progress

### Sprint 1 — Business Understanding ✅

**CRISP-DM Phase:** Business Understanding  
**Dates:** November 2025  
**Deliverables:**
- GitHub repository created and structured with standard ML project layout
- Trello board configured with sprint columns (Backlog, In Progress, Done)
- Dissertation proposal finalised and submitted (CMP600)
- Research question and objectives defined
- CRISP-DM methodology adopted as the project framework

---

### Sprint 2 — Data Understanding ✅

**CRISP-DM Phase:** Data Understanding  
**Dates:** November–December 2025  
**Script:** `sprint2_eda.py`  
**Deliverables:**
- Kaggle Malicious URLs dataset loaded: 651,191 raw URL records
- Class distribution analysed: benign, phishing, defacement, malware
- URL length distributions plotted by class
- Missing values and duplicates identified
- Binary label strategy defined (benign=0, malicious=1)

**Key Finding:** The dataset is moderately imbalanced (~57% benign, ~43% malicious). Stratified splitting was adopted to preserve class ratios in train/test sets.

**Output plots:** `01_label_distribution.png`, `02_url_length_distribution.png`

---

### Sprint 3 — Data Preparation: Cleaning ✅

**CRISP-DM Phase:** Data Preparation  
**Dates:** December 2025  
**Script:** `src/preprocessing/cleaning.py`  
**Deliverables:**
- Null/empty URL records removed
- Duplicate records removed
- Multi-class labels binarized → benign (0) vs malicious (1)
- Clean dataset saved for feature engineering

**Key Metrics:**

| Step | Count |
|---|---|
| Raw input records | 651,191 |
| After null removal | ~648,000 |
| After deduplication | 641,053 |
| Rows removed total | 10,138 (1.56%) |

**Output plots:** `03_binary_label_distribution.png`

---

### Sprint 4 — Data Preparation: Feature Engineering ✅

**CRISP-DM Phase:** Data Preparation  
**Dates:** January 2026  
**Script:** `src/features/lexical_features.py`  
**Output:** `data/processed/features_sprint4.csv` — 641,053 rows × 10 features + label

**Features extracted:** `url_length`, `domain_length`, `path_length`, `dot_count`, `slash_count`, `digit_count`, `digit_ratio`, `letter_count`, `special_char_count`, `entropy`

**Key Finding:** Correlation heatmap showed no significant multicollinearity between features. All 10 features are sufficiently independent for use in all three classifiers without dimensionality reduction.

**Output plots:** `04_feature_distributions.png`, `05_feature_correlation.png`, `05_url_length_by_label.png`

---

### Sprint 5 — Modelling: Logistic Regression Baseline ✅

**CRISP-DM Phase:** Modelling  
**Dates:** February 2026  
**Script:** `src/models/sprint5_baseline_lr.py`  
**Results file:** `data/processed/sprint5_results.txt`

**Configuration:**
- Scaler: StandardScaler (zero mean, unit variance)
- Solver: lbfgs (converged in 31 iterations, ~2.6 seconds)
- Class weight: balanced (compensates for class imbalance)
- Train/Test split: 80% / 20% stratified (random_state=42)
- Training set: 512,842 URLs | Test set: 128,211 URLs

**Results on Test Set:**

| Metric | Value |
|---|---|
| Accuracy | 78.94% |
| Precision | 78.83% |
| Recall | 50.08% |
| F1-Score | 0.6125 |
| **False Positive Rate (FPR)** | **6.69%** ← baseline to beat |
| ROC AUC | 0.8241 |

**Confusion Matrix:**

| | Predicted Benign | Predicted Malicious |
|---|---|---|
| **Actual Benign** | 79,884 (TN) | 5,728 (FP) |
| **Actual Malicious** | 21,267 (FN) | 21,332 (TP) |

**Output plots:** `06_sprint5_confusion_matrix.png`, `07_sprint5_roc_curve.png`, `08_sprint5_feature_coefficients.png`

**Interpretation:** The linear model achieves acceptable accuracy but poor recall (50.08%), meaning it misses approximately half of all malicious URLs. The FPR of 6.69% is the baseline target for subsequent models to improve upon. The feature coefficient plot shows `url_length` as the strongest predictor.

---

### Sprint 6 — Modelling: Random Forest ✅

**CRISP-DM Phase:** Modelling  
**Dates:** February–March 2026  
**Script:** `src/models/sprint6_random_forest.py`  
**Results file:** `data/processed/sprint6_results.txt`

**Configuration:**
- n_estimators: 200 decision trees
- max_depth: 20 (prevents overfitting)
- min_samples_split: 5
- class_weight: balanced
- random_state: 42

**Results on Test Set:**

| Metric | Value | vs LR Baseline |
|---|---|---|
| Accuracy | **94.03%** | +15.09pp |
| Precision | **89.46%** | +10.63pp |
| Recall | **93.00%** | +42.92pp |
| F1-Score | **0.9120** | +0.2995 |
| **False Positive Rate (FPR)** | **5.45%** | -1.24pp ✅ |
| ROC AUC | **0.9855** | +0.1614 |

**Confusion Matrix:**

| | Predicted Benign | Predicted Malicious |
|---|---|---|
| **Actual Benign** | 80,943 (TN) | 4,669 (FP) |
| **Actual Malicious** | 2,980 (FN) | 39,619 (TP) |

**Output plots:** `09_sprint6_confusion_matrix.png`, `10_sprint6_roc_curve.png`, `11_sprint6_feature_importances.png`

**Interpretation:** Massive improvement over the LR baseline on every metric. Recall jumped from 50% to 93% — the model now correctly identifies 93% of all malicious URLs. The AUC of 0.9855 indicates near-perfect discriminative ability. The non-linear ensemble model clearly captures complex feature interactions that the linear model cannot model.

---

### Sprint 7 — Modelling: SVM (LinearSVC) ✅

**CRISP-DM Phase:** Modelling  
**Dates:** March 2026  
**Script:** `src/models/sprint7_svm.py`  
**Results file:** `data/processed/sprint7_results.txt`

**Configuration:**
- Classifier: LinearSVC with Platt scaling (CalibratedClassifierCV for probability estimates)
- Regularisation parameter C: 1.0
- max_iter: 2000
- class_weight: balanced

**Results on Test Set:**

| Metric | Value | vs LR Baseline |
|---|---|---|
| Accuracy | 78.43% | -0.51pp |
| Precision | 77.16% | -1.67pp |
| Recall | 49.84% | -0.24pp |
| F1-Score | 0.6056 | -0.0069 |
| **False Positive Rate (FPR)** | **7.34%** | +0.65pp ❌ worse |
| ROC AUC | 0.8286 | +0.0045 |

**Confusion Matrix:**

| | Predicted Benign | Predicted Malicious |
|---|---|---|
| **Actual Benign** | 79,329 (TN) | 6,283 (FP) |
| **Actual Malicious** | 21,368 (FN) | 21,231 (TP) |

**Output plots:** `12_sprint7_confusion_matrix.png`, `13_sprint7_roc_curve.png`

**Interpretation:** SVM performs comparably to Logistic Regression, confirming that both linear models struggle with the non-linear decision boundary in this dataset. The FPR is actually worse than LR (7.34% vs 6.69%), further reinforcing Random Forest as the superior model for this task.

---

### Sprint 8 — Evaluation: Cross-Validation & Feature Selection ✅

**CRISP-DM Phase:** Evaluation  
**Dates:** March 2026  
**Script:** `src/models/sprint8_9_evaluation.py`  
**Results files:** `data/processed/sprint8_cv_results.csv`, `data/processed/sprint8_feature_selection.csv`

**Cross-Validation Configuration:**
- Method: 5-fold Stratified Cross-Validation
- Sample: 100,000 URLs (stratified subsample for computational efficiency)
- Metrics evaluated: Accuracy, F1, FPR, Recall

**Cross-Validation Results:**

| Model | CV Accuracy (mean ± std) | CV F1 (mean ± std) | CV FPR (mean ± std) |
|---|---|---|---|
| Logistic Regression | 75.82% ± 0.19% | 0.7497 ± 0.0024 | 20.79% ± 0.14% |
| **Random Forest** | **91.95% ± 0.17%** | **0.9198 ± 0.0017** | **8.44% ± 0.34%** |
| SVM (LinearSVC) | 75.81% ± 0.19% | 0.7487 ± 0.0024 | 20.45% ± 0.14% |

The low standard deviations across all 5 folds confirm that results are **stable and not due to chance**.

**Feature Selection (ANOVA F-test — all 641,053 rows):**

| Rank | Feature | F-Score | p-value |
|---|---|---|---|
| 1 | `dot_count` | 31,994 | < 0.001 |
| 2 | `path_length` | 19,041 | < 0.001 |
| 3 | `slash_count` | 10,162 | < 0.001 |
| 4 | `special_char_count` | 8,873 | < 0.001 |
| 5 | `domain_length` | 3,308 | < 0.001 |
| 6 | `letter_count` | 2,636 | < 0.001 |
| 7 | `url_length` | 2,242 | < 0.001 |
| 8 | `entropy` | 1,294 | < 0.001 |
| 9 | `digit_count` | 419 | < 0.001 |
| 10 | `digit_ratio` | 81 | < 0.001 |

All 10 features are statistically significant (p < 0.05). The top 3 features (`dot_count`, `path_length`, `slash_count`) account for the majority of discriminative power, consistent with known phishing URL patterns (subdomain stacking, path obfuscation).

**Output plots:** `14_sprint8_cv_comparison.png`, `15_sprint8_feature_selection.png`

---

### Sprint 9 — Evaluation: Final Model Comparison ✅

**CRISP-DM Phase:** Evaluation  
**Dates:** March 2026  
**Script:** `src/models/sprint8_9_evaluation.py`  
**Results files:** `data/processed/sprint9_model_comparison.csv`, `data/processed/sprint9_final_summary.txt`

**Final Model Comparison (Test Set: 128,211 URLs):**

| Model | Accuracy | Precision | Recall | F1-Score | FPR | ROC AUC |
|---|---|---|---|---|---|---|
| Logistic Regression | 78.94% | 78.83% | 50.08% | 0.6125 | 6.69% | 0.8241 |
| **Random Forest** | **94.03%** | **89.46%** | **93.00%** | **0.9120** | **5.45%** | **0.9855** |
| SVM (LinearSVC) | 78.43% | 77.16% | 49.84% | 0.6056 | 7.34% | 0.8286 |

**Output plots:** `16_sprint9_combined_roc.png`, `17_sprint9_model_comparison_bars.png`, `18_sprint9_performance_heatmap.png`

**Winner: Random Forest** — best on every single metric.

---

## Results Summary

| Model | Accuracy | F1-Score | FPR | ROC AUC |
|---|---|---|---|---|
| Logistic Regression (baseline) | 78.94% | 0.6125 | 6.69% | 0.8241 |
| **Random Forest (WINNER)** | **94.03%** | **0.9120** | **5.45%** | **0.9855** |
| SVM (LinearSVC) | 78.43% | 0.6056 | 7.34% | 0.8286 |

---

## Key Findings

1. **Random Forest is the best model** across all four evaluation metrics (Accuracy, F1, FPR, AUC). It achieves 94.03% accuracy and an AUC of 0.9855 on 128,211 test URLs.

2. **The feature-to-label relationship is non-linear.** The large performance gap between Random Forest (94%) and both linear models (LR: 79%, SVM: 78%) confirms that lexical URL features interact in complex, non-linear ways that ensemble methods capture but linear classifiers cannot.

3. **`dot_count` is the single most discriminative feature** (F-score: 31,994), followed by `path_length` and `slash_count`. Phishing URLs tend to use subdomain stacking (more dots) and longer paths for obfuscation.

4. **FPR is the critical usability metric.** Random Forest achieves the lowest FPR (5.45%), meaning it incorrectly blocks the fewest legitimate URLs — a key requirement for real-world deployment.

5. **Lexical features alone are sufficient** for high-accuracy phishing detection. No external API calls, DNS lookups, or page content analysis are required, enabling true real-time, client-side classification.

---

## References

- Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step Data Mining Guide.* SPSS Inc.
- Siddhartha, M. (2024). *Malicious URLs Dataset.* Kaggle. https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset
- Sahingoz, O. K., Buber, E., Demir, O., & Diri, B. (2019). Machine learning based phishing detection from URLs. *Expert Systems with Applications*, 117, 227–237.
- Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32.
- Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273–297.

---

**Last Updated:** 25 March 2026  
**GitHub:** https://github.com/s3giu/phishing-url-detection  
**Trello:** https://trello.com/b/YbG9606p/phishing
