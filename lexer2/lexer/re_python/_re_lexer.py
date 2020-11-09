"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import typing as _t

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

    VENDOR_ID = "RE_PYTHON_DEFAULT"


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
            vendorId=self.VENDOR_ID,
            ruleset=ruleset,
            handleFlags=handleFlags,
            textstream=textstream
        )
        return


  # --- PROTECTED METHODS --- #

    def _CompileRule(self, rule: _rule.Rule) -> _IMatcher:
        return _Re_Matcher(self.VENDOR_ID, rule.ID, rule.GetRegexPattern())


    def _MatchRule(self, rule: _rule.Rule) -> _misc.Ptr_t[_Token]:

        token: _misc.Ptr_t[_Token] = None

        # NOTE: Inlined version
        matcher: _Re_Matcher = rule._matcher
        regex_match = matcher._pattern.match(
            # Data input
            self._ts._strBuffer,
            # Read STARTING AT position
            self._ts._strBufferPos,
            # Read UNTIL position
            self._ts._strBufferSize
        )

        # Create token if a match was found
        if (regex_match):
            # txt_pos = self._ts.GetTextPosition()
            txt_pos = self._ts._tp
            token = _Token(
                rule.ID,
                regex_match.group(),
                _file.TextPosition(
                    txt_pos.pos,
                    txt_pos.col,
                    txt_pos.ln
                )
            )

        return token
