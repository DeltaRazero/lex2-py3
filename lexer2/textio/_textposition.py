"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

# struct
class TextPosition:
    """Struct that holds data about the position in a text file.

    Properties:
    -----------
    pos : int
        Absolute position in a text file. Note that multibyte characters are counted as
        one position. Therefore this value should only be used by Textstream objects.
    col : int
        Column at a position in a text file. Counting starts from 0.
    ln : int
        Line at a position in a text file. Counting starts from 0.
    """

  # --- PROPERTIES --- #

    pos : int
    col : int
    ln  : int


  # --- CONSTRUCTOR --- #

    def __init__(self, pos: int=0, col: int=0, ln: int=0) -> None:
        """TextPosition object instance initializer.

        Parameters
        ----------
        pos : int, optional
            Absolute position in a text file. Note that multibyte characters are counted
            as one position. Therefore this value should only be used by Textstream
            objects.
            By default 0
        col : int, optional
            Column at a position in a text file. Counting starts from 0.
            By default 0
        ln : int, optional
            Line at a position in a text file. Counting starts from 0.
            By default 0
        """
        self.pos = pos
        self.col = col
        self.ln  = ln
        return


  # --- PUBLIC METHODS --- #

    @staticmethod
    def Update(textPosition: 'TextPosition', strData: str) -> None:

        for char in strData:

            textPosition.pos += 1
            textPosition.col += 1

            if (char == '\n'):
                textPosition.ln += 1
                textPosition.col = 0

        return


    @staticmethod
    def UpdateCol(textPosition: 'TextPosition') -> None:

        textPosition.pos += 1
        textPosition.col += 1

        return


    @staticmethod
    def UpdateNl(textPosition: 'TextPosition') -> None:

        textPosition.pos += 1
        textPosition.ln  += 1
        textPosition.col = 0

        return


    @staticmethod
    def Reset(textPosition: 'TextPosition') -> None:

        textPosition.pos = 0
        textPosition.col = 0
        textPosition.ln  = 0

        return
