"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import io       as _io
import typing   as _t
import pathlib  as _pl
import warnings as _warnings

from ._interface_textstream import ITextstream  as _ITextstream
from ._textposition         import TextPosition as _TextPosition

# ***************************************************************************************

class BufferedTextstream (_ITextstream):

  # --- FIELDS --- #

    _encoding   : str
    _convertEol : bool

    _tp : _TextPosition
    _f  : _t.IO[bytes]

    _chunkSize  : int
    _chunkSplit : int

    # NOTE: Size of the binary buffer should always be equal to the chunk size
    _binBuffer : bytes

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
        self._f  = _io.BytesIO()
        self._f.close()

        self._chunkSize  = chunkSize // 2 * 2
        self._chunkSplit = self._chunkSize // 2

        self.Close()

        return


    def __del__(self):
        self.Close()
        return


  # --- INTERFACE METHODS --- #

    def Open(self,
             fp: _t.Union[str, _pl.Path],
             encoding: str="UTF-8",
             convertLineEndings: bool=True
    ) -> None:

        self._encoding   = encoding
        self._convertEol = convertLineEndings

        # Read file in given encoding
        self.Close()
        # NOTE: open() accepts both 'str' and 'Path' arguments, so conversion in this
        # method is not needed.
        self._f = open(fp, "rb")
        self.UpdateW()

        return


    def Load(self, strData: str, convertLineEndings: bool=True) -> None:

        _warnings.warn(
            "Usage of Load() in a buffered texstream is highly discouraged.\n"+\
            "Consider using the default ('unbuffered') textstream instead or use Open().",
            RuntimeWarning
        )

        self._encoding   = "UTF-8"
        self._convertEol = convertLineEndings

        self.Close()
        self._f = _io.BytesIO( strData.encode(encoding="UTF-8") )

        return


    def Close(self) -> None:

        if (not self._f.closed):
            self._f.close()

        self._binBuffer = bytes()

        self._strBuffer = ""
        self._strBufferSize = 0
        self._strBufferPos  = 0

        _TextPosition.Reset(self._tp)

        return


    def Update(self, n: int) -> None:

        self._strBufferPos += n

        if (self._strBufferPos > self._chunkSplit):

            self._strBuffer =\
                self._strBuffer[self._strBufferPos:]\
                +\
                self._Read(self._strBufferPos)

            self._strBufferSize  = len(self._strBuffer)
            self._strBufferPos   = 0

        elif (self._strBufferPos == self._strBufferSize):

            pass

        return


    def UpdateW(self) -> None:

        self._Read(self._chunkSize)

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

    @staticmethod
    def _BinaryStringLength(s: str) -> int:
        return len(s.encode("UTF-8"))


    def _Read(self, nChars: int) -> str:

        # Some characters may not have been decoded due to missing bytes (multibyte encoding)
        self._binBuffer =\
            self._binBuffer[self._BinaryStringLength(self._strBuffer):] +\
            self._f.read(nChars)

        self._strBuffer = self._binBuffer.decode(self._encoding, "ignore")
        if (self._convertEol):  # Convert all line-endings to POSIX format ('\n')
            self._strBuffer = self._strBuffer.replace("\r\n", "\n")
        self._strBufferSize = len(self._strBuffer)

        # If we read 2 or 4 byte characters, keep reading until we reach the amount of
        # characters specified by nChars.
        if (self._strBufferSize < nChars):

            while(1):

                byte = self._f.read(1)

                # We actually check for the length here. If it is 0, then we read no
                # bytes, indicating EOF.
                if (not byte):
                    break

                self._binBuffer += byte

                self._strBuffer = self._binBuffer.decode(self._encoding, "ignore")
                if (self._convertEol):  # Convert all line-endings to POSIX format ('\n')
                    self._strBuffer = self._strBuffer.replace("\r\n", "\n")
                self._strBufferSize = len(self._strBuffer)

        return self._strBuffer
