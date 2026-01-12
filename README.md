# Phishing URL Detection – CMP600 Dissertation

**Author:** Sergiu Ionut Pascaru (ID: 2310-111729)  
**Module:** CMP600 – Dissertation  
**Institution:** Newcastle College Group  
**Timeline:** Nov 2025 – May 2026

## Project Overview

This project implements a machine learning approach to detect phishing URLs using only lexical URL features (structure analysis) for real-time, client-side detection without external lookups.

The study compares three classifiers:
- **Logistic Regression** (baseline linear model)
- **Random Forest** (ensemble non-linear model)
- **Support Vector Machine (SVM)** (kernel-based non-linear model)

## Dataset

**Malicious URLs Dataset** (Siddhartha, 2024) from Kaggle:
- 650,000+ labelled URL records
- Classes: benign, phishing, defacement, malware
- Binary target for this project: benign (0) vs malicious (1)
- Source: https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset

## Methodology

**Framework:** CRISP-DM (Cross-Industry Standard Process for Data Mining)

1. Business Understanding (Sprint 1)
2. Data Understanding (Sprint 2)
3. Data Preparation (Sprints 3–4)
4. Modelling (Sprints 5–7)
5. Evaluation (Sprints 8–9)
6. Deployment (Sprints 10–14)

## Project Structure

```
phishing-url-detection/
├── data/
│   ├── raw/                 # Original Kaggle CSV
│   └── processed/           # Cleaned and engineered data
├── notebooks/               # Jupyter notebooks for each sprint
├── src/
│   ├── preprocessing/       # Data cleaning modules
│   └── features/            # Feature extraction modules
├── docs/                    # Documentation and proposal
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Jupyter Notebook

### Installation

1. Clone the repository:
```bash
git clone https://github.com/s3giu/phishing-url-detection.git
cd phishing-url-detection
```

2. Install required packages:
```bash
pip install pandas numpy scikit-learn jupyter matplotlib seaborn
```

3. Download the dataset from Kaggle:
   - Go to: https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset
   - Download and extract `malicious_urls.csv`
   - Place it in `data/raw/` folder

4. Launch Jupyter Notebook:
```bash
jupyter notebook
```

### Sprint Execution

Each sprint follows the same workflow:
1. Create a new branch: `git checkout -b sprint<N>-<description>`
2. Implement tasks (code, notebooks, testing)
3. Commit changes: `git add . && git commit -m "Sprint X: ..."`
4. Push to GitHub: `git push origin sprint<N>-<description>`
5. Merge to main: `git checkout main && git merge sprint<N>-<description>`

## Sprint Progress

| Sprint | Phase | Status | Description |
|--------|-------|--------|-------------|
| 1 | Business Understanding | ✅ Complete | Project setup, GitHub, Trello |
| 2 | Data Understanding | 🔄 In Progress | EDA, dataset exploration |
| 3 | Data Preparation | ⏳ Pending | Data cleaning, binarization |
| 4 | Data Preparation | ⏳ Pending | Feature engineering |
| 5-7 | Modelling | ⏳ Pending | Train classifiers |
| 8-9 | Evaluation | ⏳ Pending | Model comparison |
| 10-14 | Deployment | ⏳ Pending | Documentation, submission |

## References

- Chapman, P., et al. (2000). CRISP-DM 1.0 Step-by-step Data Mining Guide.
- Siddhartha, M. (2024). Malicious URLs Dataset. Kaggle.
- Sahingoz, O.K., et al. (2019). Machine Learning Based Phishing Detection from URLs. Expert Systems with Applications, 117, 227–237.

---

**Last Updated:** January 12, 2026  
**Status:** Sprint 1 Complete
