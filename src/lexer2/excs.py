"""Assets of exceptions."""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from . import file as _file

# ***************************************************************************************

class BufferSizeError (Exception):
    """Raised whenever the buffer size of a buffered filestream is too small.
    """

  # --- CONSTRUCTOR --- #

    def __init__(self, bufferSize: int):

        message = "Buffer size of {} is too small!" \
                  .format(bufferSize)

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        return


class UnknownTokenError (Exception):
    """Raised whenever an unknown token type has been encountered.

    Properties
    ----------
    pos : TextPosition
        Position in the textstream where the token occurs.
    data : str
        String data of the unknown token.
    """

  # --- PROPERTIES --- #

    pos  : _file.TextPosition
    data : str


  # --- CONSTRUCTOR --- #

    def __init__(self, pos: _file.TextPosition, data: str):

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
