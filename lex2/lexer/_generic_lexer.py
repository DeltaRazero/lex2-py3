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

    from ._base_lexer import BaseLexer

    from lex2 import (
        excs,
        textio,
        predefs,
    )
    from lex2 import (
        Token,
    )
    from lex2._util.types import (
        ptr_t
    )

# ***************************************************************************************

class GenericLexer (__.BaseLexer):
    """An generic implementation of ILexer.
    """

    # :: CONSTRUCTOR & DESTRUCTOR :: #

    @__.abc.abstractmethod
    def __init__(self):
        """AbstractLexer object instance initializer.
        """
        super().__init__()

        return


    def __del__(self):
        super().__del__()
        return


    # :: PUBLIC METHODS :: #

    def get_next_token(self) -> __.Token:
        if (not self._ts):
            raise RuntimeError("No open textstream to read data from")
        return self._split_by_separators()


    # :: PRIVATE METHODS :: #

    def _count_char_occurrences(self, matching_char: str) -> int:
        """Counts the amount of continuous occurrences of a given character at the current position in the textstream.
        """
        # NOTE: These variables are cached here to make lookup times faster. This is not
        # necessary in compiled languages.
        buf: str         = self._ts._string_buffer
        buf_size: int    = self._ts._string_buffer_size
        current_pos: int = self._ts._string_buffer_pos

        # NOTE: The character at the current position has already been read, so skip it
        i = current_pos + 1
        while (i < buf_size):

            char: str = buf[i]
            if (char != matching_char):
                break
            i += 1

        return i - current_pos


    def _split_by_separators(self) -> __.Token:
        """
        Scans for the special seperator characters (SPACE, TAB, NEWLINE).

        The seperator characters are skipped by default, but can be returned or ignored
        entirely by setting the corresponding options for them. Scanning is done
        independently of a regex engine.

        If no seperator characters are found, proceed to matching rules.
        """
        # Cache some variables to prevent constant lookups
        opts = self._options
        # tp: _textio.TextPosition = self._ts.get_text_position()
        tp: __.textio.TextPosition = self._ts._tp

        token: __.ptr_t[__.Token] = None
        char: str
        goto_matchers: bool

        # Scan mainloop
        while (not self._ts.is_eof()):

            # char = self._ts.get_string_buffer()[ self._ts.get_string_buffer_position() ]
            char: str = self._ts._string_buffer[ self._ts._string_buffer_pos ]
            goto_matchers = False

            # SPACE character
            if (char == ' '):

                opt = opts.space
                n = self._count_char_occurrences(' ')

                if (opt.ignores): goto_matchers = True
                else:
                    if (opt.returns): token = __.Token(
                        __.predefs.space.id,
                        " "*n,
                        __.textio.TextPosition(
                            tp.pos,
                            tp.col,
                            tp.ln
                        )
                    )
                    self._ts.update(n)

            # NEWLINE character (UNIX)
            elif (char == '\n'):

                opt = opts.newline

                if (opt.ignores): goto_matchers = True
                else:
                    if (opt.returns): token = __.Token(
                        __.predefs.newline.id,
                        "\n",
                        __.textio.TextPosition(
                            tp.pos,
                            tp.col,
                            tp.ln
                        )
                    )
                    self._ts.update(1)

            # NEWLINE character (Windows)
            elif (char == '\r'):

                # NOTE: Files using the old Macintosh NEWLINE style (a single '\r' character)
                # is extremely uncommon and therefore not supported. It is always assumed
                # that this is going to be a Windows NEWLINE character ("\r\n").

                opt = opts.newline

                if (opt.ignores): goto_matchers = True
                else:
                    if (opt.returns): token = __.Token(
                        __.predefs.newline.id,
                        "\n",
                        __.textio.TextPosition(
                            tp.pos,
                            tp.col,
                            tp.ln
                        )
                    )
                    self._ts.update(2)

            # TAB character
            elif (char == '\t'):

                opt = opts.tab
                n = self._count_char_occurrences('\t')

                if (opt.ignores): goto_matchers = True
                else:
                    if (opt.returns): token = __.Token(
                        __.predefs.tab.id,
                        "\t"*n,
                        __.textio.TextPosition(
                            tp.pos,
                            tp.col,
                            tp.ln
                        )
                    )
                    self._ts.update(n)

            # Not a seperator character, so proceed to matching rules
            else:
                goto_matchers = True

            if (goto_matchers):
                return self._match_rules()

            if (token):
                return token

        # If EOF is reached
        raise __.excs.EndOfData()


    def _match_rules(self) -> __.Token:
        """
        Scans for rules in the currently active ruleset using regex matchers.

        If no rule matches, proceed to throw an unknown token type error.
        """
        # Match mainloop
        for rule in self._active_ruleset:

            # A string is returned when a match is found, else NULL.
            # NOTE: When a ruleset is pushed, it is guaranteed that a rule always has a
            # matcher instance set.
            # match: __.ptr_t[str] = rule.get_matcher().match(self._ts)
            match: __.ptr_t[str] = rule._matcher.match(self._ts)
            if (match):
                # Store if the token type should be returned to the user
                returns = self._options.id_returns.get(rule.id, rule.returns)

                # Create a token instance
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

                # Update text position and new data into buffer
                self._ts.update(len(match))

                # Return token accordingly
                if (returns):
                    return token
                del token
                return self.get_next_token()

            # Else no match
            del match

        # If no match has been found, proceed to throw an unknown token type error.
        self._raise_unknown_token_error()


    def _raise_unknown_token_error(self) -> None:
        """Raises an error whenever an unknown token type error has been found.
        """
        tp: __.textio.TextPosition = self._ts.get_text_position()

        # Store the current position as start position first
        pos = __.textio.TextPosition(
            tp.pos,
            tp.col,
            tp.ln
        )

        # Include all characters until a seperator character (SPACE, TAB or NEWLINE) or EOF
        unknown_data = ""
        while(1):

            n_chars_read: int = 0
            buf = self._ts.get_string_buffer()[self._ts.get_string_buffer_position():]

            for n_chars_read, char in enumerate(buf):
                # Store data and throw exception
                if (char in (' ', '\t', '\n', '\r')):
                    unknown_data += buf[:n_chars_read]
                    raise __.excs.UnknownTokenError(pos, unknown_data)

            # If the buffer is exhausted, the unknown data is continued in the next buffer
            unknown_data += buf
            self._ts.update(n_chars_read)

            if (self._ts.is_eof()):
                raise __.excs.UnknownTokenError(pos, unknown_data)
