"""
Sprint 3: Data Cleaning and Label Binarization
Author: Sergiu Ionut Pascaru
Module: CMP600 - Dissertation

Description:
This module handles data cleaning and label binarization for the 
Malicious URLs dataset from Kaggle (Siddhartha, 2024).

Functions:
    - load_raw_data(): Load CSV file from data/raw/
    - clean_urls(): Remove invalid URLs and standardize format
    - binarize_labels(): Convert multi-class labels to binary
    - save_processed_data(): Save cleaned data to data/processed/
"""

import pandas as pd
import numpy as np
import re
from typing import Tuple


def load_raw_data(filepath: str = '../data/raw/malicious_urls.csv') -> pd.DataFrame:
    """
    Load the raw Malicious URLs dataset from CSV file.
    
    Parameters:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Raw dataset with 'url' and 'type' columns
    """
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df):,} records")
    return df


def clean_urls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize URL strings.
    
    Operations:
        1. Remove leading/trailing whitespace
        2. Convert to lowercase
        3. Remove duplicate URLs
        4. Remove URLs with missing values
        
    Parameters:
        df (pd.DataFrame): DataFrame with 'url' column
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    print("Cleaning URLs...")
    initial_count = len(df)
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Remove rows with missing URLs
    df_clean = df_clean.dropna(subset=['url'])
    
    # Strip whitespace
    df_clean['url'] = df_clean['url'].str.strip()
    
    # Convert to lowercase for consistency
    df_clean['url'] = df_clean['url'].str.lower()
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates(subset=['url'])
    
    final_count = len(df_clean)
    removed = initial_count - final_count
    print(f"Removed {removed:,} records ({removed/initial_count*100:.2f}%)")
    print(f"Remaining: {final_count:,} records")
    
    return df_clean


def binarize_labels(df: pd.DataFrame, 
                    positive_label: str = 'benign',
                    label_column: str = 'type') -> pd.DataFrame:
    """
    Convert multi-class labels to binary classification.
    
    Mapping:
        - 'benign' -> 0 (safe)
        - 'phishing', 'defacement', 'malware' -> 1 (malicious)
        
    Parameters:
        df (pd.DataFrame): DataFrame with label column
        positive_label (str): Label to map to 0 (default: 'benign')
        label_column (str): Name of the label column (default: 'type')
        
    Returns:
        pd.DataFrame: DataFrame with new 'label' column (binary)
    """
    print("Binarizing labels...")
    df_binary = df.copy()
    
    # Create binary label: 0 = benign, 1 = malicious
    df_binary['label'] = df_binary[label_column].apply(
        lambda x: 0 if x == positive_label else 1
    )
    
    # Print distribution
    benign_count = (df_binary['label'] == 0).sum()
    malicious_count = (df_binary['label'] == 1).sum()
    total = len(df_binary)
    
    print(f"Label distribution:")
    print(f"  Benign (0):    {benign_count:>10,} ({benign_count/total*100:.2f}%)")
    print(f"  Malicious (1): {malicious_count:>10,} ({malicious_count/total*100:.2f}%)")
    
    return df_binary


def save_processed_data(df: pd.DataFrame, 
                        filepath: str = '../data/processed/cleaned_urls_sprint3.csv') -> None:
    """
    Save processed DataFrame to CSV file.
    
    Parameters:
        df (pd.DataFrame): Processed DataFrame to save
        filepath (str): Output file path
    """
    print(f"Saving processed data to: {filepath}")
    df.to_csv(filepath, index=False)
    print(f"Saved {len(df):,} records")


def run_cleaning_pipeline(input_path: str = '../data/raw/malicious_urls.csv',
                          output_path: str = '../data/processed/cleaned_urls_sprint3.csv') -> pd.DataFrame:
    """
    Run the complete data cleaning pipeline.
    
    Steps:
        1. Load raw data
        2. Clean URLs
        3. Binarize labels
        4. Save processed data
        
    Parameters:
        input_path (str): Path to raw data CSV
        output_path (str): Path for processed data CSV
        
    Returns:
        pd.DataFrame: Cleaned and processed DataFrame
    """
    print("=" * 60)
    print("SPRINT 3: DATA CLEANING PIPELINE")
    print("=" * 60)
    
    # Step 1: Load
    df = load_raw_data(input_path)
    
    # Step 2: Clean
    df = clean_urls(df)
    
    # Step 3: Binarize
    df = binarize_labels(df)
    
    # Step 4: Save
    save_processed_data(df, output_path)
    
    print("=" * 60)
    print("Pipeline complete!")
    print("=" * 60)
    
    return df


# Allow running as script
if __name__ == "__main__":
    run_cleaning_pipeline()
