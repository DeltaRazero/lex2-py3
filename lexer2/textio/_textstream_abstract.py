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

    _bufferString : str
    _bufferStringSize : int
    _bufferStringPos  : int


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self) -> None:

        self._tp = _TextPosition()

        self._bufferString = ""
        self._bufferStringSize = 0
        self._bufferStringPos  = 0

        return


  # --- INTERFACE METHODS --- #

    def IsEOF(self) -> bool:

        # NOTE: In C++ you would just do:
        #
        #     return _bufferedString.empty()
        #
        # return not self._bufferedString
        return not self._bufferStringSize


  # --- INTERFACE GETTERS --- #

    def GetTextPosition(self) -> _TextPosition:
        return self._tp


    def GetBufferString(self) -> str:
        return self._bufferString


    def GetBufferStringSize(self) -> int:
        return self._bufferStringSize


    def GetBufferStringPosition(self) -> int:
        return self._bufferStringPos
