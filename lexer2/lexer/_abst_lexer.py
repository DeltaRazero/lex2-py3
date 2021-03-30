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
from .. import textio  as _textio
from .. import predefs as _predefs
from .. import misc    as _misc
from .. import _rule
from .. import _flags

from .. import ILexer       as _ILexer
from .. import IMatcher     as _IMatcher
from .. import Token        as _Token
from .. import LexerOptions as _LexerOptions

# ***************************************************************************************

class AbstractLexer (_textio.TextIO, _ILexer, metaclass=_abc.ABCMeta):
    """Abstract base class of an ILexer implementation.
    """

  # --- FIELDS --- #

    _vendorId: str

    _rulesets : _t.List[_rule.ruleset_t]
    _options  : _LexerOptions


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    @_abc.abstractmethod
    def __init__(self,
                 vendorId: str,
                 ruleset: _rule.ruleset_t=[],
                 options: _LexerOptions=_LexerOptions(),
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
        super().__init__()

        self._vendorId = vendorId

        self._rulesets = []
        if (len(ruleset)): self.PushRuleset(ruleset)

        self._options = options

        return


    def __del__(self):

        super().__del__()

        return


  # --- PUBLIC METHODS --- #

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


    def GetOptions(self) -> _LexerOptions:
        return self._options


    def GetNextToken(self) -> _Token:
        # TODO: CHeck if stream open
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
        txt_pos: _textio.TextPosition = self._ts.GetTextPosition()
        # txt_pos: _textio.TextPosition = self._ts._tp


        # Scan mainloop
        token: _misc.ptr_t[_Token] = None
        while(1):

            # NOTE: --- METHOD 1 ---
            buf: str = self._ts.GetBufferString()[self._ts.GetBufferStringPosition():]
            # buf: str = txt_stream._bufferString[txt_stream._bufferStringPos:] # TODO: test
            for c, char in enumerate(buf):


            # NOTE: --- METHOD 2 ---
            # c = 0
            # for i in range(self._ts._strBufferPos, self._ts._strBufferSize):
            #     char = self._ts._strBuffer[i]


                # SPACE character
                if (char == ' '):
                    if (self._options.returnSpace):
                        token = _Token(
                            _predefs.space.id,
                            "",
                            _textio.TextPosition(
                                txt_pos.pos,
                                txt_pos.col,
                                txt_pos.ln
                            )
                        )
                    _textio.TextPosition.UpdateCol(txt_pos)

                # NEWLINE character (UNIX)
                elif (char == '\n'):
                    if (self._options.returnNewline):
                        token = _Token(
                            _predefs.newline.id,
                            "",
                            _textio.TextPosition(
                                txt_pos.pos,
                                txt_pos.col,
                                txt_pos.ln
                            )
                        )
                    _textio.TextPosition.UpdateNl(txt_pos)

                # NEWLINE character (WINDOWS)
                # TODO?
                # elif (char == '\r'):
                #     if (flags.newline == _flags.HFlag.HANDLE_AND_RETURN):
                #         token = _Token(
                #             _predefs.newline.id,
                #             "",
                #             _textio.TextPosition(
                #                 txt_pos.pos,
                #                 txt_pos.col,
                #                 txt_pos.ln
                #             )
                #         )
                #     _textio.TextPosition.UpdateCol(txt_pos)
                #     self._ts.Update(1)
                #
                #     # Making the assumption here it is followed by a \n character
                #     self.GetNextToken()
                #
                #     if (token):
                #         return token

                # TAB character
                elif (char == '\t'):
                    if (self._options.returnTab):
                        token = _Token(
                            _predefs.tab.id,
                            "",
                            _textio.TextPosition(
                                txt_pos.pos,
                                txt_pos.col,
                                txt_pos.ln
                            )
                        )
                    _textio.TextPosition.UpdateCol(txt_pos)

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
        txt_pos: _textio.TextPosition = self._ts.GetTextPosition()
        # txt_pos: _textio.TextPosition = self._ts._tp

        # Match mainloop
        ruleset: _rule.ruleset_t = self._rulesets[-1]
        for rule in ruleset:
            # A token is returned if the (implemented) regex pattern matcher found a match.
            token: _misc.ptr_t[_Token] = self._MatchRule(rule)
            if (token):

                # Update positions
                self._ts.Update(len(token.data))
                _textio.TextPosition.Update(txt_pos, token.data)

                # TODO: REMOVE?
                # Throw ChunkSizeError whenever the token data length is equal to or  # TODO: update comment
                # exceeds the filestream's allocated chunk size.
                # if (token.data.__len__() >= self._ts.GetBufferStringSize()):
                # if (token.data.__len__() >= self._ts._bufferStringSize):
                    # raise _excs.ChunkSizeError(self._ts.GetBufferStringSize())  # TODO: update exception

                # COMMENTs can easily span across multiple chunks, so it is not wise to
                # create a single regex pattern defining the start and stop. Instead,
                # there is a regex pattern for defining the begin and one defining the
                # end.
                if (token.IsRule(_predefs.comment)):
                    # rule = static_cast<BaseComment*>(rule)->ruleEnd
                    rule: _rule.Rule = rule.ruleEnd #type: ignore
                    temp_token: _Token
                    sstream: _io.StringIO

                    # If a comment token doesn't have to be returned, we can optimize a
                    # little by leaving out some string operations.
                    do_return = self._options.returnComment
                    if (do_return):
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
                        # n2 = txt_stream.GetChunkSize() - txt_stream.GetBufferedStringPosition()
                        # n2 = txt_stream._chunkSize - txt_stream._bufferedStringPos
                        n2 = self._ts.GetBufferStringSize() - self._ts.GetBufferStringPosition() # TODO: TEST

                        # Update positions
                        self._ts.Update(len(temp_token.data))
                        _textio.TextPosition.Update(txt_pos, temp_token.data)

                        # Append the intermediate string data from the temporary comment
                        # token to the parent comment token (which is the token that will
                        # be returned).
                        if (do_return):
                            # sstream << temp_token.data
                            sstream.write(temp_token.data)
                        del temp_token

                        # The regex pattern object will continue to match ALL characters
                        # until the sequence of characters that defines termination of
                        # a comment is found.
                        # In practice, this means that the while-loop can be stopped
                        # whenever the currently loaded buffer string holds the comment
                        # terminator sequence of characters.
                        if (n1 < n2):
                            break

                        # If the textstream has reached the end of data
                        if (self._ts.IsEOF()):
                            del token
                            raise _excs.EndOfTextstream()
                            # TODO? UnterminatedCommentError

                    # Return or ignore COMMENT token accordingly
                    if (do_return):
                        sstream.seek(0)  # Seek back to the beginning of the virtual file
                        comment_token = _Token(token.id, sstream.read(), token.position)
                        sstream.close()
                        del token
                        return comment_token
                    else:
                        del token
                        return self.GetNextToken()

                # Continue here if it isn't a COMMENT token

                # Check user-defined flag values if the token should be returned or
                # ignored. If no key-pair can be found, default to False
                ignore_token = self._options.returnRule.get(token.id, False)
                if (ignore_token):
                    del token
                    return self.GetNextToken()

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
        txt_pos: _textio.TextPosition = self._ts.GetTextPosition()

        # Store the start position before skipping any characters
        start_pos = _textio.TextPosition(
            txt_pos.pos,
            txt_pos.col,
            txt_pos.ln
        )

        # Skip mainloop
        unknown_data = ""
        buf = self._ts.GetBufferString()[self._ts.GetBufferStringPosition():]
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
        # if (not self._options.returnUnknownToken):
            # return self.GetNextToken()

        # Else (HANDLE_AND_RETURN), raise an UnidentifiedTokenError with the data collected
        # in the above procedures.
        raise _excs.UnidentifiedTokenError(
            start_pos,
            unknown_data
        )
