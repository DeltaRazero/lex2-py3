"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
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
    def Close(self) -> None:
        """Closes and deletes textstream resources.
        """
        pass


    @_abc.abstractmethod
    def Update(self, n: int) -> None:
        """Updates the textstream's buffer.

        Parameters
        ----------
        n : int
            Amount of characters to read/update.
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
