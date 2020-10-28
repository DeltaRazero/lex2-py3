"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc as _abc

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


  # --- PUBLIC STATIC METHODS --- #

    @staticmethod
    def Reset(textPosition: 'TextPosition') -> None:

        textPosition.pos = 0
        textPosition.col = 0
        textPosition.ln  = 0

        return

# ***************************************************************************************

class ITextstream (metaclass=_abc.ABCMeta):
    """Common interface to a Textstream object instance.
    """

  # --- INTERFACE METHODS --- #

    @_abc.abstractmethod
    def Open(self, fp: str, encoding: str="UTF-8", convertLineEndings: bool=True) -> None:
        """Opens a textfile.

        Parameters
        ----------
        fp : str
            Filepath string.
        encoding : str, optional
            Encoding of textfile. By default "UTF-8".
        convertLineEndings : bool, optional
            Convert line-endings from Windows style to UNIX style. By default 'True'.
        """
        pass

    @_abc.abstractmethod
    def Load(self, strData: str, convertLineEndings: bool=True) -> None:
        """Directly loads string data into the textstream object.

        Parameters
        ----------
        strData : str
            String data. Note that encoding depends on the system-wide encoding.
        convertLineEndings : bool, optional
            Convert line-endings from Windows style to UNIX style. By default 'True'.
        """
        pass

    @_abc.abstractmethod
    def Close(self) -> None:
        """Closes and deletes the textstream's data.
        """
        pass


    @_abc.abstractmethod
    def Seek(self, offset: int, whence: int=0) -> None:
        """Seek to a specified position in the textstream.

        Parameters
        ----------
        offset : int
            Position in the textstream. Direction determined by the argument `whence`.
        whence : int, optional
            Direction of the `offset` argument. By default 0
        """
        pass

    @_abc.abstractmethod
    def Tell(self) -> TextPosition:
        """Gets the current position in the textstream.

        Returns
        -------
        TextPosition
        """
        pass


    @_abc.abstractmethod
    def IsEOF(self) -> bool:
        """Evaluates whether EOF (i.e. end of data) of the textstream has been reached.

        Returns
        -------
        bool
        """
        pass


    @_abc.abstractmethod
    def GetBuffer(self) -> str:
        """Gets the string buffer instance.

        Returns
        -------
        str
        """
        pass

    @_abc.abstractmethod
    def GetBufferLength(self) -> int:
        """Gets the length of the string buffer (in characters).

        Returns
        -------
        int
        """
        pass

    @_abc.abstractmethod
    def GetBufferPosition(self) -> int:
        """Gets the current position in the the string buffer.

        Returns
        -------
        int
        """
        pass

    # TODO?: GetTextstreamType()  -->  check if memory or buffered
