"""
Compatibility layer for various versions of python
"""

try:
    basestring = basestring
except NameError:
    # Python3 fallback
    basestring = str
