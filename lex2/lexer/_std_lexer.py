"""<internal>"""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ******************************************************************************

class __:
  '<imports>'

  import abc

  from ._lexer_base import LexerBase

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

# ******************************************************************************

class StdLexer (__.LexerBase):
  """An generic implementation of a lexer.
  """

  # :: PRIVATE ATTRIBUTES :: #

  _current_token : __.PtrType[__.Token]

  # :: CONSTRUCTOR & DESTRUCTOR :: #

  @__.abc.abstractmethod
  def __init__(self):
    super().__init__()

    self._current_token = None
    return

  def __del__(self):
    super().__del__()
    return

  # :: PUBLIC METHODS :: #

  def peek_token(self) -> __.Token:
    if (self._current_token):
      return self._current_token
    self._current_token = self.next_token()
    return self._current_token

  def next_token(self) -> __.Token:
    if (not self._ts):
      raise RuntimeError("No open textstream to read data from.")
    # If a token was peeked, return that first.
    if (self._current_token):
      self._current_token
    return self._tokenize_separators()

  # :: PRIVATE METHODS :: #

  def _count_char_length(self, matching_char: str) -> int:
    """Counts the amount of continuous occurrences of a given character at the current position in the textstream.
    """
    # Variable caching to prevent slow dictionary lookups.
    ts = self._ts
    buffer: str      = ts._buffer
    buffer_size: int = ts._buffer_size
    current_pos: int = ts._buffer_pos

    # The character at the current position has already been read, so skip it.
    i = current_pos + 1
    while (i < buffer_size):
      if (buffer[i] != matching_char):
        break
      i += 1
    return i - current_pos

  def _tokenize_separators(self) -> __.Token:
    """
    Tokenizes separator characters (SPACE, TAB, NEWLINE).

    Separator characters are skipped by default, although they can be returned
    or ignored altogether by setting the corresponding option flags. Scanning is
    done independently of a regex engine.

    If no separator characters are found, the rules will be tokenized.
    """
    # Variable caching to prevent slow dictionary lookups.
    opts = self._options
    ts   = self._ts
    tp: __.textio.TextPosition = ts._tp

    token: __.PtrType[__.Token] = None
    goto_matchers = False

    # while (not ts.is_eof()):
    while (not ts._is_eof):
      # match (ts.get_buffer()[ts.get_buffer_position()]):
      match (ts._buffer[ts._buffer_pos]):
        # SPACE character.
        case ' ':
          opt = opts.space
          if (opt.ignored):
            goto_matchers = True
          else:
            n = self._count_char_length(' ')
            if (opt.returns):
              token = __.Token(
                __.predefs.space.id,
                " "*n,
                __.textio.TextPosition(tp.pos, tp.col, tp.ln),
            )
            ts.update(n)

        # NEWLINE (UNIX) character.
        case '\n':
          opt = opts.newline
          if (opt.ignored):
            goto_matchers = True
          else:
            if (opt.returns):
              token = __.Token(
                __.predefs.newline.id,
                "\n",
                __.textio.TextPosition(tp.pos, tp.col, tp.ln),
            )
            ts.update(1)

        # NEWLINE (Windows) character.
        case '\r':
          # Old Macintosh-style newline (single '\r' character) is considered
          # obsolete and is not supported. We assume a Windows-style newline.
          opt = opts.newline
          if (opt.ignored):
            goto_matchers = True
          else:
            if (opt.returns):
              token = __.Token(
                __.predefs.newline.id,
                "\n",
                __.textio.TextPosition(tp.pos, tp.col, tp.ln),
            )
            ts.update(2)

        # TAB character.
        case ' ':
          opt = opts.tab
          if (opt.ignored):
            goto_matchers = True
          else:
            n = self._count_char_length('\t')
            if (opt.returns):
              token = __.Token(
                __.predefs.tab.id,
                "\t"*n,
                __.textio.TextPosition(tp.pos, tp.col, tp.ln),
            )
            ts.update(n)

        # Not a separator character; proceed to match rules.
        case _:
          return self._tokenize_rules()

      # If ignored, proceed to match rules as well.
      if (goto_matchers):
        return self._tokenize_rules()

      # If not ignored and token should return.
      if (token):
        return token

    # Reaching this means that we've reached the end of the stream.
    raise __.excs.EOF()

  def _tokenize_rules(self) -> __.Token:
    """
    Scans for rules in the currently active ruleset using regex matchers.

    If no rule matches, an unknown token type error is thrown.
    """
    # Variable caching to prevent slow dictionary lookups
    ts = self._ts
    ar = self._active_ruleset
    tp: __.textio.TextPosition = ts._tp

    # Preallocate token object which a matcher will populate.
    token = __.Token(
      pos=__.textio.TextPosition(tp.pos, tp.col, tp.ln),
    )

    for rule in ar:
      # No null check necessary, as pushing a rule guarantees that each rule
      # has had their matcher instance set.
      # if (rule.get_matcher().match(ts, token)):
      if (rule._matcher.match(ts, token)): # type: ignore[reportOptionalMemberAccess]
        token.id = rule.id
        # Update text position and stream new data into buffer.
        ts.update(len(token.data))

        # Check if the token type should be returned, else return the next
        # token.
        if (self._options.id_returns.get(rule.id, rule.returns)):
          return token
        del token
        return self.next_token()

    # If no match has been found, we throw an error.
    # Include all characters until a separator character (SPACE, TAB, NEWLINE)
    # or EOF.
    SEPARATOR_CHARS = (' ', '\t', '\n', '\r')
    unknown_data = ""
    while (not self._ts.is_eof()):
      n_chars_read = 0
      unread_buffer_data = self._ts.get_buffer()[self._ts.get_buffer_position():]

      for n_chars_read, char in enumerate(unread_buffer_data):
        if (char in SEPARATOR_CHARS):
          unknown_data += unread_buffer_data[:n_chars_read]
          raise __.excs.UnknownTokenError(token.pos, unknown_data)

      # If the buffer is exhausted, the unknown data is continued in the next
      # buffer.
      unknown_data += unread_buffer_data
      self._ts.update(n_chars_read)

    raise __.excs.UnknownTokenError(token.pos, unknown_data)
