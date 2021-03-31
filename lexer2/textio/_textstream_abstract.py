"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._intf_textstream import ITextstream  as _ITextstream
from ._textposition    import TextPosition as _TextPosition

# ***************************************************************************************

class AbstractTextstream (_ITextstream):

  # --- FIELDS --- #

    _tp : _TextPosition

    _isEof : bool

    _bufferString : str
    _bufferStringSize : int
    _bufferStringPos  : int


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self) -> None:

        self._tp = _TextPosition()

        self._isEof = False

        self._bufferString = ""
        self._bufferStringSize = 0
        self._bufferStringPos  = 0

        return


  # --- INTERFACE METHODS --- #

    def IsEOF(self) -> bool:
        return self._isEof


  # --- INTERFACE GETTERS --- #

    def GetTextPosition(self) -> _TextPosition:
        return self._tp


    def GetBufferString(self) -> str:
        return self._bufferString


    def GetBufferStringSize(self) -> int:
        return self._bufferStringSize


    def GetBufferStringPosition(self) -> int:
        return self._bufferStringPos
