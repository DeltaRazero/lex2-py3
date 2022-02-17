"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import abc

    from ._textposition import TextPosition

# ***************************************************************************************

class ITextstream (metaclass=__.abc.ABCMeta):
    """Common interface to a Textstream object instance.
    """

  # --- INTERFACE METHODS --- #

    @__.abc.abstractmethod
    def Close(self) -> None:
        """Closes and deletes textstream resources.
        """
        ...


    @__.abc.abstractmethod
    def Update(self, n: int) -> None:
        """Updates the textstream's buffer.

        Parameters
        ----------
        n : int
            Amount of characters to read/update. Must be a positive number.
        """
        ...


    @__.abc.abstractmethod
    def IsEOF(self) -> bool:
        """Evaluates whether the textstream has reached the end of data.
        """
        ...


  # --- INTERFACE GETTERS --- #

    @__.abc.abstractmethod
    def GetTextPosition(self) -> __.TextPosition:
        """Gets the TextPosition object instance.
        """
        ...


    @__.abc.abstractmethod
    def GetBufferString(self) -> str:
        """Gets the currently buffered string value.
        """
        ...


    @__.abc.abstractmethod
    def GetBufferStringSize(self) -> int:
        """Gets the length of the currently buffered string (in characters).
        """
        ...


    @__.abc.abstractmethod
    def GetBufferStringPosition(self) -> int:
        """Gets the index of the current position in the buffered string.
        """
        ...


    # TODO?: GetTextstreamType()  -->  check if memory or buffered


# ***************************************************************************************

class AbstractTextstream (ITextstream): # pylint: disable=abstract-method
    """Abstract base class of an ITextstream implementation.
    """

  # --- FIELDS --- #

    _tp : __.TextPosition

    _isEof : bool

    _bufferString : str
    _bufferStringSize : int
    _bufferStringPos  : int


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self) -> None:

        self._tp = __.TextPosition()

        self._isEof = False

        self._bufferString = ""
        self._bufferStringSize = 0
        self._bufferStringPos  = 0

        return


  # --- INTERFACE METHODS --- #

    def IsEOF(self) -> bool:
        return self._isEof


  # --- INTERFACE GETTERS --- #

    def GetTextPosition(self) -> __.TextPosition:
        return self._tp


    def GetBufferString(self) -> str:
        return self._bufferString


    def GetBufferStringSize(self) -> int:
        return self._bufferStringSize


    def GetBufferStringPosition(self) -> int:
        return self._bufferStringPos


  # --- PROTECTED METHODS --- #

    def _UpdatePosition(self, n: int) -> None:
        """Updates text position."""

        # Cache variable for faster lookup times in Python. Not necessary for compiled languages
        _tp = self._tp

        old_pos = self._bufferStringPos
        self._bufferStringPos += n

        chars = self._bufferString[ old_pos : self._bufferStringPos ]
        strlen = len(chars)
        sizeof = strlen # in bytes

        _tp.pos += strlen

        lns = chars.count('\n')
        if (lns):
            _tp.col = 0
            _tp.ln += lns
            # for (int i=size-1; i>=0; i--)
            for i in range(sizeof-1, -1, -1):
                if (chars[i] == '\n'):
                    # chars  = chars[ i+1 : ]
                    # strlen = sizeof(chars)
                    strlen = strlen - i - 1
                    break

        _tp.col += strlen

        return

        # Older slower code, not portable without unicode-aware strings
        """
        _tp = self._tp
        for char in self._bufferString[ old_pos : self._bufferStringPos ]:

            _tp.pos += 1
            _tp.col += 1

            if (char == '\n'):
                _tp.ln += 1
                _tp.col = 0

        return
        """
