"""
Test configuration and utilities for KB-AI test suite
"""

import sys
import os

# Add Scripts directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Scripts'))

# Test constants
TEST_TICKERS = ['AAPL', 'GOOGL', 'MSFT']
MOCK_GROUND_TRUTH = {
    'sma50': 175.50,
    'sma200': 168.20,
    'rsi': 58.3,
    'trend_score': 1.5
}

# Evaluation thresholds
GOOD_SCORE_THRESHOLD = 80
ACCEPTABLE_SCORE_THRESHOLD = 70
