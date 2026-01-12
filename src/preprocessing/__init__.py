# Preprocessing Module
# CMP600 Dissertation - Phishing URL Detection

"""
Data preprocessing module for cleaning and preparing URL data.

Functions (to be implemented in Sprint 3):
    - load_raw_data(): Load CSV file from data/raw/
    - clean_urls(): Remove invalid URLs and standardize format
    - binarize_labels(): Convert multi-class to binary labels
    - save_processed_data(): Save cleaned data to data/processed/
"""

from .cleaning import *
