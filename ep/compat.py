"""
Compatibility layer for various versions of python
"""

try:
    # In python2.x this would generate a pylint error:
    basestring = basestring  # NOQA
except NameError:
    # Python3 fallback
    basestring = str
