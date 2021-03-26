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
    """Common interface to a TextStream object instance.
    """

  # --- INTERFACE METHODS --- #

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


    # @_abc.abstractmethod
    # def GetChunkSize(self) -> int:
    #     """Gets the chunk size (maximum size of a chunk in bytes).
    #     """
    #     pass


    @_abc.abstractmethod
    def GetBufferString(self) -> str:
        """Gets the currently buffered string value.
        """
        pass


    @_abc.abstractmethod
    def GetBufferStringSize(self) -> int:
        """Gets the length of the currently buffered string (in characters).
        """
        pass


    @_abc.abstractmethod
    def GetBufferStringPosition(self) -> int:
        """Gets the index of the current position in the buffered string.
        """
        pass


    # TODO?: GetTextstreamType()  -->  check if memory or buffered
