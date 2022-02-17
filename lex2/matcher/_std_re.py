"""Components of a lexer implementation with Python's builtin `re` module."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import typing as t
    import re

    from . import (
        BaseMatcher
    )

    from lex2 import (
        textio,
    )
    from lex2._util.types import (
        ptr_t,
    )

# ***************************************************************************************

class Re_Matcher (__.BaseMatcher):
    """An implementation of IMatcher using Python's builtin `re` module, using AbstractMatcher as base.
    """

  # --- FIELDS --- #

    # t.Pattern is an object instance of a compiled regex pattern, by Python's builtin
    # `re` module.
    _pattern : __.t.Pattern[str]


  # --- CONSTRUCTOR --- #

    def __init__(self) -> None:
        super().__init__()
        return


  # --- PUBLIC METHODS --- #

    def CompilePattern(self, regexPattern: str) -> None:
        self._pattern = __.re.compile(regexPattern)
        return


    def Match(self, ts: __.textio.ITextstream) -> __.ptr_t[str]:

        regex_match = self._pattern.match(
            ts._bufferString,     # Data input
            ts._bufferStringPos,  # Read STARTING AT position
            ts._bufferStringSize, # Read UNTIL position
        )

        if (regex_match):
            return regex_match.group()
        return None
