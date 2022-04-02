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

class ReMatcher (__.BaseMatcher):
    """Implementation of IMatcher using Python's builtin `re` module.
    """

    # :: PRIVATE PROPERTIES :: #

    # t.Pattern is an instance of a compiled regex pattern of Python's builtin 're' module
    _pattern : __.t.Pattern[str]


    # :: CONSTRUCTOR :: #

    def __init__(self) -> None:
        super().__init__()
        return


    # :: PUBLIC METHODS :: #

    def compile_pattern(self, regex_pattern: str) -> None:
        self._pattern = __.re.compile(regex_pattern)
        return


    def match(self, ts: __.textio.ITextstream) -> __.ptr_t[str]:

        regex_match = self._pattern.match(
            ts._string_buffer,     # Data input
            ts._string_buffer_pos,  # Read STARTING AT position
            ts._string_buffer_size, # Read UNTIL position
        )

        if (regex_match):
            return regex_match.group()
        return None
