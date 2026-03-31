"""
银行股估值模型框架
包含DDM、PB-ROE、RIV和相对估值法
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Investment Agent Team"

from .config import Config
from .data_fetcher import DataFetcher
from .calculator import ValuationCalculator
from .analyzer import ValuationAnalyzer

__all__ = [
    'Config',
    'DataFetcher',
    'ValuationCalculator',
    'ValuationAnalyzer',
]
