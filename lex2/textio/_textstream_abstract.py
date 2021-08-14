"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    from ._intf_textstream import ITextstream
    from ._textposition    import TextPosition

# ***************************************************************************************

class AbstractTextstream (_.ITextstream):

  # --- FIELDS --- #

    _tp : _.TextPosition

    _isEof : bool

    _bufferString : str
    _bufferStringSize : int
    _bufferStringPos  : int


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self) -> None:

        self._tp = _.TextPosition()

        self._isEof = False

        self._bufferString = ""
        self._bufferStringSize = 0
        self._bufferStringPos  = 0

        return


  # --- INTERFACE METHODS --- #

    def IsEOF(self) -> bool:
        return self._isEof


  # --- INTERFACE GETTERS --- #

    def GetTextPosition(self) -> _.TextPosition:
        return self._tp


    def GetBufferString(self) -> str:
        return self._bufferString


    def GetBufferStringSize(self) -> int:
        return self._bufferStringSize


    def GetBufferStringPosition(self) -> int:
        return self._bufferStringPos
