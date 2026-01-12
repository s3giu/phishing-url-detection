# Features Module
# CMP600 Dissertation - Phishing URL Detection

"""
Feature engineering module for extracting lexical features from URLs.

Functions (to be implemented in Sprint 4):
    - extract_url_length(): Get total URL length
    - extract_domain_length(): Get domain name length
    - extract_path_length(): Get URL path length
    - extract_digit_count(): Count numeric characters
    - extract_special_char_count(): Count special characters
    - calculate_entropy(): Calculate Shannon entropy
    - extract_all_features(): Extract all features at once
"""

from .lexical_features import *
