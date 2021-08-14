"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    import abc

    from ._textposition import TextPosition

# ***************************************************************************************

class ITextstream (metaclass=_.abc.ABCMeta):
    """Common interface to a Textstream object instance.
    """

  # --- INTERFACE METHODS --- #

    @_.abc.abstractmethod
    def Close(self) -> None:
        """Closes and deletes textstream resources.
        """
        pass


    @_.abc.abstractmethod
    def Update(self, n: int) -> None:
        """Updates the textstream's buffer.

        Parameters
        ----------
        n : int
            Amount of characters to read/update.
        """
        pass


    @_.abc.abstractmethod
    def IsEOF(self) -> bool:
        """Evaluates whether the textstream has reached the end of data.
        """
        pass


  # --- INTERFACE GETTERS --- #

    @_.abc.abstractmethod
    def GetTextPosition(self) -> _.TextPosition:
        """Gets the TextPosition object instance.
        """
        pass


    @_.abc.abstractmethod
    def GetBufferString(self) -> str:
        """Gets the currently buffered string value.
        """
        pass


    @_.abc.abstractmethod
    def GetBufferStringSize(self) -> int:
        """Gets the length of the currently buffered string (in characters).
        """
        pass


    @_.abc.abstractmethod
    def GetBufferStringPosition(self) -> int:
        """Gets the index of the current position in the buffered string.
        """
        pass


    # TODO?: GetTextstreamType()  -->  check if memory or buffered
