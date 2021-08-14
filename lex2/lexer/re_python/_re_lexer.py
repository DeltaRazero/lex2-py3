"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    from ._re_matcher import Re_Matcher

    from .. import AbstractLexer

    from ... import textio
    from ... import misc
    from ... import opts

    from ... import ruleset_t
    from ... import Rule

    from ... import IMatcher
    from ... import Token

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
        return _.Re_Matcher(self.VENDOR_ID, rule.regexPattern)


    def _MatchRule(self, rule: _.Rule) -> _.misc.ptr_t[_.Token]:

        token: _.misc.ptr_t[_.Token] = None

        # NOTE: It's faster to cache this variable in CPython to prevent unnecessary
        # lookups to 'self'.
        _ts = self._ts

        # matcher: _Re_Matcher = rule.GetMatcher()
        # regex_match = matcher.GetPatternMatcher(
        #   self._ts.GetBufferString(),         # Data input
        #   self._ts.GetBufferStringPosition(), # Read STARTING AT position
        #   self._ts.GetBufferStringSize(),     # Read UNTIL position
        # )

        matcher: _.Re_Matcher = rule._matcher
        regex_match = matcher._pattern.match(
            _ts._bufferString,     # Data input
            _ts._bufferStringPos,  # Read STARTING AT position
            _ts._bufferStringSize, # Read UNTIL position
        )

        # Create token if a match was found
        if (regex_match):
            # txt_pos: _textio.TextPosition = self._ts.GetTextPosition()
            txt_pos: _.textio.TextPosition = _ts._tp
            token = _.Token(
                rule.id,
                regex_match.group(),
                _.textio.TextPosition(
                    txt_pos.pos,
                    txt_pos.col,
                    txt_pos.ln
                )
            )
            del regex_match

        return token
