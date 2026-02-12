"""Components of matcher implementations."""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ******************************************************************************

from lex2 import util

# ******************************************************************************

# Core.
from ._matcher_base import MatcherBase

# Implementations.
if (util.deps.is_module_installed("re")):
  from ._std_re import ReMatcher
