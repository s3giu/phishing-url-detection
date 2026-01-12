"""
Sprint 4: Lexical Feature Extraction
Author: Sergiu Ionut Pascaru
Module: CMP600 - Dissertation

Description:
This module extracts lexical features from URLs for phishing detection.
These features are based on URL structure only (no external lookups).

Features Extracted:
    1. url_length - Total URL length
    2. domain_length - Domain name length
    3. path_length - URL path length
    4. digit_count - Number of digits
    5. letter_count - Number of letters
    6. special_char_count - Number of special characters
    7. digit_ratio - Ratio of digits to total length
    8. dot_count - Number of dots
    9. slash_count - Number of forward slashes
    10. entropy - Shannon entropy of URL string
"""

import pandas as pd
import numpy as np
import math
from urllib.parse import urlparse
from collections import Counter
from typing import Dict, List


def extract_url_length(url: str) -> int:
    """Extract total URL length."""
    return len(url)


def extract_domain_length(url: str) -> int:
    """Extract domain name length from URL."""
    try:
        parsed = urlparse(url if url.startswith('http') else f'http://{url}')
        domain = parsed.netloc
        return len(domain)
    except:
        return len(url.split('/')[0])


def extract_path_length(url: str) -> int:
    """Extract URL path length."""
    try:
        parsed = urlparse(url if url.startswith('http') else f'http://{url}')
        return len(parsed.path)
    except:
        parts = url.split('/', 1)
        return len(parts[1]) if len(parts) > 1 else 0


def extract_digit_count(url: str) -> int:
    """Count number of digits in URL."""
    return sum(c.isdigit() for c in url)


def extract_letter_count(url: str) -> int:
    """Count number of letters in URL."""
    return sum(c.isalpha() for c in url)


def extract_special_char_count(url: str) -> int:
    """Count special characters in URL."""
    special_chars = set('-_.~:/?#[]@!$&\'()*+,;=%')
    return sum(c in special_chars for c in url)


def extract_digit_ratio(url: str) -> float:
    """Calculate ratio of digits to total URL length."""
    if len(url) == 0:
        return 0.0
    return extract_digit_count(url) / len(url)


def extract_dot_count(url: str) -> int:
    """Count number of dots in URL."""
    return url.count('.')


def extract_slash_count(url: str) -> int:
    """Count number of forward slashes in URL."""
    return url.count('/')


def calculate_entropy(url: str) -> float:
    """
    Calculate Shannon entropy of URL string.
    
    Higher entropy indicates more randomness/complexity.
    Phishing URLs often have higher entropy due to random strings.
    """
    if len(url) == 0:
        return 0.0
    
    # Count character frequencies
    freq = Counter(url)
    length = len(url)
    
    # Calculate entropy
    entropy = 0.0
    for count in freq.values():
        probability = count / length
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy


def extract_all_features(url: str) -> Dict[str, float]:
    """
    Extract all lexical features from a single URL.
    
    Parameters:
        url (str): URL string to analyze
        
    Returns:
        dict: Dictionary of feature names and values
    """
    return {
        'url_length': extract_url_length(url),
        'domain_length': extract_domain_length(url),
        'path_length': extract_path_length(url),
        'digit_count': extract_digit_count(url),
        'letter_count': extract_letter_count(url),
        'special_char_count': extract_special_char_count(url),
        'digit_ratio': extract_digit_ratio(url),
        'dot_count': extract_dot_count(url),
        'slash_count': extract_slash_count(url),
        'entropy': calculate_entropy(url)
    }


def extract_features_dataframe(df: pd.DataFrame, 
                                url_column: str = 'url') -> pd.DataFrame:
    """
    Extract all lexical features from a DataFrame of URLs.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing URLs
        url_column (str): Name of the URL column
        
    Returns:
        pd.DataFrame: DataFrame with extracted features
    """
    print("Extracting lexical features...")
    print(f"Processing {len(df):,} URLs...")
    
    # Extract features for each URL
    features_list = []
    for i, url in enumerate(df[url_column]):
        if (i + 1) % 100000 == 0:
            print(f"  Processed {i+1:,} URLs...")
        features_list.append(extract_all_features(url))
    
    # Create DataFrame from features
    features_df = pd.DataFrame(features_list)
    
    print(f"Extracted {len(features_df.columns)} features")
    print(f"Features: {list(features_df.columns)}")
    
    return features_df


def run_feature_pipeline(input_path: str = '../data/processed/cleaned_urls_sprint3.csv',
                         output_path: str = '../data/processed/features_sprint4.csv') -> pd.DataFrame:
    """
    Run the complete feature extraction pipeline.
    
    Parameters:
        input_path (str): Path to cleaned data CSV
        output_path (str): Path for feature matrix CSV
        
    Returns:
        pd.DataFrame: Feature matrix with labels
    """
    print("=" * 60)
    print("SPRINT 4: FEATURE EXTRACTION PIPELINE")
    print("=" * 60)
    
    # Load cleaned data
    print(f"\nLoading data from: {input_path}")
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df):,} records")
    
    # Extract features
    print("\n")
    features_df = extract_features_dataframe(df)
    
    # Add label column
    features_df['label'] = df['label'].values
    
    # Save feature matrix
    print(f"\nSaving features to: {output_path}")
    features_df.to_csv(output_path, index=False)
    print(f"Saved {len(features_df):,} records with {len(features_df.columns)} columns")
    
    print("\n" + "=" * 60)
    print("Feature extraction complete!")
    print("=" * 60)
    
    return features_df


# Allow running as script
if __name__ == "__main__":
    run_feature_pipeline()
