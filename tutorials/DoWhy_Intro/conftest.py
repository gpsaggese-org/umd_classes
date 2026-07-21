"""
Pytest configuration for the DoWhy tutorial.

Adds the tutorial root to sys.path so tests under test/ can import
dowhy_utils directly.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
