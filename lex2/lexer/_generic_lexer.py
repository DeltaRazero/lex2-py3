"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import abc
    import typing as t

    from ._base_lexer import BaseLexer

    from lex2 import (
        excs,
        textio,
        predefs,
    )
    from lex2 import (
        ruleset_t,
        Rule,
        Token,
    )
    from lex2._util.types import (
        ptr_t
    )

# ***************************************************************************************

class GenericLexer (__.BaseLexer):
    """An generic implementation of ILexer.
    """

  # --- CONSTRUCTOR & DESTRUCTOR --- #

    @__.abc.abstractmethod
    def __init__(self):
        """AbstractLexer object instance initializer.
        """
        super().__init__()

        return


    def __del__(self):
        super().__del__()
        return


  # --- PUBLIC METHODS --- #

    def GetNextToken(self) -> __.Token:
        if (not self._ts):
            raise RuntimeError("No open textstream to read data from")
        return self._split_by_separators()


  # --- PRIVATE METHODS --- #

    def _CountCharOccurrences(self, matchingChar: str) -> int:
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


    def _split_by_separators(self) -> __.Token:
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
        txt_pos: __.textio.TextPosition = self._ts._tp

        token: __.ptr_t[__.Token] = None
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
                n = self._CountCharOccurrences(' ')

                if (opt.ignores): goto_matcher = True
                else:
                    if (opt.returns): token = __.Token(
                        __.predefs.space.id,
                        " "*n,
                        __.textio.TextPosition(
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
                    if (opt.returns): token = __.Token(
                        __.predefs.newline.id,
                        "\n",
                        __.textio.TextPosition(
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
                    if (opt.returns): token = __.Token(
                        __.predefs.newline.id,
                        "\n",
                        __.textio.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                    self._ts.Update(2)

            # TAB character
            elif (char == '\t'):

                opt = opts.tab
                n = self._CountCharOccurrences('\t')

                if (opt.ignores): goto_matcher = True
                else:
                    if (opt.returns): token = __.Token(
                        __.predefs.tab.id,
                        "\t"*n,
                        __.textio.TextPosition(
                            txt_pos.pos,
                            txt_pos.col,
                            txt_pos.ln
                        )
                    )
                    self._ts.Update(n)

            # Not a special character, i.e. a regular character
            else:
                goto_matcher = True

            if (goto_matcher):
                return self._match_rules()

            if (token):
                return token

        # If EOF is reached
        raise __.excs.EndOfData()


    def _match_rules(self) -> __.Token:
        """
        This method scans for tokens using the rules (as defined by the user) in a given
        ruleset.

        If no rule (regex pattern) matches, then the lexer will proceed to throw an
        UnidentifiedTokenError, signaling this back to the caller program.
        """

        # Match mainloop
        for rule in self._active_ruleset:

            # A token is returned if the (implemented) regex pattern matcher found a match.

            # A non-empty string is returned if the (implemented) regex pattern matcher
            # found a match.
            # NOTE: Because of the checks performed during pushing a ruleset, it is
            # guaranteed that a rule's GetMatcher() method returns a Matcher instance and
            # not a null reference.
            # match: __.ptr_t[str] = rule.GetMatcher().Match(self._ts)
            match: __.ptr_t[str] = rule._matcher.Match(self._ts)
            if (match):

                # Store if the token type should be returned to the user
                returns = self._options.idReturns.get(rule.id, rule.returns)

                # Create a token object
                # tp: __.textio.TextPosition = self._ts.GetTextPosition()
                tp: __.textio.TextPosition = self._ts._tp
                token = __.Token(
                    rule.id,
                    match,
                    __.textio.TextPosition(
                        tp.pos,
                        tp.col,
                        tp.ln
                    )
                )

                # Update new data into buffer
                self._ts.Update(len(match))

                # TODO?: Buffer size warning if len(token.data) >= self._ts.GetBufferStringSize()

                # if (token.IsRule(__.predefs.comment)):
                #     self._GNT_HandleComment(rule, token, returns) # TODO: TO REMOVE

                # Return token accordingly
                if (returns):
                    return token
                del token
                return self.GetNextToken()

            # Else no match
            del match

        # If no matches were found at all (i.e. no regex pattern was matched), then the
        # lexer has found an unidentified token type.
        self._GNT_RaiseUnidentifiedTokenError()

    '''
    def _GNT_HandleComment(self, rule: __.Rule, token: __.Token, returns: bool) -> None:
        """
        This method handles processing of a COMMENT token.

        Comments can easily span across multiple buffers, so it is not wise to create a
        single regex pattern defining the start and stop. Instead, there is a separate
        rule for defining them. This method handles that special functionality.
        """

        # rule = static_cast<BaseComment*>(rule)->endRule
        rule = __.t.cast(__.predefs.BaseComment, rule).endRule

        # Comment handling mainloop
        while(1):

            # Using the end regex matcher (stored in a comment rule object),
            # ALL characters are matched until a NEWLINE character (for
            # singleline comments) or the characters defining the end of a
            # multiline comment are found.
            # match: __.ptr_t[str] = rule.GetMatcher().Match(self._ts)
            match: __.ptr_t[str] = rule._matcher.Match(self._ts)

            # NOTE: It is guaranteed that a match here will not be a null reference.
            n1 = len(match)
            # n2 = self._ts.GetBufferStringSize() - self._ts.GetBufferStringPosition()
            n2 = self._ts._bufferStringSize - self._ts._bufferStringPos

            # Update positions
            self._ts.Update(n1)

            # Append the string data to the comment token if it should be
            # returned to the user.
            if (returns):
                token.data += match

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
                raise __.excs.EndOfData()
                # TODO? UnterminatedCommentError

        return
    '''

    def _GNT_RaiseUnidentifiedTokenError(self) -> None:
        """
        This method handles raising an exception whenever an unidentified token type has
        been determined (i.e. no regex pattern was matched).
        """

        txt_pos: __.textio.TextPosition = self._ts.GetTextPosition()

        # Store the start position before skipping any characters
        pos = __.textio.TextPosition(
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
                    raise __.excs.UnidentifiedTokenError(pos, unidentified_data)

            # If the buffer is exhausted, meaning the unidentified data is continued in
            # the following buffer
            unidentified_data += buf
            self._ts.Update(n_chars_read)
