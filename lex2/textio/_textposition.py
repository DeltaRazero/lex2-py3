"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

# struct
class TextPosition:
    """Struct that holds data about the position in a textstream."""

    __slots__ = ('pos', 'col', 'ln')

    # :: PUBLIC ATTRIBUTES :: #

    pos : int
    """
    Absolute position in a textstream. Counting starts from 0.
    Note that multi-byte characters are counted as one position.
    """
    col : int
    """Column of a position in a textstream. Counting starts from 0."""
    ln  : int
    """Line of a position in a textstream. Counting starts from 0."""


    # :: CONSTRUCTOR :: #

    def __init__(self, pos: int=0, col: int=0, ln: int=0) -> None:
        """TextPosition object instance initializer.

        Parameters
        ----------
        pos : int, optional
            Absolute position in a text file. Note that multi-byte characters are counted
            as one position.
        col : int, optional
            Column at a position in a text file. Counting starts from 0.
        ln : int, optional
            Line at a position in a text file. Counting starts from 0.
        """
        self.pos = pos
        self.col = col
        self.ln  = ln
        return
