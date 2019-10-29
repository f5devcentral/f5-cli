""" global imports for tests - abstracts away try/except"""

import unittest
import pytest
try:
    from unittest.mock import Mock, MagicMock, patch, call, PropertyMock, mock_open
except ImportError:  # python 2.x support
    from mock import Mock, MagicMock, patch, call, PropertyMock, mock_open

__all__ = [
    'unittest',
    'pytest',
    'Mock',
    'MagicMock',
    'patch',
    'call',
    'PropertyMock',
    'mock_open'
]
