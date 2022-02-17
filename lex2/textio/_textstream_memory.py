"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    from ._textstream_core import (
        ITextstream,
        AbstractTextstream,
    )

# ***************************************************************************************

class Textstream_Memory (__.AbstractTextstream, __.ITextstream):

  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self,
                 strData: str,
                 convertLineEndings: bool
    ) -> None:
        """TextPosition object instance initializer.

        Parameters
        ----------
        strData : str
            String data to directly load. Note that encoding depends on the system-wide
            encoding.
        convertLineEndings : bool
            Convert line-endings from Windows style to UNIX style.
        """
        super().__init__()

        # Convert all line-endings to POSIX format ('\n')
        if (convertLineEndings):
            strData = strData.replace("\r\n", "\n")

        self._bufferString = strData
        self._bufferStringSize = len(strData)  # TODO: Make this StringBufferSize --> size is binary/chars/bytes, length for amount of code points

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

        self._UpdatePosition(n)

        # If current position Signal EOF
        if (self._bufferStringPos >= self._bufferStringSize):
            self._isEof = True

        return
