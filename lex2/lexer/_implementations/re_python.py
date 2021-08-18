"""Components of a lexer implementation with Python's builtin `re` module."""

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

    from .. import AbstractLexer
    from .. import AbstractMatcher

    from ... import (
        textio,
        misc,
        opts,

        ruleset_t,
        Rule,
        IMatcher,
    )

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

    def Match(self, ts: _.textio.ITextstream) -> _.misc.ptr_t[str]:

        regex_match = self._pattern.match(
            ts._bufferString,     # Data input
            ts._bufferStringPos,  # Read STARTING AT position
            ts._bufferStringSize, # Read UNTIL position
        )

        if (regex_match):
            return regex_match.group()
        return None

# ***************************************************************************************

class Re_Lexer (_.AbstractLexer):
    """An implementation of ILexer using Python's builtin `re` module, using AbstractLexer as base.
    """

  # --- CONSTANTS --- #

    VENDOR_ID = "RE_PYTHON_DEFAULT"


  # --- CONSTRUCTOR --- #

    def __init__(self,
                 ruleset: _.ruleset_t=[],
                 options: _.opts.LexerOptions=_.opts.LexerOptions(),
    ):
        """Re_Lexer object instance initializer.

        Parameters
        ----------
        ruleset : ruleset_t, optional
            Initial ruleset.
            By default []
        options : LexerOptions, optional
            Struct specifying processing options of the lexer.
            By default LexerOptions()
        """
        super().__init__(
            vendorId=self.VENDOR_ID,
            ruleset=ruleset,
            options=options,
        )
        return


  # --- PROTECTED METHODS --- #

    def _CompileRule(self, rule: _.Rule) -> _.IMatcher:
        return Re_Matcher(self.VENDOR_ID, rule.regexPattern)
