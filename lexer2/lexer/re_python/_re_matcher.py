"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import typing as _t
import re     as _re

from .. import AbstractMatcher as _AbstractMatcher

# ***************************************************************************************

class Re_Matcher (_AbstractMatcher):
    """An implementation of IMatcher using Python's builtin `re` module, using AbstractMatcher as base.
    """

  # --- FIELDS --- #

    # t.Pattern is an object instance of a compiled regex pattern, by Python's builtin
    # `re` module.
    _pattern : _t.Pattern[str]


  # --- CONSTRUCTOR --- #

    def __init__(self, vendorId: str, ruleId: str, regexPattern: str):
        """AbstractMatcher object instance initializer.

        Parameters
        ----------
        vendorId : str
            Lexer implementation identifier string (a.k.a. 'vendor ID').
        ruleId : str
            The identifying string of a resulting token's type (e.g. "NUMBER", "WORD").
        regexPattern : str
            Regex pattern used by a lexer to identify tokens during lexical analysis.
        """
        super().__init__(vendorId, ruleId, regexPattern)
        return


  # --- PROTECTED METHODS --- #

    # NOTE: Called from abstract base class' constructor
    def _CompilePattern(self) -> None:
        self._pattern = _re.compile(self._regexPattern)
        return


  # --- GETTERS --- #

    def GetPatternMatcher(self) -> _t.Pattern[str]:
        # NOTE: Should actually be type-casted to (void*)
        return self._pattern
