# Friday Viva Preparation Plan
## CMP600 Dissertation — Sergiu Ionut Pascaru
### PhishGuard: A Machine Learning Approach to Real-Time Phishing URL Detection

---

## Overview of the Viva

| Element | Detail |
|---------|--------|
| **Format** | Part A: 10-minute presentation + Part B: 10–15 minute Q&A |
| **Total Duration** | 30–45 minutes |
| **Weighting** | 20% of final module grade |
| **Examiners** | Academic panel (likely your supervisor Oti Edema + one other) |
| **Purpose** | Confirm authorship, demonstrate understanding, defend decisions |

---

## Day-by-Day Preparation Schedule

### Tuesday (Today) — Content Mastery

**Morning (2 hours): Know your numbers cold**

You must be able to state these from memory without hesitation:

| Metric | Logistic Regression | Random Forest | SVM (LinearSVC) |
|--------|--------------------|--------------|--------------------|
| Accuracy | 78.94% | **94.03%** | 78.43% |
| Precision | 0.7883 | **0.8946** | 0.7716 |
| Recall | 0.5008 | **0.9300** | 0.4984 |
| F1-Score | 0.6125 | **0.9120** | 0.6056 |
| FPR | 6.69% | **5.45%** | 7.34% |
| ROC AUC | 0.8241 | **0.9855** | 0.8286 |

**Cross-validation (5-fold on 100,000 rows):**
- Random Forest: 91.95% ± 0.17% accuracy, F1 = 0.9198 ± 0.0017

**Top 3 features by ANOVA F-score:**
1. dot_count (F = 31,994) — most discriminative
2. path_length (F = 19,041)
3. slash_count (F = 10,162)

**Dataset facts:**
- Source: Malicious URLs Dataset (Kaggle, Siddhartha 2024)
- Raw: 651,191 records → cleaned: 641,053 unique URLs
- Split: 80/20 stratified → 512,842 train / 128,211 test
- Class balance: ~66.7% benign, ~33.3% malicious

**Afternoon (2 hours): Know your methodology**

Be ready to explain each decision:

- **Why CRISP-DM?** Industry-standard data mining methodology; maps naturally to sprint-based Agile development; provides clear phases from business understanding to deployment.
- **Why lexical features only?** No external API calls needed; real-time capable (< 1ms per URL); privacy-preserving; reproducible; addresses a gap in literature where most studies mix feature types.
- **Why Random Forest won?** Phishing vs. benign URL patterns are non-linear; RF captures complex feature interactions through ensemble of 200 decision trees; handles class imbalance with class_weight='balanced'.
- **Why 80/20 split?** Standard practice; stratified to preserve class distribution; large enough test set (128,211 URLs) for statistically reliable evaluation.
- **Why these 10 features?** Selected based on literature review (Sahingoz et al. 2019; Ma et al. 2009) and validated by ANOVA F-test; all purely structural (no DNS, no WHOIS, no page content).

---

### Wednesday — Presentation Rehearsal

**Morning: Rehearse the 10-minute presentation**

Practice out loud, timing yourself. Target timings per slide:

| Slide | Topic | Time |
|-------|-------|------|
| 1 | Title + Research Aim | 30 sec |
| 2 | Background & Rationale | 60 sec |
| 3 | Literature Overview + Gap | 75 sec |
| 4 | Methodology (CRISP-DM + Agile) | 75 sec |
| 5 | Dataset + Features | 60 sec |
| 6 | Results Table | 90 sec |
| 7 | Key Finding: Why RF Won | 60 sec |
| 8 | Discussion + Limitations | 60 sec |
| 9 | Conclusion + Contributions | 45 sec |
| 10 | Live Demo | 90 sec |

**Afternoon: Prepare for Q&A**

Read through the Q&A guide (separate document). Practise answering out loud — not reading from notes.

---

### Thursday — Final Preparation

**Morning:**
- Do one full run-through of the presentation (timed, standing up, speaking aloud)
- Test the PhishGuard live demo: https://phishguardapp.manus.space
  - Try: `https://www.google.com` → should score ~5/100 (Safe)
  - Try: `http://myaccount-update.net/verify` → should score ~50/100 (Suspicious)
  - Try: `http://192.168.1.1/paypal/login/secure` → should score 100/100 (Malicious)
- Check GitHub repo is accessible: https://github.com/s3giu/phishing-url-detection

**Afternoon:**
- Lay out your clothes (smart/professional)
- Print a one-page cheat sheet with your key numbers (for your own reference before entering the room — not to use during the viva)
- Get a good night's sleep

---

### Friday — Viva Day

**Before the viva:**
- Arrive 15 minutes early
- Review your one-page cheat sheet once outside the room, then put it away
- Take a deep breath — you built this system, you know it better than anyone in the room

**During the presentation:**
- Speak slowly and clearly
- Make eye contact with both examiners
- When you reach the demo slide, open the browser and demonstrate live

**During Q&A:**
- Take a moment before answering — it is fine to pause and think
- If you do not know something, say: *"That is a good question. Based on my research, I would say..."*
- Never say "I don't know" — always connect to what you do know
- Be honest about limitations — the examiners respect intellectual honesty

---

## Key Messages to Convey

These are the three things you want the examiners to remember:

1. **You understand the problem deeply.** Phishing is a real, growing threat (APWG 2024: attacks peaked in 2022). Your solution addresses a specific, justified gap — lexical-only, real-time detection.

2. **Your methodology was rigorous and justified.** Every decision (CRISP-DM, feature selection, 80/20 split, class_weight='balanced') was grounded in literature and validated empirically.

3. **Your results are significant and honest.** Random Forest achieved 94.03% accuracy with 5.45% FPR — competitive with published literature. You acknowledge limitations (temporal drift, lexical-only scope) without undermining the contribution.

---

## What to Bring on Friday

- [ ] Laptop (charged, with presentation open and browser ready)
- [ ] Charger
- [ ] USB backup of the presentation (in case of technical issues)
- [ ] One printed copy of your dissertation (optional but impressive)
- [ ] Water bottle
- [ ] Student ID

---

## Viva Checklist

- [ ] Can state all 6 performance metrics for all 3 models from memory
- [ ] Can explain why Random Forest outperformed linear models
- [ ] Can justify every methodological choice
- [ ] Can explain each of the 10 lexical features and why they matter
- [ ] Can demonstrate PhishGuard live (tested on Thursday)
- [ ] Presentation rehearsed at least 3 times
- [ ] Q&A answers practised out loud
- [ ] Professional attire ready
- [ ] GitHub repo accessible and dissertation folder visible
