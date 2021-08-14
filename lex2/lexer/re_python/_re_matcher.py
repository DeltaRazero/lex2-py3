"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    import typing as t
    import re

    from .. import AbstractMatcher

# ***************************************************************************************

class Re_Matcher (_.AbstractMatcher):
    """An implementation of IMatcher using Python's builtin `re` module, using AbstractMatcher as base.
    """

  # --- FIELDS --- #

    # t.Pattern is an object instance of a compiled regex pattern, by Python's builtin
    # `re` module.
    _pattern : _.t.Pattern[str]


  # --- CONSTRUCTOR --- #

    def __init__(self, vendorId: str, regexPattern: str):
        """AbstractMatcher object instance initializer.

        Parameters
        ----------
        vendorId : str
            Lexer implementation identifier string (a.k.a. 'vendor ID').
        regexPattern : str
            Regex pattern used by a lexer to identify tokens during lexical analysis.
        """
        super().__init__(vendorId, regexPattern)
        return


  # --- PROTECTED METHODS --- #

    # NOTE: Called from abstract base class' constructor
    def _CompilePattern(self) -> None:
        self._pattern = _.re.compile(self._regexPattern)
        return


  # --- GETTERS --- #

    def GetPatternMatcher(self) -> _.t.Pattern[str]:
        # NOTE: Should actually be type-casted to (void*)
        return self._pattern
