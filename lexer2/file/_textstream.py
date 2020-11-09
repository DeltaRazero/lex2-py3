"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import io as _io

from ._interface_textstream import ITextstream  as _ITextstream
from ._textposition         import TextPosition as _TextPosition

# ***************************************************************************************

class Textstream (_ITextstream):

  # --- FIELDS --- #

    # _encoding   : str
    _convertEol : bool

    _tp : _TextPosition
    _stringStream : _io.StringIO

    _chunkSize  : int
    _chunkSplit : int

    _strBuffer : str
    _strBufferSize : int
    _strBufferPos  : int


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self, chunkSize: int=512) -> None:
        """TextPosition object instance initializer.

        Parameters
        ----------
        chunkSize : int, optional
            Size of a single string buffer chunk (in characters). Note that this number
            will be floored to the nearest even number.
            By default 512.
        """

        self._tp = _TextPosition()
        self._stringStream = _io.StringIO()
        self._stringStream.close()

        self._chunkSize  = chunkSize // 2 * 2
        self._chunkSplit = self._chunkSize // 2

        self.Close()

        return


    def __del__(self):
        self.Close()
        return


  # --- INTERFACE METHODS --- #

    def Open(self, fp: str, encoding: str="UTF-8", convertLineEndings: bool=True) -> None:

        self._encoding   = encoding
        self._convertEol = convertLineEndings

        # Read file in given encoding
        self.Close()
        with open(fp, "rb") as f:
            bin_data = f.read()
            str_data = bin_data.decode(self._encoding, "ignore")
            self._PrepareData(str_data)

        return


    def Load(self, strData: str, convertLineEndings: bool=True) -> None:

        self._convertEol = convertLineEndings

        self.Close()
        self._PrepareData(strData)

        return


    def Close(self) -> None:

        if (not self._stringStream.closed):
            self._stringStream.close()

        self._strBuffer = ""
        self._strBufferSize = 0
        self._strBufferPos  = 0

        _TextPosition.Reset(self._tp)

        return


    def Update(self, n: int) -> None:

        self._strBufferPos   += n

        if (self._strBufferPos > self._chunkSplit):

            n = self._strBufferSize - self._strBufferPos
            if (n):  # NOTE: Last n characters (n=0) doesn't work in Python
                self._strBuffer =\
                    self._strBuffer[-n:] +\
                    self._stringStream.read(self._strBufferPos)
            else:
                self._strBuffer =\
                    self._stringStream.read(self._strBufferPos)

            self._strBufferSize  = len(self._strBuffer)
            self._strBufferPos   = 0

        return


    def UpdateW(self) -> None:

        n = self._chunkSize
        self._strBuffer = self._stringStream.read(n)
        self._strBufferSize = len(self._strBuffer)

        return


    def IsEOF(self) -> bool:

        # NOTE: In C++ you would just do:
        #
        #     return _strBuffer.empty()
        #
        return not self._strBuffer


  # --- INTERFACE GETTERS --- #

    def GetTextPosition(self) -> _TextPosition:
        return self._tp


    def GetChunkSize(self) -> int:
        return self._chunkSize


    def GetStrBuffer(self) -> str:
        return self._strBuffer


    def GetStrBufferSize(self) -> int:
        return self._strBufferSize


    def GetStrBufferPosition(self) -> int:
        return self._strBufferPos


  # --- PRIVATE METHODS --- #

    def _PrepareData(self, strData: str) -> None:

        if (self._convertEol):  # Convert all line-endings to POSIX format ('\n')
            strData = strData.replace("\r\n", "\n")

        self._stringStream = _io.StringIO(strData)
        self.UpdateW()

        return
