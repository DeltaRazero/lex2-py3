"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import abc as _abc

from ._textposition import TextPosition as _TextPosition

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
        """Closes and deletes the textstream's (buffer) data.
        """
        pass


    @_abc.abstractmethod
    def Update(self, n: int) -> None:
        """Reads data and updates the textstream's buffer.

        Parameters
        ----------
        n : int
            Amount of characters to read/update.
        """
        pass


    @_abc.abstractmethod
    def UpdateW(self) -> None:
        """Reads data and updates the whole textstream's buffer.
        """
        pass


    @_abc.abstractmethod
    def IsEOF(self) -> bool:
        """Evaluates whether the textstream has reached the end of data.
        """
        pass


  # --- INTERFACE GETTERS --- #

    @_abc.abstractmethod
    def GetTextPosition(self) -> _TextPosition:
        """Gets the TextPosition object instance.
        """
        pass


    @_abc.abstractmethod
    def GetChunkSize(self) -> int:
        """Gets the chunk size (of the string buffer).
        """
        pass


    @_abc.abstractmethod
    def GetStrBuffer(self) -> str:
        """Gets the string buffer.
        """
        pass

    @_abc.abstractmethod
    def GetStrBufferSize(self) -> int:
        """Gets the string buffer size.
        """
        pass

    @_abc.abstractmethod
    def GetStrBufferPosition(self) -> int:
        """Gets the current position in the string buffer.
        """
        pass


    # TODO?: GetTextstreamType()  -->  check if memory or buffered
