"""Components of exceptions."""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from . import textio as _textio

# ***************************************************************************************

class ChunkSizeError (Exception):
    """Raised whenever the chunk size of a filestream is too small.
    """

  # --- CONSTRUCTOR --- #

    def __init__(self, bufferSize: int):

        msg = f"Chunk size of {bufferSize} is too small!"

        # Call the base class constructor with the parameters it needs
        super().__init__(msg)

        return


class UnidentifiedTokenError (Exception):
    """Raised whenever an unknown token type has been encountered.

    Readonly Properties
    -------------------
    pos : TextPosition
        Position in the textstream where the token occurs.
    data : str
        String data of the unknown token.
    """

  # --- READONLY PROPERTIES --- #

    pos  : _textio.TextPosition
    data : str


  # --- CONSTRUCTOR --- #

    def __init__(self, pos: _textio.TextPosition, data: str):

        # Positions are zero-based numbered. Since most, if not all, text editors are
        # one-based numbered, offset line/column positions by one (1).
        msg = f"Unidentified token at {pos.ln+1}:{pos.col+1}"

        message = "Unidentified token at {}:\n\n    \"{}\"" \
                  .format(
                      # Internally, the positions start at 0-based indexes,
                      # however most, if not all, text editors start at 1-based
                      # indexes.
                      "ln: {} col: {}".format(pos.ln+1, pos.col+1),
                      data
                  )

        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.pos  = pos
        self.data = data

        return


class EndOfTextstream (Exception):
    """Raised whenever a lexer has reached the end of a textstream.
    """

    def __init__(self):

        message = "End of data reached."

        # Call the base class constructor with the parameters it needs
        super().__init__(message)
