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
    from lex2.util.types import (
        PtrType,
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
        # Variable caching to prevent slow dictionary lookups
        ts = self._ts
        buf: str         = ts._string_buffer
        buf_size: int    = ts._string_buffer_size
        current_pos: int = ts._string_buffer_pos

        # The character at the current position has already been read, so skip it
        i = current_pos + 1
        while (i < buf_size):
            if (buf[i] != matching_char):
                break
            i += 1

        return i - current_pos


    def _split_by_separators(self) -> __.Token:
        """
        Scans for separator characters (SPACE, TAB, NEWLINE).

        The separator characters are skipped by default, but can be returned or ignored
        entirely by setting the corresponding options for them. Scanning is done
        independently of a regex engine.

        If no separator characters are found, proceed to matching rules.
        """
        # Variable caching to prevent slow dictionary lookups
        opts = self._options
        ts   = self._ts
        # tp: __.textio.TextPosition = self._ts.get_text_position()
        tp: __.textio.TextPosition = ts._tp

        token: __.PtrType[__.Token] = None
        char: str
        goto_matchers = False

        # Scan mainloop
        # while (not ts.is_eof()):
        while (not ts._is_eof):
            # char = ts.get_string_buffer()[ ts.get_string_buffer_position() ]
            char: str = ts._string_buffer[ ts._string_buffer_pos ]

            # SPACE character
            if (char == ' '):
                opt = opts.space
                if (opt.ignored): goto_matchers = True
                else:
                    n = self._count_char_occurrences(' ')
                    if (opt.returns): token = __.Token(
                        __.predefs.space.id,
                        " "*n,
                        __.textio.TextPosition(
                            tp.pos,
                            tp.col,
                            tp.ln
                        )
                    )
                    ts.update(n)

            # NEWLINE character (UNIX)
            elif (char == '\n'):
                opt = opts.newline
                if (opt.ignored): goto_matchers = True
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
                    ts.update(1)

            # NEWLINE character (Windows)
            elif (char == '\r'):
                # The old Macintosh-style newline (single '\r' character) is considered
                # obsolete, and strings using the format are unsupported in this library.
                # Whenever such a character is encountered, it is assumed that it is part
                # of a Windows-style newline, i.e. "\r\n".
                opt = opts.newline
                if (opt.ignored): goto_matchers = True
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
                    ts.update(2)

            # TAB character
            elif (char == '\t'):
                opt = opts.tab
                if (opt.ignored): goto_matchers = True
                else:
                    n = self._count_char_occurrences('\t')
                    if (opt.returns): token = __.Token(
                        __.predefs.tab.id,
                        "\t"*n,
                        __.textio.TextPosition(
                            tp.pos,
                            tp.col,
                            tp.ln
                        )
                    )
                    ts.update(n)

            # Not a separator character, so proceed to matching rules
            else:
                return self._match_rules()

            if (goto_matchers):
                return self._match_rules()

            if (token):
                return token

        # If EOF is reached
        raise __.excs.EOF()


    def _match_rules(self) -> __.Token:
        """
        Scans for rules in the currently active ruleset using regex matchers.

        If no rule matches, proceed to throw an unknown token type error.
        """
        # Variable caching to prevent slow dictionary lookups
        ts = self._ts
        ar = self._active_ruleset
        tp: __.textio.TextPosition = ts._tp

        token = __.Token(
            pos=__.textio.TextPosition(
                tp.pos,
                tp.col,
                tp.ln
            )
        )

        # Match mainloop
        for rule in ar:
            # No null check necessary, as pushing a ruleset guarantees that each rule has
            # their matcher instances set.
            if (rule._matcher.match(ts, token)): # type: ignore[reportOptionalMemberAccess]
                token.id = rule.id

                # Update text position and new data into buffer
                ts.update(len(token.data))

                # Check if the token type should be returned and return token accordingly
                if (self._options.id_returns.get(rule.id, rule.returns)):
                    return token
                del token
                return self.get_next_token()

        # If no match has been found, proceed to throw an unknown token type error.
        # Include all characters until a separator character (SPACE, TAB or NEWLINE) or EOF
        unknown_data = ""
        while(not self._ts.is_eof()):

            n_chars_read = 0
            buf = self._ts.get_string_buffer()[self._ts.get_string_buffer_position():]

            for n_chars_read, char in enumerate(buf):
                if (char in (' ', '\t', '\n', '\r')):
                    unknown_data += buf[:n_chars_read]
                    raise __.excs.UnknownTokenError(token.pos, unknown_data)

            # If the buffer is exhausted, the unknown data is continued in the next buffer
            unknown_data += buf
            self._ts.update(n_chars_read)

        raise __.excs.UnknownTokenError(token.pos, unknown_data)
