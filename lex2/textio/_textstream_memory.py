"""<internal>"""

'''
zlib License

(C) 2020-2021 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class _:
    '<imports>'

    from ._intf_textstream     import ITextstream
    from ._textstream_abstract import AbstractTextstream

# ***************************************************************************************

class Textstream_Memory (_.AbstractTextstream, _.ITextstream):

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
        self._bufferStringSize = len(strData)

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

        old_pos = self._bufferStringPos
        self._bufferStringPos += n

        # Update textposition
        _tp = self._tp  # NOTE: It's faster to lookup/cache the variable in Python like this
        for char in self._bufferString[ old_pos : self._bufferStringPos ]:

            _tp.pos += 1
            _tp.col += 1

            if (char == '\n'):
                _tp.ln += 1
                _tp.col = 0

        # If current position Signal EOF
        if (self._bufferStringPos >= self._bufferStringSize):
            self._isEof = True

        return
