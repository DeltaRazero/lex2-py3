"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._re_matcher import Re_Matcher as _Re_Matcher

from .. import AbstractLexer as _AbstractLexer

from ... import file as _file
from ... import misc as _misc
from ... import _rule
from ... import _flags

from ... import IMatcher as _IMatcher
from ... import Token    as _Token

# ***************************************************************************************

class Re_Lexer (_AbstractLexer):
    """An implementation of ILexer using Python's builtin `re` module, using AbstractLexer as base.
    """

  # --- CONSTANTS --- #

    _VENDOR_ID = "RE_PYTHON_DEFAULT"


  # --- CONSTRUCTOR --- #

    def __init__(self,
                 ruleset: _rule.Ruleset_t=[],
                 handleFlags: _flags.HFlags=_flags.HFlags(),
                 textstream: _file.ITextstream=_file.Textstream()
    ):
        """Re_Lexer object instance initializer.

        Parameters
        ----------
        ruleset : Ruleset_t, optional
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
            vendorId=self._VENDOR_ID,
            ruleset=ruleset,
            handleFlags=handleFlags,
            textstream=textstream
        )
        return


  # --- PROTECTED METHODS --- #

    def _CompileRule(self, rule: _rule.Rule) -> _IMatcher:
        return _Re_Matcher(self._VENDOR_ID, rule.GetId(), rule.GetRegexPattern())


    def _MatchRule(self, rule: _rule.Rule) -> _misc.Ptr_t[_Token]:

        token: _misc.Ptr_t[_Token] = None

        matcher: _Re_Matcher = rule.GetMatcher()  #type: ignore[reportGeneralTypeIssues]
        regex_match = matcher.GetPatternMatcher().match(
            self._ts.GetBuffer(),         # Data input
            self._ts.GetBufferPosition(), # Read STARTING AT position
            self._ts.GetBufferLength()    # Read UNTIL position
        )
        # regex_match: _misc.Ptr_t[_t.Match[str]] # _t.Union[_t.Match[str], None]

        # Create token if a match was found
        if (regex_match):
            txt_pos = self._ts.Tell()
            token = _Token(
                rule.GetId(),
                regex_match.group(),
                _file.TextPosition(
                    txt_pos.pos,
                    txt_pos.col,
                    txt_pos.ln
                )
            )

        return token
