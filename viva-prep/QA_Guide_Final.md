# Viva Q&A Guide — PhishGuard
## Only the 7 questions from the examiner instructions
### Keep it natural. Don't memorise. Understand the reasoning and speak in your own words.

---

## Q1. Why did you choose this topic?

**Natural answer:**

"Phishing is the most common cyber attack in the world — over 4.7 million attacks reported in 2023 alone. I was interested in cybersecurity and wanted to do something practical, not just theoretical. When I looked at the literature, I noticed that most detection systems either rely on blacklists, which are always behind, or they need to load the webpage first, which is slow.

I thought — what if you could tell whether a URL is dangerous just by looking at the text of the link itself? That is fast, it is private because you do not send the URL anywhere, and it works even offline. When I found that no one had done a proper controlled comparison of classifiers using only structural URL features on a large dataset, I knew that was my gap."

---

## Q2. How did you ensure your data collection was reliable and valid?

**Natural answer:**

"I used the Malicious URLs Dataset from Kaggle by Siddhartha, published in 2024. It contains over 651,000 labelled URLs. It is publicly available, so anyone can verify my results.

To ensure reliability, I did several things. I removed duplicates — because if the same URL appears in both training and testing, the model would cheat. I cleaned the data by removing rows with missing values and standardising everything to lowercase. I used stratified splitting — 80% training, 20% testing — which guarantees both sets have the same proportion of benign and malicious URLs. And I fixed the random seed to 42, so anyone running my code gets exactly the same results.

For validity, I used 5-fold cross-validation on a separate subsample of 100,000 URLs. The low standard deviation — only 0.17% for Random Forest — confirms the results are stable and not just a lucky split."

---

## Q3. What were the main challenges you faced?

**Natural answer:**

"Three main challenges.

First, malformed URLs. Many malicious URLs are deliberately broken or unusual — they crash Python's standard URL parser. I had to write custom exception handling so the pipeline could skip bad rows without crashing, and I avoided using urlparse entirely, using vectorised pandas string operations instead.

Second, class imbalance. The dataset is 67% benign and 33% malicious. If I trained naively, the model could just predict 'benign' for everything and get 67% accuracy. I solved this using class_weight='balanced', which makes the model pay more attention to the minority class during training.

Third, computational cost. Running 5-fold cross-validation on 641,000 URLs with Random Forest would take too long. I used a balanced subsample of 100,000 URLs for cross-validation, which is standard practice and still gives statistically reliable results."

---

## Q4. How did you analyse your data? Why that approach?

**Natural answer:**

"I used a supervised machine learning approach — specifically, a classification experiment. I trained three different classifiers on the same 10 features and the same data split, then compared their performance using six metrics: Accuracy, Precision, Recall, F1-Score, False Positive Rate, and ROC AUC.

I chose this approach because my research question is fundamentally empirical — 'which type of model works best for this task?' The only way to answer that is to run a controlled experiment where everything is the same except the algorithm.

I also used ANOVA F-test for feature selection — this tells me statistically which features are most useful for distinguishing between benign and malicious URLs. And I used cross-validation to confirm the results are stable.

Why not qualitative methods? Because there are no human participants in this study. It is purely about measuring model performance on data. Quantitative methods are the only appropriate choice."

---

## Q5. Which theoretical perspectives influenced your work and why?

**Natural answer:**

"Three main theoretical influences.

First, the work of Ma et al. from 2009, who first proved that URL features alone have enough predictive power for classification. They showed that you do not need to load the page — the URL string itself contains useful patterns.

Second, Breiman's 2001 paper on Random Forests. He showed that building many decision trees on random subsets of features and data, then combining their votes, produces models that are both accurate and resistant to overfitting. This is exactly why Random Forest works so well for my task — phishing patterns involve complex interactions between multiple features that a single linear model cannot capture.

Third, the CRISP-DM framework by Chapman et al. from 2000. This gave me a structured methodology to follow — from understanding the business problem through to deployment. It kept the project organised and ensured I did not skip important steps like data understanding or evaluation."

---

## Q6. What would you do differently if you repeated the study?

**Natural answer:**

"Three things.

First, I would add temporal validation. Instead of a random train/test split, I would train on older URLs and test on newer ones. This would tell me how quickly the model degrades as phishing tactics evolve — which is the biggest real-world concern.

Second, I would add a few more feature types. Specifically, character-level n-grams — short sequences of characters — which would help detect brand spoofing. For example, 'paypa1' instead of 'paypal'. My current features cannot catch that, but n-grams could.

Third, I would test gradient boosting methods like XGBoost or LightGBM. The literature suggests they might perform even better than Random Forest for tabular data, and I did not include them because I wanted to keep the comparison focused on three clearly different algorithm types."

---

## Q7. How do your findings contribute to existing knowledge?

**Natural answer:**

"Three specific contributions.

First, I provide the largest controlled comparison of linear versus non-linear classifiers on purely structural lexical features. Previous studies either used smaller datasets, mixed different feature types, or did not control the comparison properly. My study uses 641,000 URLs with the same 10 features across all three models.

Second, I explicitly report False Positive Rate — which most studies do not do. This matters because in practice, if your system blocks too many legitimate websites, users will simply turn it off. My Random Forest achieves 5.45% FPR, which means only about 1 in 18 legitimate URLs gets incorrectly flagged.

Third, the entire pipeline is open-source and reproducible on GitHub. Fixed random seeds, documented preprocessing, modular code. Any researcher can replicate my exact results or extend the work with new features or algorithms."

---

## Bonus: If They Ask About Ethics

**Natural answer:**

"The project was approved as low risk because it uses only publicly available secondary data — no human participants, no personal information. All URLs were treated as text strings in an offline Python environment. I never visited any of the malicious URLs. The ethics form was submitted in December 2025 and approved. I followed the NCG Research Ethics Policy throughout."

---

## Key Numbers to Know (just glance at before you go in)

| What | Number |
|------|--------|
| Dataset size | 641,053 URLs |
| Split | 80/20 stratified |
| Class balance | 67% benign, 33% malicious |
| RF Accuracy | 94.03% |
| RF F1-Score | 0.9120 |
| RF FPR | 5.45% |
| RF ROC AUC | 0.9855 |
| LR Accuracy | 78.94% |
| SVM Accuracy | 78.43% |
| Top feature | dot_count (F = 31,994) |
| Number of features | 10 |
| Number of trees in RF | 200 |
| Cross-val accuracy | 91.95% ± 0.17% |
