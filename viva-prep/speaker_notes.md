# Speaker Notes — PhishGuard Viva Presentation
## Strictly following the 9-section structure from the instructions

---

## Slide 1: Title & Research Aim

**Say this:**

"Good morning. My dissertation is titled 'A Machine Learning Approach to Real-Time Phishing URL Detection: A Comparative Analysis of Classification Models.'

The aim of my research is to find out whether machine learning models trained only on lexical URL features can provide high accuracy and low False Positive Rates for real-time, client-side phishing detection.

In simple terms — can we tell if a URL is dangerous just by looking at the text of the link, without loading the page or checking any database?"

---

## Slide 2: Background & Rationale

**Say this:**

"Phishing is the number one cybercrime globally. The APWG reported over 4.7 million attacks in 2023 alone. The FBI estimates over $10 billion in losses from internet crime in 2022, with phishing being the top attack vector.

The traditional defence is blacklisting — maintaining a list of known bad URLs. The problem is that blacklists are reactive. Research by Sheng et al. found it takes an average of 12 hours for a new phishing URL to be added to a blacklist. By then, most victims have already been compromised.

This is why my research matters — we need a proactive system that can analyse a URL the moment a user clicks it, in real time, without waiting for it to appear on a list."

---

## Slide 3: Literature Overview

**Say this:**

"The literature shows three generations of phishing detection. First, blacklists — accurate for known threats but cannot catch new ones. Second, content-based methods that analyse the webpage itself — accurate but slow because you have to load the page first. Third, lexical methods that analyse just the URL string — fast but the question is whether they are accurate enough.

Key studies that guided my work: Sahingoz et al. 2019 showed Random Forest outperforms linear models for URL classification. Ma et al. 2009 proved that URL features alone have predictive power. Rao and Pais 2020 used deep learning but did not report False Positive Rate.

The gap I identified: no study has done a controlled comparison of linear versus non-linear classifiers using only structural lexical features on a large dataset, with explicit FPR reporting. That is exactly what my dissertation does."

---

## Slide 4: Methodology

**Say this:**

"I followed the CRISP-DM framework — the industry standard for data mining projects. It has six phases: Business Understanding, Data Understanding, Data Preparation, Modelling, Evaluation, and Deployment. I mapped each phase to a two-week Agile sprint.

My research philosophy is positivist — I believe in measurable, objective results. My approach is deductive — I had a hypothesis from the literature that non-linear models would outperform linear ones, and I tested it.

For data: I used the Malicious URLs Dataset from Kaggle — 641,053 URLs after cleaning. I split it 80/20 using stratified sampling to maintain the class balance. I engineered 10 lexical features from the URL string alone — things like URL length, dot count, path length, and Shannon entropy.

I then trained three classifiers: Logistic Regression as a linear baseline, Random Forest as a non-linear ensemble, and Support Vector Machine as another linear comparator. All used the same data, same features, same split — a fair, controlled experiment."

**If asked "Why these methods?":**

"Logistic Regression is the standard linear baseline. Random Forest is the literature's recommended ensemble method for this task. SVM provides a second linear perspective to confirm whether the limitation is the algorithm or the linearity itself."

---

## Slide 5: Features (10 Lexical Features)

**Say this:**

"These are my 10 features. They are all extracted from the URL text alone — no network calls, no page loading, no external APIs. This means extraction takes less than 1 millisecond per URL.

The top three most discriminative features, confirmed by ANOVA F-test, are: dot_count with an F-score of 31,994, path_length at 19,041, and slash_count at 10,162. All ten features were statistically significant at p less than 0.001.

Why these features work: attackers have to manipulate URLs to look legitimate. Subdomain stacking adds dots. Obfuscation adds path depth and slashes. These structural patterns are what the model learns to detect."

---

## Slide 6: Findings

**Say this:**

"Here are my results. Random Forest achieved 94.03% accuracy, an F1-Score of 0.9120, and most importantly, a False Positive Rate of just 5.45%. That means out of every 100 legitimate URLs, only about 5 would be incorrectly flagged.

The linear models — Logistic Regression at 78.94% and SVM at 78.43% — performed almost identically to each other but 15 percentage points worse than Random Forest. Their recall was only about 50%, meaning they missed half of all malicious URLs.

Cross-validation confirmed these results are stable — Random Forest scored 91.95% accuracy with a standard deviation of only 0.17%, showing the results are not dependent on one lucky data split."

---

## Slide 7: Discussion

**Say this:**

"The key insight is this: the 15-percentage-point gap between Random Forest and the linear models tells us that the relationship between URL features and phishing is fundamentally non-linear.

A URL with many dots is not necessarily malicious — bbc.co.uk has three dots. But a URL with many dots AND a long path AND high entropy is very likely malicious. Linear models cannot capture these feature interactions. Random Forest can, because each of its 200 trees makes decisions along different feature axes.

This connects directly back to the literature — Sahingoz et al. found the same pattern, and my study confirms it on a much larger dataset of 641,000 URLs versus their 73,000.

My contribution to existing knowledge is threefold: the largest controlled lexical comparison, explicit FPR reporting which most studies omit, and a fully reproducible open-source pipeline on GitHub."

---

## Slide 8: Limitations

**Say this:**

"I want to be honest about what this study cannot do.

First, temporal drift — the dataset is historical. Phishing tactics evolve, and the model may become less effective over time without retraining.

Second, lexical features alone cannot catch 'perfect mimicry' — an attacker who registers a short, clean domain name that looks completely legitimate.

Third, I compared three algorithms. I did not test gradient boosting methods like XGBoost or deep learning approaches, which could potentially perform better.

However, these limitations do not undermine the value of the work. The study answers a specific research question — whether lexical features alone are sufficient for a practical first-layer defence — and the answer is clearly yes, with the right algorithm."

---

## Slide 9: Conclusion & Implications

**Say this:**

"To summarise: machine learning trained on lexical features can detect phishing URLs in real time with 94% accuracy and an acceptable False Positive Rate, but only when using non-linear ensemble methods like Random Forest. Linear models are not sufficient for this task.

For future research, I recommend: adding lightweight NLP features like character n-grams, implementing a temporal retraining pipeline for production use, and extending to multi-class classification — phishing, malware, defacement, and benign.

The practical implication is that this approach can be deployed as a fast, privacy-preserving first layer of defence in browser extensions, email gateways, or mobile apps — anywhere you need instant URL classification without external API calls."

---

## Slide 10: Live Demo

**Say this:**

"Let me show you PhishGuard — the working prototype I built to demonstrate the research in practice.

I will test three URLs:

First, google.com — a clearly safe URL. You can see it scores 5 out of 100, all features at low risk.

Second, a suspicious URL with a hyphenated domain and no HTTPS — it scores around 50, showing medium risk.

Third, an IP-based URL with deep path structure — this scores 100 out of 100, with all 10 features flagged at high risk.

The application uses the same 10 features and the same scoring logic from the Random Forest model. It runs entirely in the browser — no server-side computation needed."

**If internet fails:** "I have pre-captured screenshots in Appendix F of my dissertation showing all three result types."

---

## Transitions Between Slides

- After Title → Background: "Let me give you some context on why this research is needed."
- After Background → Literature: "Now let me show you what the existing research says."
- After Literature → Methodology: "So how did I go about addressing this gap?"
- After Methodology → Features: "Let me explain the specific features I engineered."
- After Features → Findings: "Now for the results."
- After Findings → Discussion: "What do these numbers actually mean?"
- After Discussion → Limitations: "Of course, no study is perfect."
- After Limitations → Conclusion: "So to bring it all together..."
- After Conclusion → Demo: "And finally, let me show you the working system."
