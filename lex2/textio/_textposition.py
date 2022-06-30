"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

# struct
class TextPosition:
    """Struct that holds data about the position in a textstream.

    Attributes
    ----------
    pos : int
        Absolute position in a textstream. Counting starts from 0.
        Note that multibyte characters are counted as one position.
    col : int
        Column of a position in a textstream. Counting starts from 0.
    ln : int
        Line of a position in a textstream. Counting starts from 0.
    """

    __slots__ = ('pos', 'col', 'ln')

    # :: PUBLIC ATTRIBUTES :: #

    pos : int
    col : int
    ln  : int


    # :: CONSTRUCTOR :: #

    def __init__(self, pos: int, col: int, ln: int) -> None:
        """TextPosition object instance initializer.

        Parameters
        ----------
        pos : int, optional
            Absolute position in a text file. Note that multibyte characters are counted
            as one position. Therefore this value should only be used by Textstream
            objects.
        col : int, optional
            Column at a position in a text file. Counting starts from 0.
        ln : int, optional
            Line at a position in a text file. Counting starts from 0.
        """
        self.pos = pos
        self.col = col
        self.ln  = ln
        return
