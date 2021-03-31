"""<internal>"""

'''
zlib License

(C) 2020 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

import pathlib as _pl
import typing  as _t
import sys     as _sys

from ._intf_textstream     import ITextstream  as _ITextstream
from ._textstream_abstract import AbstractTextstream as _AbstractTextstream

# ***************************************************************************************

_SYSTEM_ENCODING = _sys.stdin.encoding

# ***************************************************************************************

class Textstream_Disk (_AbstractTextstream, _ITextstream):

  # --- FIELDS --- #

    _encoding : str
    _f : _t.IO[bytes]

    # NOTE: Size of the binary buffer should always be equal to the chunk size
    _buffer : bytes
    _bufferSize  : int

    _bufferStringSplit : int


    _undecodedBytes : bytes

    _reachedEOF : bool


  # --- CONSTRUCTOR & DESTRUCTOR --- #

    def __init__(self,
                 fp: _t.Union[str, _pl.Path],
                 bufferSize: int,
                 encoding: str,
                 convertLineEndings: bool,
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

        self._encoding   = encoding
        self._convertEOL = convertLineEndings

        # # Because a dual buffer is needed, divide this number?
        # bufferSize = bufferSize // 2

        # Enforce minimum buffer size of 128
        if (bufferSize<256):
            # TODO: Raise warnings to stdout
            bufferSize=256

        # bufferSize=34

        self._bufferSize = bufferSize // 2 * 2

        self._undecodedBytes     = bytes()
        self._undecodedBytesSize = 0

        self._reachedEOF = False

        self._f = open(fp, "rb")
        self._buffer = bytes()

        self._Read(self._bufferSize)
        self._RefreshBufferStringMeta()

        return


    def __del__(self):
        self.Close()
        return


  # --- INTERFACE METHODS --- #

    def Close(self) -> None:

        if (self._f.closed):
            return

        self._f.close()
        self._buffer       = bytes()
        self._bufferString = ""

        return


    def Update(self, n: int) -> None:

        self._bufferStringPos += n

        if (n < 1):
            # raise Exception("Read at least one")
            return

        # Can't be possible to read more than the allocated buffer size
        if (n > self._bufferSize):
            raise MemoryError()

        if (self._reachedEOF):
            if (self._bufferStringPos >= self._bufferStringSize):
                self._isEof = True

        elif (self._bufferStringPos > self._bufferStringSplit):

            # Remainder to fill entire string buffer (in bytes)
            remainder = self._bufferSize - self._bufferStringSize

            self._bufferString =\
                self._bufferString[self._bufferStringPos:]\
                +\
                self._Read(self._bufferStringPos + remainder)

            self._RefreshBufferStringMeta()

        return




  # --- PRIVATE METHODS --- #

    @staticmethod
    def _BinaryStringLength(s: str) -> int:
        return len(s.encode(_SYSTEM_ENCODING))


    def _RefreshBufferStringMeta(self) -> None:

        self._bufferStringPos   = 0
        self._bufferStringSize  = len(self._bufferString)
        self._bufferStringSplit = self._bufferStringSize // 2

        # print("---")
        # print(self._bufferString)

        return


    def _Read(self, nBytes: int) -> str:

        nBytes -= self._undecodedBytesSize
        if (nBytes < 0):
            raise Exception("lower than 0, buffer size too small!")  # TODO: Cleanup

        temp = self._f.read(nBytes)

        # If the amount of bytes read is lower than given as input, then EOF is reached
        bytes_read = len(temp)
        if (bytes_read < nBytes):
            self._reachedEOF = True
            nBytes = bytes_read

            # In case the buffer is completely empty
            # if (not temp  and  nBytes):
            #     nBytes = 0

        # If some multi-byte encoded characters had missing bytes, insert the already
        # read files at the beginning of the buffer. That way multi-byte encoded
        # characters can be fully decoded.
        if (self._undecodedBytes):

            self._buffer =\
                self._undecodedBytes + temp

        # Else just move the already read bytes to the buffer
        else:
            self._buffer = temp

        # Decode to a string object with given text encoding
        self._bufferString = self._buffer.decode(self._encoding, errors="ignore")
        if (self._convertEOL):
            self._bufferString = self._bufferString.replace("\r", "")
            # self._bufferString = self._bufferString.replace("\r\n", "\n")

        # In case multi-byte characters are present, some characters may not have been
        # decoded. We keep those undecoded bytes and insert them at the begin of the next
        # buffer update.
        n_undecoded_bytes = nBytes - self._BinaryStringLength(self._bufferString) + self._undecodedBytesSize
        # If convert EOL, then \r bytes disappearing don't count
        if (self._convertEOL):
            n_undecoded_bytes -= self._buffer.count(b"\r\n")

        if (n_undecoded_bytes):
            self._undecodedBytes     = self._buffer[-n_undecoded_bytes:]
            self._undecodedBytesSize = n_undecoded_bytes
        else:
            # No need to re-init if already empty
            if (self._undecodedBytes):
                self._undecodedBytes     = bytes()
                self._undecodedBytesSize = 0

        return self._bufferString
