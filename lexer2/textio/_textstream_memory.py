"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

from ._intf_textstream     import ITextstream  as _ITextstream
from ._textstream_abstract import AbstractTextstream as _AbstractTextstream

# ***************************************************************************************

class Textstream_Memory (_AbstractTextstream, _ITextstream):

  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self,
                 strData: str,
                 convertLineEndings: bool=True
    ) -> None:
        """TextPosition object instance initializer.

        Parameters
        ----------
        chunkSize : int, optional
            Size of a single string buffer chunk (in characters). Note that this number
            will be floored to the nearest even number.

            By default 512.
        """
        super().__init__()

        if (convertLineEndings):  # Convert all line-endings to POSIX format ('\n')
            strData = strData.replace("\r\n", "\n")

        self._bufferString = strData
        self._bufferStringSize = strData.__len__()

        return


    def __del__(self):
        self.Close()
        return


  # --- INTERFACE METHODS --- #

    def Close(self) -> None:

        self._bufferString = ""
        self._bufferStringPos  = 0
        self._bufferStringSize = 0

        return


    def Update(self, n: int) -> None:

        # TODO?: Read buffer and internally update textposition

        self._bufferStringPos += n

        if (self._bufferStringPos >= self._bufferStringSize):
            self._isEof = True

        return
