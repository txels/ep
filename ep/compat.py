"""
Compatibility layer for various versions of python
"""

try:
    # In python2.x this will generate a pylint error. We let it be as a
    # reminder that this is a hack.
    basestring = basestring
except NameError:
    # Python3 fallback
    basestring = str
