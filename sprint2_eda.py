import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

PROJECT = r"D:\Dissertation\phishing-url-detection"
RAW_CSV = os.path.join(PROJECT, "data", "raw", "malicious_phish.csv")
OUT_DIR = os.path.join(PROJECT, "data", "processed")

os.makedirs(OUT_DIR, exist_ok=True)

print("Loading:", RAW_CSV)
df = pd.read_csv(RAW_CSV)

print(f"\nDataset shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print("Columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

# Missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Label distribution
print("\nLabel counts:")
print(df["type"].value_counts())

plt.figure(figsize=(8, 5))
df["type"].value_counts().plot(kind="bar", color="steelblue")
plt.title("URL Labels Distribution")
plt.xlabel("Label")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "01_label_distribution.png"), dpi=300)
plt.close()

# URL length distribution
df["url_length"] = df["url"].astype(str).str.len()
print("\nURL length stats:")
print(df["url_length"].describe())

plt.figure(figsize=(10, 5))
plt.hist(df["url_length"], bins=50, color="coral", alpha=0.7, edgecolor="black")
plt.title("URL Length Distribution")
plt.xlabel("URL length (characters)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "02_url_length_distribution.png"), dpi=300)
plt.close()

print("\nSaved plots to:")
print(" -", os.path.join(OUT_DIR, "01_label_distribution.png"))
print(" -", os.path.join(OUT_DIR, "02_url_length_distribution.png"))

print("\nSprint 2 EDA complete.")
