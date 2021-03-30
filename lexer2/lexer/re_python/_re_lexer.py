"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._re_matcher import Re_Matcher as _Re_Matcher

from .. import AbstractLexer as _AbstractLexer

from ... import textio as _textio
from ... import misc as _misc
from ... import _rule

from ... import IMatcher     as _IMatcher
from ... import Token        as _Token
from ... import LexerOptions as _LexerOptions

# ***************************************************************************************

class Re_Lexer (_AbstractLexer):
    """An implementation of ILexer using Python's builtin `re` module, using AbstractLexer as base.
    """

  # --- CONSTANTS --- #

    VENDOR_ID = "RE_PYTHON_DEFAULT"


  # --- CONSTRUCTOR --- #

    def __init__(self,
                 ruleset: _rule.ruleset_t=[],
                 options: _LexerOptions=_LexerOptions(),
    ):
        """Re_Lexer object instance initializer.

        Parameters
        ----------
        ruleset : ruleset_t, optional
            Initial ruleset.
            By default []
        handleFlags : HFlags, optional
            Initial handleFlags struct.
            By default HFlags()
        textstream : ITextstream, optional
            Specify a specific ITextstream implementation.
            By default Textstream()
        """
        super().__init__(
            vendorId=self.VENDOR_ID,
            ruleset=ruleset,
            options=options,
        )
        return


  # --- PROTECTED METHODS --- #

    def _CompileRule(self, rule: _rule.Rule) -> _IMatcher:
        return _Re_Matcher(self.VENDOR_ID, rule.regexPattern)


    def _MatchRule(self, rule: _rule.Rule) -> _misc.ptr_t[_Token]:

        token: _misc.ptr_t[_Token] = None

        # matcher: _Re_Matcher = rule.GetMatcher()
        # regex_match = matcher.GetPatternMatcher(
        #   self._ts.GetBufferString(),         # Data input
        #   self._ts.GetBufferStringPosition(), # Read STARTING AT position
        #   self._ts.GetBufferStringSize(),     # Read UNTIL position
        # )

        matcher: _Re_Matcher = rule._matcher
        regex_match = matcher._pattern.match(
            self._ts._bufferString,     # Data input
            self._ts._bufferStringPos,  # Read STARTING AT position
            self._ts._bufferStringSize, # Read UNTIL position
        )

        # Create token if a match was found
        if (regex_match):
            # txt_pos: _textio.TextPosition = self._ts.GetTextPosition()
            txt_pos: _textio.TextPosition = self._ts._tp
            token = _Token(
                rule.id,
                regex_match.group(),
                _textio.TextPosition(
                    txt_pos.pos,
                    txt_pos.col,
                    txt_pos.ln
                )
            )

        return token
