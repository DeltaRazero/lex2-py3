"""Components of matcher implementations."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from lex2 import _util

# ***************************************************************************************

# Core
from ._base_matcher import BaseMatcher

# Implementations
if (_util.deps.ModuleInstalled("re")):
    from ._std_re import Re_Matcher
