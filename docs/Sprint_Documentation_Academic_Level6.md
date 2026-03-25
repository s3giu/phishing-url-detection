# CMP600 Dissertation — Sprint-by-Sprint Academic Documentation

**Student:** Sergiu Ionut Pascaru (ID: 2310-111729)  
**Supervisor:** Oritsetimeyin Edema  
**Programme:** BSc (Hons) Computing [Top-up] — Newcastle College Group  
**Module:** CMP600 – Dissertation  
**Project Title:** A Machine Learning Approach to Real-Time Phishing URL Detection: A Comparative Analysis of Classification Models  
**Submission Deadline:** May 2026  

---

> **Purpose of this document:** This document provides a full academic justification for every decision made across Sprints 1–9, structured to address the three core questions required at Level 6 Computing: *why* each approach was chosen, *how* it was implemented, and *what purpose* it serves in relation to the research question, the CRISP-DM methodology, and the CMP600 assessment brief.

---

## Table of Contents

1. [Research Question & Methodology Overview](#methodology)
2. [Sprint 1: Project Setup & Business Understanding](#sprint1)
3. [Sprint 2: Data Acquisition & Exploratory Data Analysis](#sprint2)
4. [Sprint 3: Data Cleaning & Pre-processing](#sprint3)
5. [Sprint 4: Lexical Feature Engineering](#sprint4)
6. [Sprint 5: Baseline Modelling — Logistic Regression](#sprint5)
7. [Sprint 6: Ensemble Modelling — Random Forest](#sprint6)
8. [Sprint 7: Kernel-based Modelling — Support Vector Machine](#sprint7)
9. [Sprints 8 & 9: Cross-Validation, Feature Selection & Final Evaluation](#sprint89)
10. [Summary of Results](#results)
11. [References](#references)

---

## Research Question & Methodology Overview {#methodology}

The central research question guiding this project is:

> *"To what extent can machine learning classifiers — Logistic Regression, Random Forest, and SVM — using only lexical URL features, distinguish between legitimate and phishing URLs in a real-time detection scenario?"*

This question was operationalized through three sub-questions: (1) which model achieves the highest F1-Score and True Positive Rate; (2) which model minimizes the False Positive Rate (FPR) to avoid disrupting legitimate user activity; and (3) how does the exclusion of host-based features affect classification performance.

The project follows the **Cross-Industry Standard Process for Data Mining (CRISP-DM)** framework, which structures the work into six iterative phases: Business Understanding, Data Understanding, Data Preparation, Modelling, Evaluation, and Deployment. This framework was selected because it is the industry-standard methodology for data mining and machine learning projects, ensuring a rigorous and reproducible research lifecycle. The project is managed using Agile principles via Trello, as required by the CMP600 assessment brief.

---

## Sprint 1: Project Setup & Business Understanding {#sprint1}

**CRISP-DM Phase:** Business Understanding  
**Dates:** 17 November – 30 November 2025  

### Why this was done

Before any technical work could begin, it was essential to establish a clear project management infrastructure. The CMP600 assessment brief explicitly requires Agile project management using Trello, with planning cards, task cards, and retrospective cards for each sprint. Furthermore, a public GitHub repository was required to host the final executable software prototype, which constitutes 40% of the module grade.

### How it was implemented

A public GitHub repository (`s3giu/phishing-url-detection`) was initialized with a structured directory hierarchy: `data/raw/` for the original dataset, `data/processed/` for cleaned and transformed outputs, `notebooks/` for exploratory analysis, and `src/` for all production Python code. A Trello board was created with columns representing the Agile workflow (Backlog, In Progress, Review, Done). The research question, aims, and objectives were formally defined in the dissertation proposal (CMP600 Proposal, December 2025).

### Purpose in the project

This sprint established the governance and transparency framework for the entire project. By making the repository public and linking it to the Trello board, the supervisor was able to monitor progress at any time, fulfilling the assessment's requirement for documented project management and version control.

---

## Sprint 2: Data Acquisition & Exploratory Data Analysis (EDA) {#sprint2}

**CRISP-DM Phase:** Data Understanding  
**Dates:** 1 December – 14 December 2025  

### Why this was done

Exploratory Data Analysis is a non-negotiable step in any data science project. Before training any model, it is critical to understand the distribution of the target variable, identify potential data quality issues (missing values, outliers), and validate that the dataset is fit for purpose. Skipping EDA risks building models on flawed data, producing results that appear valid but are scientifically unsound.

### How it was implemented

The "Malicious URLs" dataset (Siddhartha, 2024) was downloaded from Kaggle and loaded into a Jupyter Notebook (`notebooks/01_eda_sprint2.ipynb`) using the Pandas library. The initial inspection revealed 651,191 rows across two columns: `url` and `type`. The label distribution was visualized using Seaborn bar charts, revealing four classes: benign (428,103), defacement (96,457), phishing (94,111), and malware (32,520). A boxplot of URL lengths was generated to understand the feature distribution before engineering.

### Purpose in the project

The EDA confirmed two critical design decisions for subsequent sprints: (1) the multi-class labels needed to be binarized to align with the binary classification objective; and (2) the dataset contained duplicate entries that would need to be removed to prevent data leakage. These findings directly shaped the data cleaning strategy in Sprint 3.

---

## Sprint 3: Data Cleaning & Pre-processing {#sprint3}

**CRISP-DM Phase:** Data Preparation  
**Dates:** 15 December – 28 December 2025  

### Why this was done

Raw data is rarely suitable for direct model training. The EDA in Sprint 2 identified two specific issues: the presence of duplicate URL entries and multi-class labels. Addressing these issues was essential to ensure the integrity of the model evaluation. Specifically, failing to remove duplicates would constitute a form of **data leakage**, where the same URL could appear in both the training and testing sets, causing the model to memorize specific strings rather than learning generalizable patterns, thereby producing artificially inflated accuracy scores.

### How it was implemented

A dedicated Python script (`src/preprocessing/cleaning.py`) was developed using Pandas. The script executed the following operations in sequence:

| Step | Operation | Rationale |
|---|---|---|
| 1 | Drop rows with null values | Prevents errors during feature extraction |
| 2 | Remove duplicate URL entries | Eliminates data leakage risk |
| 3 | Binary label mapping | Aligns with binary classification objective |

The binary label mapping transformed `benign` to `0` and all other classes (`phishing`, `defacement`, `malware`) to `1`. This reduced the dataset from 651,191 to **641,053 unique, clean records**, which were saved as `data/processed/cleaned_urls_sprint3.csv`.

### Purpose in the project

This sprint produced the clean, validated dataset that served as the single source of truth for all subsequent modelling work. The binary transformation was justified by the real-world deployment context: a client-side browser extension needs to make a single binary decision (safe or unsafe) to protect the user, not distinguish between types of malicious content.

---

## Sprint 4: Lexical Feature Engineering {#sprint4}

**CRISP-DM Phase:** Data Preparation  
**Dates:** 29 December 2025 – 11 January 2026  

### Why this was done

Machine learning algorithms cannot process raw text strings. The URL data needed to be transformed into a structured numerical matrix. The specific decision to use **only lexical features** (attributes derived from the URL string itself) was a deliberate design choice rooted in the project's core constraint: real-time, low-latency detection. Academic literature (Sahingoz et al., 2019; Ma et al., 2009) demonstrates that content-based features (HTML analysis) and host-based features (DNS/WHOIS lookups) introduce network latency of hundreds of milliseconds, making them unsuitable for client-side, real-time detection.

### How it was implemented

A vectorized Python module (`src/features/lexical_features.py`) was developed using Pandas string operations. Standard URL parsing libraries (e.g., Python's `urllib.parse`) were deliberately avoided because they fail silently on malformed malicious URLs, which are common in phishing datasets. Instead, regex-based string operations were used for robustness and speed. The ten features extracted are described below:

| Feature | Description | Academic Justification |
|---|---|---|
| `url_length` | Total character count of the URL | Phishing URLs tend to be longer to obscure the true domain |
| `domain_length` | Length of the domain component | Short, legitimate domains vs. long obfuscated ones |
| `path_length` | Length of the URL path | Deep paths are common in phishing redirects |
| `digit_count` | Number of numeric characters | High digit counts indicate IP-based or obfuscated URLs |
| `letter_count` | Number of alphabetic characters | Structural composition indicator |
| `special_char_count` | Count of special characters (`@`, `-`, `_`, etc.) | Phishing URLs often use special chars to mimic legitimate domains |
| `dot_count` | Number of dots in the URL | Multiple subdomains are a known phishing indicator |
| `slash_count` | Number of forward slashes | Indicates URL depth and redirect complexity |
| `digit_ratio` | Ratio of digits to total URL length | Normalized measure of numeric obfuscation |
| `entropy` | Shannon entropy of the URL string | Measures randomness; high entropy indicates algorithmically generated domains |

### Purpose in the project

This sprint produced the final model-ready feature matrix (`data/processed/features_sprint4.csv`), containing 641,053 rows and 11 columns (10 features + binary label). This artefact was the direct input for all three model training sprints (5, 6, 7), ensuring that all models were evaluated on an identical, consistent dataset.

---

## Sprint 5: Baseline Modelling — Logistic Regression {#sprint5}

**CRISP-DM Phase:** Modelling  
**Dates:** 12 January – 25 January 2026  

### Why this was done

The purpose of Sprint 5 was to establish a quantitative performance baseline. In machine learning research, a baseline model is essential to provide a reference point against which more complex models can be compared. Without a baseline, it is impossible to determine whether the additional complexity of a Random Forest or SVM is actually justified. Logistic Regression was selected as the baseline because it is the simplest, most interpretable binary classifier, and its performance directly reveals whether the classification problem is linearly separable.

### How it was implemented

The script (`src/models/sprint5_baseline_lr.py`) used Scikit-Learn. The dataset was split into 80% training (512,842 rows) and 20% testing (128,211 rows) using **stratified sampling** (`stratify=y`) to preserve the class ratio. `StandardScaler` was applied to normalize features, a mathematical requirement for linear models. The `lbfgs` solver was used, which is efficient for large datasets. The evaluation generated a Confusion Matrix, Classification Report, and ROC Curve.

### Purpose in the project

The baseline results established the performance floor for the project:

| Metric | Value |
|---|---|
| Accuracy | 78.94% |
| F1-Score | 0.6125 |
| False Positive Rate (FPR) | 6.69% |
| ROC AUC | 0.8241 |

The low F1-Score (0.61) and high FPR (6.69%) demonstrated that a linear decision boundary was insufficient to capture the complexity of phishing URL patterns, providing the academic justification for proceeding to non-linear models in Sprints 6 and 7.

---

## Sprint 6: Ensemble Modelling — Random Forest {#sprint6}

**CRISP-DM Phase:** Modelling  
**Dates:** 26 January – 8 February 2026  

### Why this was done

Following the underperformance of the linear baseline, Sprint 6 investigated whether an ensemble of decision trees could better model the non-linear interactions between lexical features. The Random Forest algorithm was selected because it is robust to overfitting, handles high-dimensional data well, and provides native feature importance scores — a valuable analytical output for understanding which URL characteristics are most predictive of malicious intent.

### How it was implemented

The script (`src/models/sprint6_random_forest.py`) trained a `RandomForestClassifier` with 200 estimators and a maximum depth of 20. The `class_weight='balanced'` parameter was set to account for the slight class imbalance in the dataset (approximately 2:1 benign to malicious ratio). The same 80/20 stratified split was used to ensure direct comparability with the Sprint 5 baseline.

### Purpose in the project

The Random Forest results demonstrated a transformative improvement over the baseline:

| Metric | Baseline (LR) | Random Forest | Improvement |
|---|---|---|---|
| Accuracy | 78.94% | **94.03%** | +15.09% |
| F1-Score | 0.6125 | **0.9120** | +0.2995 |
| FPR | 6.69% | **5.45%** | −1.24% |
| ROC AUC | 0.8241 | **0.9855** | +0.1614 |

This result directly answered the research question: the non-linear ensemble model significantly outperforms the linear baseline, confirming that phishing URL structures exhibit complex, non-linear patterns that lexical features can capture effectively when modelled with the appropriate algorithm.

---

## Sprint 7: Kernel-based Modelling — Support Vector Machine {#sprint7}

**CRISP-DM Phase:** Modelling  
**Dates:** 9 February – 22 February 2026  

### Why this was done

The third model in the comparative analysis was the Support Vector Machine (SVM). SVMs are widely cited in the phishing detection literature (e.g., Sahingoz et al., 2019) and were included to provide a comprehensive comparison between linear models (Logistic Regression), ensemble models (Random Forest), and margin-based classifiers (SVM). Including SVM also fulfils the original research proposal's commitment to a three-way comparative analysis.

### How it was implemented

Traditional SVMs using non-linear kernels (RBF, Polynomial) require $O(n^2)$ memory for the kernel matrix, which is computationally infeasible for a dataset of 500,000+ rows. Therefore, `LinearSVC` was selected, which scales linearly with the number of samples. Because `LinearSVC` does not natively produce probability scores (required for ROC curve generation), it was wrapped in `CalibratedClassifierCV` using Platt scaling. The script (`src/models/sprint7_svm.py`) used the same stratified split and `StandardScaler` pipeline.

### Purpose in the project

The SVM results confirmed the pattern established by the baseline:

| Metric | SVM | Logistic Regression |
|---|---|---|
| Accuracy | 78.43% | 78.94% |
| F1-Score | 0.6056 | 0.6125 |
| FPR | 7.34% | 6.69% |

The SVM's performance was marginally worse than even the Logistic Regression baseline, providing strong evidence that the decision boundary for this problem is fundamentally non-linear. The SVM's higher FPR (7.34%) makes it the least suitable model for real-world deployment from a usability perspective.

---

## Sprints 8 & 9: Cross-Validation, Feature Selection & Final Evaluation {#sprint89}

**CRISP-DM Phase:** Evaluation  
**Dates:** Sprint 8: 23 February – 8 March 2026 | Sprint 9: 9 March – 22 March 2026  

### Why this was done

A single train/test split, while informative, does not guarantee that the results are generalizable and not an artifact of how the data happened to be divided. **Cross-validation** was therefore essential to validate that the Random Forest's superior performance was consistent and reproducible across different data partitions. Additionally, **feature selection** was performed to identify which of the ten lexical features contributed most to the classification, providing academic insight into the structural characteristics of phishing URLs.

### How it was implemented

**Sprint 8 — Cross-Validation:** A 5-fold stratified cross-validation was applied to all three models using a balanced subsample of 100,000 rows. This subsample size was chosen to balance statistical representativeness with computational feasibility. The results confirmed the stability of the Random Forest:

| Model | CV Accuracy (Mean ± Std) | CV F1 (Mean ± Std) |
|---|---|---|
| Logistic Regression | 75.82% ± 0.19% | 0.7497 ± 0.0024 |
| **Random Forest** | **91.95% ± 0.17%** | **0.9198 ± 0.0017** |
| SVM (LinearSVC) | 75.81% ± 0.19% | 0.7487 ± 0.0024 |

**Sprint 8 — Feature Selection:** ANOVA F-test (`SelectKBest` with `f_classif`) was applied to rank all ten features by their statistical discriminative power:

| Rank | Feature | F-Score |
|---|---|---|
| 1 | `dot_count` | 31,994 |
| 2 | `path_length` | 19,041 |
| 3 | `slash_count` | 10,162 |
| 4 | `special_char_count` | 8,873 |
| 5 | `domain_length` | 3,308 |

**Sprint 9 — Final Comparison:** Combined ROC curves, a comparative bar chart, and a performance heatmap were generated to produce publication-quality visualizations summarizing all findings.

### Purpose in the project

The cross-validation results confirmed that the Random Forest's performance was not due to overfitting on a specific data split — it consistently achieved ~92% accuracy across all five folds. The feature selection analysis revealed that structural URL attributes (`dot_count`, `path_length`, `slash_count`) are the most powerful predictors of malicious intent, which aligns with and extends the existing literature on lexical phishing detection.

---

## Summary of Results {#results}

The following table presents the final comparative results across all three models, evaluated on the held-out test set of 128,211 URLs:

| Model | Accuracy | Precision | Recall | F1-Score | FPR | ROC AUC |
|---|---|---|---|---|---|---|
| Logistic Regression | 78.94% | 0.7883 | 0.5008 | 0.6125 | 6.69% | 0.8241 |
| **Random Forest** | **94.03%** | **0.8946** | **0.9300** | **0.9120** | **5.45%** | **0.9855** |
| SVM (LinearSVC) | 78.43% | 0.7716 | 0.4984 | 0.6056 | 7.34% | 0.8286 |

**Conclusion:** Random Forest is the optimal model for real-time phishing URL detection using lexical features. It achieves the highest accuracy, F1-Score, and ROC AUC, while simultaneously achieving the lowest False Positive Rate — the most critical usability metric for a real-world client-side detection system.

---

## References {#references}

[1] Sahingoz, O.K., Buber, E., Demir, O. and Diri, B. (2019) 'Machine learning based phishing detection from URLs', *Expert Systems with Applications*, 117, pp. 345–357. Available at: https://doi.org/10.1016/j.eswa.2018.09.029

[2] Ma, J., Saul, L.K., Savage, S. and Voelker, G.M. (2009) 'Identifying suspicious URLs: An application of large-scale online learning', *Proceedings of the 26th Annual International Conference on Machine Learning (ICML)*. Available at: https://dl.acm.org/doi/10.1145/1553374.1553462

[3] Siddhartha (2024) *Malicious URLs Dataset*, Kaggle. Available at: https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset

[4] Breiman, L. (2001) 'Random Forests', *Machine Learning*, 45(1), pp. 5–32. Available at: https://doi.org/10.1023/A:1010933404324

[5] Cortes, C. and Vapnik, V. (1995) 'Support-vector networks', *Machine Learning*, 20(3), pp. 273–297. Available at: https://doi.org/10.1007/BF00994018
