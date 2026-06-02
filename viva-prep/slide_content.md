# Viva Presentation Slide Content
## CMP600 Dissertation — Sergiu Ionut Pascaru

---

## Slide 1: Title

**Title:** PhishGuard: A Machine Learning Approach to Real-Time Phishing URL Detection

**Subtitle:** CMP600 Dissertation — Viva Voce Presentation

**Name:** Sergiu Ionut Pascaru

**Institution:** Elizabeth School of London | BSc (Hons) Computing

**Date:** June 2026

**Speaker note:** "Good morning/afternoon. My name is Sergiu Ionut Pascaru and my dissertation is titled PhishGuard — a machine learning system for detecting phishing URLs in real time using only the structural features of the URL itself."

---

## Slide 2: Research Aim & Background

**Heading:** Why Phishing Detection Matters

**Key points (bullet-free — use visual blocks):**
- **651,191 URLs** analysed in this study
- Phishing attacks peaked in **2022** (APWG, 2024) — still the #1 cyber threat
- Traditional blacklists fail against **zero-hour attacks** (new URLs not yet listed)
- Machine learning offers real-time, scalable detection

**Research Question:**
> "Can machine learning models using only lexical URL features detect phishing URLs accurately enough for real-world deployment, and which classifier performs best?"

**Research Aim:**
To design, implement, and evaluate a lexical-feature-based ML pipeline that classifies URLs as benign or malicious in real time.

**Speaker note:** "Phishing is not a new problem, but it is a growing one. The APWG reported record-high phishing volumes in 2022. The key challenge is zero-hour attacks — brand new URLs that no blacklist has seen yet. Machine learning trained on the structural patterns of URLs can detect these instantly."

---

## Slide 3: Literature Overview & Research Gap

**Heading:** What the Literature Tells Us

**Three columns:**

| Blacklisting | Content-Based ML | Lexical-Only ML |
|---|---|---|
| Fast but reactive | High accuracy but slow | Fast AND accurate |
| Fails on new URLs | Requires page loading | Works on URL alone |
| Google Safe Browsing | DNS + WHOIS + HTML | This study's approach |

**Research Gap identified:**
- Most studies mix feature types (lexical + DNS + content)
- No controlled comparison of purely lexical classifiers on large-scale dataset
- FPR (False Positive Rate) rarely reported — critical for user experience

**Key sources:** Sahingoz et al. (2019), Ma et al. (2009), Rao & Pais (2020), APWG (2024)

**Speaker note:** "The literature shows three generations of phishing detection. Blacklists are fast but reactive. Content-based ML is accurate but slow. The gap I identified is that no study had done a rigorous, controlled comparison of purely lexical classifiers on a large, modern dataset — with explicit FPR reporting."

---

## Slide 4: Methodology

**Heading:** Research Design — CRISP-DM + Agile Scrum

**Two-part visual:**

**Left: CRISP-DM Phases**
1. Business Understanding (Sprint 1)
2. Data Understanding (Sprint 2)
3. Data Preparation (Sprints 3–4)
4. Modelling (Sprints 5–7)
5. Evaluation (Sprints 8–9)
6. Deployment (Sprint 10+)

**Right: Key Decisions**
- **Philosophy:** Positivist — observable, measurable, reproducible
- **Approach:** Deductive — hypothesis tested empirically
- **Strategy:** Experimental — controlled comparison of 3 classifiers
- **Dataset:** Malicious URLs Dataset (Kaggle, 641,053 URLs)
- **Split:** 80/20 stratified train/test

**Speaker note:** "I used CRISP-DM because it is the industry-standard data mining methodology and maps naturally to Agile sprints. My philosophy is positivist — I believe knowledge comes from observable, measurable phenomena. My approach is deductive — I took hypotheses from the literature and tested them empirically."

---

## Slide 5: The 10 Lexical Features

**Heading:** Feature Engineering — 10 Structural URL Features

**Feature table (two columns):**

| Feature | Why It Detects Phishing |
|---------|------------------------|
| url_length | Malicious URLs are longer to obscure domain |
| domain_length | Unusual lengths indicate suspicious activity |
| path_length | Deep paths hide true destination |
| digit_count | IP addresses inflate digit count |
| letter_count | Baseline composition metric |
| special_char_count | Obfuscation uses @, !, % symbols |
| digit_ratio | High ratio = algorithmically generated |
| dot_count | Subdomain stacking (most discriminative: F=31,994) |
| slash_count | Directory depth and complexity |
| entropy | Shannon entropy — high = random/obfuscated |

**Key point:** All features extracted in < 1ms per URL — no external API calls needed

**Speaker note:** "These 10 features were selected based on the literature and validated by ANOVA F-test. The most discriminative feature is dot_count with an F-score of 31,994 — phishing URLs stack subdomains to look legitimate. All features are purely structural — no DNS lookups, no page loading, which makes the system real-time capable."

---

## Slide 6: Results — Model Performance

**Heading:** Results: Random Forest Outperforms All

**Performance table:**

| Model | Accuracy | F1-Score | FPR | ROC AUC |
|-------|----------|----------|-----|---------|
| Logistic Regression | 78.94% | 0.6125 | 6.69% | 0.8241 |
| **Random Forest** | **94.03%** | **0.9120** | **5.45%** | **0.9855** |
| SVM (LinearSVC) | 78.43% | 0.6056 | 7.34% | 0.8286 |

**Cross-validation (5-fold, 100,000 rows):**
- Random Forest: **91.95% ± 0.17%** — highly stable

**Visual:** Bar chart showing the three models' accuracy side by side

**Speaker note:** "Random Forest achieved 94.03% accuracy with a False Positive Rate of just 5.45% — meaning only 1 in 18 legitimate URLs is incorrectly flagged. The linear models plateaued at 78–79%, confirming that the relationship between lexical features and phishing is non-linear. Cross-validation confirmed this is not overfitting."

---

## Slide 7: Why Random Forest Won

**Heading:** Why Random Forest Outperformed Linear Models

**Three reasons (visual cards):**

**1. Non-linearity of phishing patterns**
URL features interact in complex, non-linear ways. A long URL with high entropy AND many dots is far more suspicious than any single feature alone. Random Forest captures these interactions; linear models cannot.

**2. Ensemble robustness**
200 decision trees vote on each URL. No single tree dominates. This reduces variance and handles the diversity of phishing tactics.

**3. Class imbalance handling**
With class_weight='balanced', RF adjusts for the 66/34 class split automatically. Linear models struggled with recall (~50%) — missing half of all phishing URLs.

**Speaker note:** "The 15-percentage-point gap between Random Forest and the linear models is the central finding of this dissertation. It empirically confirms what Breiman (2001) theorised — ensemble methods excel when decision boundaries are complex and non-linear."

---

## Slide 8: Limitations & Discussion

**Heading:** Honest Limitations — What This Study Cannot Do

**Three limitations:**

**1. Temporal Drift**
The dataset is historical. As phishing tactics evolve, the model may need retraining. A production system would require periodic retraining on fresh data.

**2. Lexical-Only Scope**
The system cannot detect phishing on legitimate-looking domains (e.g., `paypal.com.phishing-site.net` might score lower than expected). Content-based features would improve this.

**3. Dataset Representativeness**
The Kaggle dataset may not represent the full diversity of current phishing campaigns, particularly mobile-targeted or homograph attacks.

**Contribution to literature:**
- Largest lexical-only controlled comparison found in reviewed literature
- Explicit FPR reporting (often absent in published studies)
- Open-source reproducible pipeline on GitHub

**Speaker note:** "I want to be honest about what this study cannot do. The model is trained on historical data and will experience temporal drift. It is also lexical-only, so sophisticated domain-spoofing attacks may evade it. However, these limitations do not undermine the core contribution — this is a rigorous, reproducible baseline that others can build on."

---

## Slide 9: Conclusion & Contributions

**Heading:** Conclusion — Three Key Contributions

**Three contribution blocks:**

**1. Empirical Evidence**
Confirmed that Random Forest (94.03% accuracy, 5.45% FPR) significantly outperforms linear classifiers for lexical phishing detection on a large-scale dataset.

**2. Reproducible Pipeline**
Complete open-source codebase on GitHub — all preprocessing, feature engineering, model training, and evaluation scripts available for replication.

**3. Working Prototype**
PhishGuard web application demonstrates real-world viability — any URL analysed in real time, accessible at https://phishguardapp.manus.space

**Recommendations for future research:**
- Integrate lightweight NLP (character n-grams) to complement lexical features
- Add temporal retraining pipeline for production deployment
- Extend to multi-class classification (phishing, malware, defacement, benign)

**Speaker note:** "To conclude — this dissertation makes three contributions: empirical evidence that Random Forest is the best lexical classifier, a reproducible open-source pipeline, and a working web prototype. The system is fast, accurate, and privacy-preserving — a viable first layer in a multi-layered security architecture."

---

## Slide 10: Live Demo — PhishGuard

**Heading:** Live Demo — PhishGuard in Action

**URL:** https://phishguardapp.manus.space

**Demo sequence (practise this exactly):**

1. Open browser to https://phishguardapp.manus.space
2. **Safe URL:** Type `https://www.google.com` → click Analyse → show green result (score ~5/100)
   - Say: "Google.com scores 5/100 — short URL, low entropy, no suspicious characters"
3. **Malicious URL:** Type `http://192.168.1.1/paypal/login/secure/verify/account` → click Analyse → show red result (score 100/100)
   - Say: "This IP-based URL scores 100/100 — raw IP address, 9 slashes, 13 digits, high entropy"
4. Point to the feature table: "Each feature is explained with its value and risk level"
5. Point to the model statistics panel: "The model used is Random Forest with 94.03% accuracy"

**Backup plan:** If internet fails, show screenshots from Appendix F of the dissertation.

**Speaker note:** "Let me show you the system working live. This is the PhishGuard prototype — it takes any URL and analyses it using the Random Forest model trained on 641,053 URLs."
