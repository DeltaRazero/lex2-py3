"""Components of exceptions."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    from lex2 import (
        textio,
    )

# ***************************************************************************************

class TokenError (Exception):
    """Base class for token errors.

    Readonly Properties
    -------------------
    pos : TextPosition
        Position in the textstream where the token occurs.
    data : str
        String data of the unknown token.
    """

    # :: READONLY PROPERTIES :: #

    pos  : __.textio.TextPosition
    data : str


    # :: CONSTRUCTOR :: #

    def __init__(self, pos: __.textio.TextPosition, data: str, message: str):

        # Positions are zero-based numbered. Since most, if not all, text editors are
        # one-based numbered, offset line/column positions by one (1).

        message =\
            f"{message} @ ln:{pos.ln+1}|col:{pos.col+1}" + "\n" + f'"{data}"'

        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.pos  = pos
        self.data = data

        return


class UnknownTokenError (TokenError):
    """Raised whenever an unknown token type has been encountered.

    Readonly Properties
    -------------------
    pos : TextPosition
        Position in the textstream where the token occurs.
    data : str
        String data of the unknown token.
    """

    # :: CONSTRUCTOR :: #

    def __init__(self, pos: __.textio.TextPosition, data: str):

        # Call the base class constructor with the parameters it needs
        super().__init__(
            pos=pos, data=data,
            message="Unknown token type"
        )

        return


class UnexpectedTokenError (TokenError):
    """Raised whenever an unexpected token type has been encountered.

    Readonly Properties
    -------------------
    pos : TextPosition
        Position in the textstream where the token occurs.
    data : str
        String data of the unknown token.
    """

    # :: CONSTRUCTOR :: #

    def __init__(self, pos: __.textio.TextPosition, data: str, id: str):

        # Call the base class constructor with the parameters it needs
        super().__init__(
            pos=pos, data=data,
            message=f'Unexpected token type \"{id}\"'
        )

        return


class EndOfData (Exception):
    """Raised whenever a lexer has reached the end of input data.
    """

    def __init__(self):
        # Call the base class constructor with the parameters it needs
        super().__init__()
        return
