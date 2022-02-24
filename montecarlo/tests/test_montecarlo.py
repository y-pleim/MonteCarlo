"""
Unit and regression test for the montecarlo package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import montecarlo


def test_montecarlo_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "montecarlo" in sys.modules
