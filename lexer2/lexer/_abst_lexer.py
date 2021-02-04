"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc    as _abc
import typing as _t
import io     as _io

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

    _rulesets : _t.List[_rule.ruleset_t]
    _hFlags   : _flags.HFlags

    _ts : _file.ITextstream


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    @_abc.abstractmethod
    def __init__(self,
                 vendorId: str,
                 ruleset: _rule.ruleset_t=[],
                 handleFlags: _flags.HFlags=_flags.HFlags(),
                 textstream: _file.ITextstream=_file.Textstream(),
    ):
        """AbstractLexer object instance initializer.

        Parameters
        ----------
        vendorId : str
            Lexer implementation identifier string (a.k.a. 'vendor ID').
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
        self._vendorId = vendorId

        self._rulesets = []
        if (len(ruleset)): self.PushRuleset(ruleset)

        self._hFlags = handleFlags
        self._ts     = textstream

        return


    def __del__(self):

        # Destructing a textstream object does not guarantee buffer close
        self._ts.Close()
        del self._ts

        return


  # --- PUBLIC METHODS --- #

    def GetTextstream(self) -> _file.ITextstream:
        return self._ts


    def PushRuleset(self, ruleset: _rule.ruleset_t) -> None:
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
        return self._GNT_P1_ScanChars()


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
    def _MatchRule(self, rule: _rule.Rule) -> _misc.ptr_t[_Token]:
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
        ptr_t[Token]
            A regex matcher should not return anything whenever no regex match was found.
            Therefore the return type is a pointer/reference of Token (i.e. Token*).
        """
        pass


  # --- PRIVATE METHODS --- #

    def _NeedsCompilation(self, rule: _rule.Rule) -> bool:
        """Check if the regex pattern matcher in a rule object needs to be compiled.
        """
        needs_compilation = False
        matcher = rule.GetMatcher()
        # If a Matcher object already compiled and stored, check its vendor ID
        if (matcher):
            needs_compilation = matcher.GetVendorId() != self._vendorId
        # If no object Matcher object stored at all
        else:
            needs_compilation = True

        return needs_compilation


    def _CompileRuleset(self, ruleset: _rule.ruleset_t) -> None:
        """Checks and compiles rules within a newly pushed ruleset.

        Whenever a ruleset is pushed, this method will check if all rules have their
        corresponding IMatcher-compatible object set to the matcher type, used by
        a specific lexer/matcher implementation, and compiles if necessary.
        """
        for rule in ruleset:

            # Call the specific lexer implementation's CompileRule() method for regex
            # pattern matcher compilation
            if (self._NeedsCompilation(rule)):
                rule.SetMatcher(self._CompileRule(rule))

            # Comment rules also have an addition rule to be compiled
            if (rule.id == _predefs.comment.id):
                # rule = static_cast<BaseComment*>(rule)->ruleEnd
                rule: _rule.Rule = rule.ruleEnd
                if (self._NeedsCompilation(rule)):
                    rule.SetMatcher(self._CompileRule(rule))

        return


    def _GNT_P1_ScanChars(self) -> _Token:
        """GetNextToken() -- Part 1 --

        This part of the GetNextMethod() method set scans for single characters that are
        usually skipped (SPACE, TAB, NEWLINE). These are predefined rules in the library
        and are scanned independent of a regex engine implementation.

        When a character other than the predefined ones is found, this signals that the
        lexer may scan for user-defined tokens, using the regex engine implementation.
        """
        flags = self._hFlags
        # txt_pos: _file.TextPosition = self._ts.GetTextPosition()
        txt_pos: _file.TextPosition = self._ts._tp

        # NOTE: In CPython it is faster to cache (only) this flag beforehand
        flag_return_space = flags.space is _flags.HFlag.HANDLE_AND_RETURN

        # Scan mainloop
        token: _misc.ptr_t[_Token] = None
        while(1):

            # NOTE: --- METHOD 1 ---
            # buf: str = self._ts.GetStrBuffer()[self._ts.GetStrBufferPosition():]
            buf: str = self._ts._strBuffer[self._ts._strBufferPos:]
            for c, char in enumerate(buf):


            # NOTE: --- METHOD 2 ---
            # c = 0
            # for i in range(self._ts._strBufferPos, self._ts._strBufferSize):
            #     char = self._ts._strBuffer[i]


                # SPACE character
                if (char == ' '):
                    if (flag_return_space):
                        token = _Token(
                            _predefs.space.id,
                            "",
                            _file.TextPosition(
                                txt_pos.pos,
                                txt_pos.col,
                                txt_pos.ln
                            )
                        )
                    _file.TextPosition.UpdateCol(txt_pos)

                # NEWLINE character (UNIX)
                elif (char == '\n'):
                    if (flags.newline == _flags.HFlag.HANDLE_AND_RETURN):
                        token = _Token(
                            _predefs.newline.id,
                            "",
                            _file.TextPosition(
                                txt_pos.pos,
                                txt_pos.col,
                                txt_pos.ln
                            )
                        )
                    _file.TextPosition.UpdateNl(txt_pos)

                # NEWLINE character (WINDOWS)
                # TODO?

                # TAB character
                elif (char == '\t'):
                    if (flags.tab == _flags.HFlag.HANDLE_AND_RETURN):
                        token = _Token(
                            _predefs.tab.id,
                            "",
                            _file.TextPosition(
                                txt_pos.pos,
                                txt_pos.col,
                                txt_pos.ln
                            )
                        )
                    _file.TextPosition.UpdateCol(txt_pos)

                # Else break to the main regex matching loop
                else:
                    self._ts.Update(c)
                    return self._GNT_P2_MatchRegexes()

                # If we didn't break AND we HFlag.HANDLE_AND_RETURN set for one of the above
                # characters
                if (token):
                    self._ts.Update(c+1)
                    return token

                # NOTE: --- METHOD 2 ---
                # c += 1

            # In case the current chunk is entirely exhausted, refill the whole string
            # buffer (in most cases the textstream reached the end of data though, so
            # nothing will be read).
            self._ts.UpdateW()
            # If the textstream has reached the end of data
            if (self._ts.IsEOF()):
                raise _excs.EndOfTextstream()


    def _GNT_P2_MatchRegexes(self) -> _Token:
        """GetNextToken() -- Part 2 --

        This part of the GetNextMethod() method set scans for tokens using the rules as
        defined by the user.

        When no regex match is made, then the lexer will jump to the method to handle
        the unknown token type.
        """
        # txt_pos = self._ts.GetTextPosition()
        txt_pos: _file.TextPosition = self._ts._tp

        # Match mainloop
        ruleset: _rule.ruleset_t = self._rulesets[-1]
        for rule in ruleset:
            # A token is returned if the (implemented) regex pattern matcher found a match.
            token: _misc.ptr_t[_Token] = self._MatchRule(rule)
            if (token):

                # Update positions
                self._ts.Update(len(token.data))
                _file.TextPosition.Update(txt_pos, token.data)

                # Throw ChunkSizeError whenever the token data length is equal to or
                # exceeds the filestream's allocated chunk size.
                # if (token.data.__len__() >= self._ts.GetChunkSize()):
                if (token.data.__len__() >= self._ts._chunkSize):
                    raise _excs.ChunkSizeError(self._ts.GetChunkSize())

                # COMMENTs can easily span across multiple chunks, so it is not wise to
                # create a single regex pattern defining the start and stop. Instead,
                # there is a regex pattern for defining the begin and one defining the
                # end.
                if (token.IsRule(_predefs.comment)):
                    # rule = static_cast<BaseComment*>(rule)->ruleEnd
                    rule: _rule.Rule = rule.ruleEnd
                    temp_token: _Token
                    sstream: _io.StringIO

                    # If a comment token doesn't have to be returned, we can optimize a
                    # little by leaving out some string operations.
                    doReturn = self._hFlags.comment==_flags.HFlag.HANDLE_AND_RETURN
                    if (doReturn):
                        # sstream << token.data
                        sstream = _io.StringIO()
                        sstream.write(token.data)

                    # Comment handling mainloop
                    while(1):

                        # Using the end regex matcher (stored in a comment rule object),
                        # ALL characters are matched until a NEWLINE character (for
                        # singleline comments) or the characters defining the end of a
                        # multiline comment are found.
                        temp_token = self._MatchRule(rule)

                        n1 = len(temp_token.data)
                        # n2 = self._ts.GetChunkSize() - self._ts.GetStrBufferPosition()
                        n2 = self._ts._chunkSize - self._ts._strBufferPos

                        # Update positions
                        self._ts.Update(len(temp_token.data))
                        _file.TextPosition.Update(txt_pos, temp_token.data)

                        # Append the intermediate string data from the temporary comment
                        # token to the parent comment token (which is the token that will
                        # be returned).
                        if (doReturn):
                            # sstream << temp_token.data
                            sstream.write(temp_token.data)
                        del temp_token

                        # The pattern defining the end will match ALL characters until
                        # the characters denoting the end of a comment is found. By doing
                        # this we know when the end is reached if the temporary token's
                        # length is smaller than the readable string data in the chunk
                        # (= chunkSize - strBufferPos).
                        if (n1 < n2):
                            break

                        # If the textstream has reached the end of data
                        if (self._ts.IsEOF()):
                            del token
                            raise _excs.EndOfTextstream()
                            # TODO? UnterminatedCommentError

                    # Check HFlag value if the token should be ignored
                    if (doReturn):
                        sstream.seek(0)  # Seek back to the beginning of the virtual file
                        comment_token = _Token(token.id, sstream.read(), token.position)
                        sstream.close()
                        del token
                        return comment_token
                    else:
                        del token
                        return self.GetNextToken()

                # Continue here if it wasn't a COMMENT

                # Check user-defined HFlag values if the token should be returned or ignored
                for rule in self._hFlags.userFlags:
                    if (token.IsRule(rule)):
                        if (self._hFlags.userFlags[rule] == _flags.HFlag.HANDLE_AND_IGNORE):  ## token.GetId() == flag_key
                            del token
                            return self.GetNextToken()
                        break

                # Else return the token as normally intended
                return token

            # Else no match
            del token

        # If no matches were found at all (no regex pattern matched), the lexer has
        # identified an unknown token.
        # Either an error is raised about the unknown token or it is skipped entirely.
        self._GNT_P3_HandleUnknownToken()


    def _GNT_P3_HandleUnknownToken(self) -> _Token:
        """GetNextToken() -- Part 3 --

        This part of the GetNextMethod() method set handles tokens that had no regex
        match; they are seen as unknown tokens.

        Depending on the HFlag value for 'unknownToken', either an error is raised about
        the unknown token, or it is skipped entirely.
        """
        # Store the start position before skipping any characters
        txt_pos = self._ts.GetTextPosition()
        start_pos = _file.TextPosition(
            txt_pos.pos,
            txt_pos.col,
            txt_pos.ln
        )

        # Skip mainloop
        unknown_data = ""
        buf = self._ts.GetStrBuffer()[self._ts.GetStrBufferPosition():]
        for c, char in enumerate(buf):
            # Store unknown characters until SPACE, TAB or NEWLINE character
            if (char in (' ', '\t', '\n') ):
                unknown_data = buf[:c]
                break
        # If the entire buffer is exhausted
        if (not unknown_data):
            unknown_data = buf

        # If the HFlag value HANDLE_AND_IGNORE is set for 'unknownToken', the unknown
        # data is ignored and the lexer will (try to) return the next token.
        if (self._hFlags.unknownToken == _flags.HFlag.HANDLE_AND_IGNORE):
            return self.GetNextToken()

        # Else (HANDLE_AND_RETURN), raise an UnknownTokenError with the data collected in
        # the above procedures.
        raise _excs.UnknownTokenError(
            start_pos,
            unknown_data
        )
