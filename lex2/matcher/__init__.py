"""Components of matcher implementations."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from lex2 import util

# ***************************************************************************************

# Core
from ._base_matcher import BaseMatcher

# Implementations
if (util.deps.is_module_installed("re")):
    from ._std_re import ReMatcher
