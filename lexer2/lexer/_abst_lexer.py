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
from .. import opts    as _opts
from .. import textio  as _textio
from .. import predefs as _predefs
from .. import misc    as _misc

from .. import ruleset_t as _ruleset_t
from .. import Rule      as _Rule
from .. import Token     as _Token
from .. import ILexer    as _ILexer
from .. import IMatcher  as _IMatcher

# ***************************************************************************************

class AbstractLexer (_textio.TextIO, _ILexer, metaclass=_abc.ABCMeta):
    """Abstract base class of an ILexer implementation.
    """

  # --- FIELDS --- #

    _vendorId: str

    _rulesets : _t.List[_ruleset_t]
    _active_ruleset : _ruleset_t

    _options  : _opts.LexerOptions


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    @_abc.abstractmethod
    def __init__(self,
                 vendorId: str,
                 ruleset: _ruleset_t=[],
                 options: _opts.LexerOptions=_opts.LexerOptions(),
    ):
        """AbstractLexer object instance initializer.

        Parameters
        ----------
        vendorId : str
            Lexer implementation identifier string (a.k.a. 'vendor ID').
        ruleset : ruleset_t, optional
            Initial ruleset.
            By default []
        options : LexerOptions, optional
            Struct specifying processing options of the lexer.
            By default LexerOptions()
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

    def PushRuleset(self, ruleset: _ruleset_t) -> None:
        # Before pushing the ruleset, we check if the pattern matchers (saved in the rule
        # objects) are compiled for the specific lexer implementation this function is called from.
        self._CompileRuleset(ruleset)
        self._rulesets.append(ruleset)
        self._active_ruleset = self._rulesets[-1]
        return


    def PopRuleset(self) -> None:
        self._rulesets.pop()
        self._active_ruleset = self._rulesets[-1]
        return


    def ClearRulesets(self) -> None:
        self._rulesets.clear()
        return


    def GetOptions(self) -> _opts.LexerOptions:
        return self._options


    def GetNextToken(self) -> _Token:
        if (not self._ts):
            raise RuntimeError("No open textstream to read data from")
        return self._GNT_SplitBySeperatators()


  # --- PROTECTED METHODS --- #

    @_abc.abstractmethod
    def _CompileRule(self, rule: _Rule) -> _IMatcher:
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
    def _MatchRule(self, rule: _Rule) -> _misc.ptr_t[_Token]:
        """Requests implemented lexer to match a rule.

        The implementation calls the GetMatcher() method from a Rule object to match a
        regex pattern.
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

    def _CompileRuleset(self, ruleset: _ruleset_t) -> None:
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

            # Comment rules have an addition rule to be compiled
            if (rule.id == _predefs.comment.id):
                # rule = static_cast<BaseComment*>(rule)->endRule
                rule: _Rule = rule.endRule
                if (self._NeedsCompilation(rule)):
                    rule.SetMatcher(self._CompileRule(rule))

        return


    def _NeedsCompilation(self, rule: _Rule) -> bool:
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


    def _CountOccurrences(self, matchingChar: str) -> int:
        """Counts the amount of continuous occurrences of a given character at the current position.
        """

        # NOTE: For in CPython, it is faster to cache these variables in order to prevent
        # dictionary lookup every time the variable is accessed.
        buf: str         = self._ts._bufferString
        buf_size: int    = self._ts._bufferStringSize
        current_pos: int = self._ts._bufferStringPos

        # NOTE: Since this method assumes the character at the current position has
        # already been, skip that position
        i = current_pos + 1
        while (i < buf_size):

            char: str = buf[i]
            if (char != matchingChar):
                break

            i += 1

        return i - current_pos


    def _GNT_SplitBySeperatators(self) -> _Token:
        """
        This method serves as scanner for the special seperator characters (SPACE, TAB,
        NEWLINE); these characters are usually skipped. Scanning for these characters
        are implemented independent of a regex engine implementation.

        When a character other than the predefined ones is found, the lexer may scan
        for user-defined rules, using the regex engine implementation.
        """

        # Precaching some variables to avoid constant lookups in CPython
        opts = self._options
        # txt_pos: _textio.TextPosition = self._ts.GetTextPosition()
        txt_pos: _textio.TextPosition = self._ts._tp

        token: _misc.ptr_t[_Token] = None
        char: str
        goto_matcher: bool

        # Scan mainloop
        while (not self._ts.IsEOF()):

            # char = self._ts.GetBufferString()[ self._ts.GetBufferStringPosition() ]
            char = self._ts._bufferString[ self._ts._bufferStringPos ]
            goto_matcher = False

        # SPACE character
            if (char == ' '):

                opt = opts.space
                n = self._CountOccurrences(' ')

                if (opt.ignores): goto_matcher = True
                else:
                    if (opt.returns): token = _Token(
                        _predefs.space.id,
                        " "*n,
                        _textio.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                    self._ts.Update(n)

        # NEWLINE character (UNIX)
            elif (char == '\n'):

                opt = opts.newline

                if (opt.ignores): goto_matcher = True
                else:
                    if (opt.returns): token = _Token(
                        _predefs.newline.id,
                        "\n",
                        _textio.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                    self._ts.Update(1)

        # NEWLINE character (WINDOWS)
            elif (char == '\r'):

                # NOTE: I honestly don't think this library will ever be used to process
                # files using the Macintosh NEWLINE style (just a single '\r' character
                # by itself). Therefore, the assumption is made that encountered such
                # a character will always be followed by a '\n' character.

                opt = opts.newline

                if (opt.ignores): goto_matcher = True
                else:
                    if (opt.returns): token = _Token(
                        _predefs.newline.id,
                        "\n",
                        _textio.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                    self._ts.Update(2)

        # TAB character
            elif (char == '\t'):

                opt = opts.tab
                n = self._CountOccurrences('\t')

                if (opt.ignores): goto_matcher = True
                else:
                    if (opt.returns): token = _Token(
                        _predefs.tab.id,
                        "\t"*n,
                        _textio.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                    self._ts.Update(n)

        # Not a special character
            else:
                goto_matcher = True

            if (goto_matcher):
                return self._GNT_MatchRegexes(self._active_ruleset)

            if (token):
                return token

        # If EOF is reached
        raise _excs.EndOfData()


    def _GNT_MatchRegexes(self, ruleset: _ruleset_t) -> _Token:
        """
        This method scans for tokens using the rules (as defined by the user) in a given
        ruleset.

        If no rule (regex pattern) matches, then the lexer will proceed to throw an
        UnidentifiedTokenError, signaling this back to the caller program.
        """

        # Match mainloop
        for rule in ruleset:

            # A token is returned if the (implemented) regex pattern matcher found a match.
            token: _misc.ptr_t[_Token] = self._MatchRule(rule)
            if (token):

                # Update new data into buffer
                self._ts.Update(len(token.data))

                # TODO?: Buffer size warning if len(token.data) >= self._ts.GetBufferStringSize()

                # return_token = self._options.idReturns.get(rule.id, rule.returns)
                return_token = self._options.idReturns.get(rule.id, rule.returns)

                if (token.IsRule(_predefs.comment)):
                    return self._GNT_HandleComment(rule, token, return_token)

                # Return token accordingly
                if (not return_token):
                    del token
                    return self.GetNextToken()
                return token

            # Else no match
            del token

        # If no matches were found at all (i.e. no regex pattern was matched), then the
        # lexer has found an unidentified token type.
        self._GNT_RaiseUnidentifiedTokenError()


    def _GNT_HandleComment(self, rule: _Rule, token: _Token, returnToken: bool) -> _Token:
        """
        This method handles processing of a COMMENT token.

        Comments can easily span across multiple buffers, so it is not wise to create a
        single regex pattern defining the start and stop. Instead, there is a separate
        rule for defining them. This method handles that special functionality.
        """

        temp_token: _Token

        # t_rule = static_cast<BaseComment*>(rule)->endRule
        t_rule: _Rule = rule.endRule

        # Comment handling mainloop
        while(1):

            # Using the end regex matcher (stored in a comment rule object),
            # ALL characters are matched until a NEWLINE character (for
            # singleline comments) or the characters defining the end of a
            # multiline comment are found.
            temp_token = self._MatchRule(t_rule)

            n1 = len(temp_token.data)
            # n2 = self._ts.GetBufferStringSize() - self._ts.GetBufferStringPosition()
            n2 = self._ts._bufferStringSize - self._ts._bufferStringPos

            # Update positions
            self._ts.Update(n1)

            # Append the intermediate string data from the temporary comment
            # token to the parent comment token (which is the token that will
            # be returned).
            if (returnToken):
                token.data += temp_token.data
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
                raise _excs.EndOfData()
                # TODO? UnterminatedCommentError

        # Return or ignore COMMENT token accordingly
        if (returnToken):
            return token
        else:
            del token
            return self.GetNextToken()


    def _GNT_RaiseUnidentifiedTokenError(self) -> None:
        """
        This method handles raising an exception whenever an unidentified token type has
        been determined (i.e. no regex pattern was matched).
        """

        txt_pos: _textio.TextPosition = self._ts.GetTextPosition()

        # Store the start position before skipping any characters
        pos = _textio.TextPosition(
            txt_pos.pos,
            txt_pos.col,
            txt_pos.ln
        )

        # Include all characters until SPACE, TAB or NEWLINE
        unidentified_data = ""
        while(1):

            n_chars_read: int = 0
            buf = self._ts.GetBufferString()[self._ts.GetBufferStringPosition():]

            for n_chars_read, char in enumerate(buf):

                # Store data and throw exception
                if (char in (' ', '\t', '\n')):
                    unidentified_data += buf[:n_chars_read]
                    raise _excs.UnidentifiedTokenError(pos, unidentified_data)

            # If the buffer is exhausted, meaning the unidentified data is continued in
            # the following buffer
            unidentified_data += buf
            self._ts.Update(n_chars_read)
