"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc    as _abc
import typing as _t

from .. import excs    as _excs
from .. import file    as _file
from .. import predefs as _predefs
from .. import misc    as _misc
from .. import _rule
from .. import _flags

from .. import ILexer   as _ILexer
from .. import IMatcher as _IMatcher
from .. import Token    as _Token

# ***************************************************************************************

class AbstractLexer (_ILexer, metaclass=_abc.ABCMeta):
    """Abstract base class of an ILexer implementation.
    """

  # --- FIELDS --- #

    _vendorId: str

    _rulesets : _t.List[_rule.Ruleset_t]
    _hFlags   : _flags.HFlags

    _ts : _file.ITextstream


  # --- CONSTRUCTOR --- #

    @_abc.abstractmethod
    def __init__(self,
                 vendorId: str,
                 ruleset: _rule.Ruleset_t=[],
                 handleFlags: _flags.HFlags=_flags.HFlags(),
                 textstream: _file.ITextstream=_file.Textstream(),
    ):
        """AbstractLexer object instance initializer.

        Parameters
        ----------
        vendorId : str
            Lexer implementation identifier string (a.k.a. 'vendor ID').
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
        self._vendorId = vendorId

        self._rulesets = []
        if (len(ruleset)): self.PushRuleset(ruleset)

        self._hFlags = handleFlags
        self._ts     = textstream

        return


  # --- PUBLIC METHODS --- #

    def GetTextstream(self) -> _file.ITextstream:
        return self._ts


    def PushRuleset(self, ruleset: _rule.Ruleset_t) -> None:
        # Before pushing the ruleset, we check if the pattern matchers (saved in the rule
        # objects) are compiled for the specific lexer implementation this function is called from.
        self._CompileRuleset(ruleset)
        self._rulesets.append(ruleset)
        return

    def PopRuleset(self) -> None:
        self._rulesets.pop()
        return

    def ClearRulesets(self) -> None:
        self._rulesets.clear()
        return


    def GetHFlags(self) -> _flags.HFlags:
        return self._hFlags


    def GetNextToken(self) -> _Token:

        flags = self._hFlags

        # This is the resulting token to return
        token: _misc.Ptr_t[_Token] = None

        # Single characters that are usually skipped. These are predefined rules in the
        # library.
        while(1):

            # If the textream has reached the end of data
            if (self._ts.IsEOF()):
                # return token
                raise _excs.EndOfTextstream()
                # raise EOFError()

            # NOTE: This is a hack in order to improve performance. Languages that use
            # compilers would probably just inline the GetBuffer() and Tell() calls, but
            # an interpreted languages such as Python obviously can't do that.
            char = self._ts._strBuffer[self._ts._textPos.pos]  #type: ignore[reportUnknownMemberType]
            # char = self._ts.GetBuffer()[self._ts.Tell().pos]

            # SPACE character
            if (char == ' '):
                if (flags.space == _flags.HFlag.HANDLE_AND_RETURN):
                    txt_pos = self._ts.Tell()
                    token = _Token(
                        _predefs.space.GetId(),
                        "",
                        _file.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                self._ts.Seek(1, 1)

            # NEWLINE character
            elif (char == '\n'):
                if (flags.newline == _flags.HFlag.HANDLE_AND_RETURN):
                    txt_pos = self._ts.Tell()
                    token = _Token(
                        _predefs.newline.GetId(),
                        "",
                        _file.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                self._ts.Seek(1, 1)

            # TAB character
            elif (char == '\t'):
                if (flags.tab == _flags.HFlag.HANDLE_AND_RETURN):
                    txt_pos = self._ts.Tell()
                    token = _Token(
                        _predefs.tab.GetId(),
                        "",
                        _file.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                self._ts.Seek(1, 1)  # TODO: Textstreams should get a read1() method

            # Else break to the main regex matching loop
            else:
                break

            # If we didn't break AND we HFlag.HANDLE_AND_RETURN set for one of the above
            # characters
            if (token):
                return token

        # Main regex matching loop
        ruleset: _rule.Ruleset_t = self._rulesets[-1]
        for rule in ruleset:

            token = self._MatchRule(rule)
            # If the (implemented) regex pattern matcher created a match
            if (token):

                # Seek past token
                self._ts.Seek(len(token.GetData()), 1)

                # Check if the token should be ignored by checking HFlag values
                # COMMENT
                if (token.IsRule(_predefs._comment_)):  #type: ignore[reportPrivateUsage]
                    if (self._hFlags.comment==_flags.HFlag.HANDLE_AND_IGNORE):
                        return self.GetNextToken()
                # USER-DEFINED RULES
                for rule in self._hFlags.userFlags:
                    if (token.IsRule(rule)):
                        if (self._hFlags.userFlags[rule]==_flags.HFlag.HANDLE_AND_IGNORE):  ## token.GetId() == flag_key
                            return self.GetNextToken()
                        break

                # Else return the token as normally intended
                return token

        # If no recognizable token type was found (no regex pattern was matched), meaning
        # an unknown token, then the procedure below is used.

        # Store the start position before skipping any characters
        txt_pos = self._ts.Tell()
        unknown_start_index: int = txt_pos.pos  # TODO: Can be removed with length variable if textstream has read method
        position = _file.TextPosition(
            txt_pos.pos,
            txt_pos.col,
            txt_pos.ln
        )

        # Mainloop for skipping characters
        while(1):

            self._ts.Seek(1, 1)  # TODO: Textstreams should get a read1() method

            if (self._ts.IsEOF()):
                break

            char = self._ts.GetBuffer()[self._ts.Tell().pos]  # TODO: Length++
            if (char in (' ', '\t', '\n') ):
                break

        # If the HANDLE_AND_IGNORE option is set for the 'unknownToken' flag,
        # all characters are skipped until a SPACE, TAB or NEWLINE character is
        # encountered.
        if (self._hFlags.unknownToken == _flags.HFlag.HANDLE_AND_IGNORE):
            return self.GetNextToken()

        # Else, if the HANDLE_AND_RETURN option is set, raise an UnknownTokenError
        # with the unknown data attached as lexer token.
        token = _Token(
            _predefs.unknownToken.GetId(),
            # NOTE: This will not work for buffered textstreams, as the length of an
            # unknown token can be larger than the buffer size.
            # TODO: Therefore, textstreams should get a read(n) method instead.
            self._ts.GetBuffer()[unknown_start_index : self._ts.Tell().pos],
            position
        )
        raise _excs.UnknownTokenError(
            token.GetPosition(),
            token.GetData()
        )


  # --- PROTECTED METHODS --- #

    @_abc.abstractmethod
    def _CompileRule(self, rule: _rule.Rule) -> _IMatcher:
        """Requests implemented lexer to compile a regex matcher object.

        Parameters
        ----------
        rule : Rule

        Returns
        -------
        IMatcher
        """
        pass


    @_abc.abstractmethod
    def _MatchRule(self, rule: _rule.Rule) -> _misc.Ptr_t[_Token]:
        """Requests implemented lexer to match a rule.

        The implementation calls the GetMatcher() method from a Rule object to match
        a regex pattern.
        The right (compiled) types of regex matcher objects are already ensured whenever
        a ruleset is pushed.

        Parameters
        ----------
        rule : Rule

        Returns
        -------
        Ptr_t[Token]
            A regex matcher should not return anything whenever no regex match was found.
            Therefore the return type is a pointer/reference of Token (i.e. Token*).
        """
        pass


  # --- PRIVATE METHODS --- #

    def _CompileRuleset(self, ruleset: _rule.Ruleset_t) -> None:
        """Checks and compiles rules within a newly pushed ruleset.

        Whenever a ruleset is pushed, this method will check if all rules have their
        corresponding IMatcher-compatible object set to the matcher type, used by
        a specific lexer/matcher implementation, and compiles if necessary.

        Parameters
        ----------
        ruleset : Ruleset_t
        """
        for rule in ruleset:

            needs_compilation = False
            # Check if the lexer implementation identifier ('vendor ID') is different
            matcher = rule.GetMatcher()
            # If a Matcher object already compiled and stored
            if (matcher):
                needs_compilation = matcher.GetVendorId() != self._vendorId
            # If not compiled at all
            else:
                needs_compilation = True

            # Call the specific lexer implementation's CompileRule() method for regex
            # pattern matcher compilation
            if (needs_compilation):
                rule.SetMatcher(self._CompileRule(rule))

        return
