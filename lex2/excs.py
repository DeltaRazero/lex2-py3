"""Components of exceptions."""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import typing as t

    from lex2 import (
        textio,
    )

# ***************************************************************************************

class UnknownTokenError (Exception):
    """Raised whenever an unknown token type has been encountered.

    Readonly Attributes
    -------------------
    pos : TextPosition
        Position in the textstream where the token occurs.
    data : str
        String data of the unknown token.
    """

    pos  : __.textio.TextPosition
    data : str

    # :: CONSTRUCTOR :: #

    def __init__(self, pos: __.textio.TextPosition, data: str):

        self.pos  = pos
        self.data = data

        # Positions are zero-based numbered. Since most, if not all, text editors are
        # one-based numbered, offset line/column positions by one (1).

        message =\
            f"Unknown token type @ ln:{pos.ln+1}|col:{pos.col+1} for the following data:" +\
            f'\n    "{data}"'

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        return


class UnexpectedTokenError (Exception):
    """Raised whenever an unexpected token type has been encountered.

    Readonly Attributes
    -------------------
    pos : TextPosition
        Position in the textstream where the token occurs.
    data : str
        String data of the received token.
    received_id : str
        Identifying string value of received token's type
    expected_ids : List[str]
        List of identifying string values of expected tokens' type.
    """

    pos  : __.textio.TextPosition
    data : str

    received_id: str
    expected_ids : __.t.List[str]

    # :: CONSTRUCTOR :: #

    def __init__(self, pos: __.textio.TextPosition, data: str, received_id: str, expected_ids: __.t.List[str]):

        self.pos  = pos
        self.data = data

        self.received_id  = received_id
        self.expected_ids = expected_ids

        # Positions are zero-based numbered. Since most, if not all, text editors are
        # one-based numbered, offset line/column positions by one (1).

        expected_ids_msg = ", ".join([f'"{eid}"' for eid in expected_ids])
        message =\
            f'Unexpected token type "{received_id}" @ ln:{pos.ln+1}|col:{pos.col+1}' +\
            f'\nExpected the following type(s): {expected_ids_msg}, for the following data:' +\
            f'\n    "{data}"'

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        return


class EOD (Exception):
    """Raised whenever a lexer has reached the end of input data from a textstream.
    """

    def __init__(self):
        # Call the base class constructor with the parameters it needs
        super().__init__()
        return
