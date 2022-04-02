"""<internal>"""

'''
zlib License

(C) 2020-2022 DeltaRazero
All rights reserved.
'''

# ***************************************************************************************

class __:
    '<imports>'

    import pathlib as pl
    import typing  as t
    import sys
    import warnings

    from ._textstream_core import (
        ITextstream,
        BaseTextstream,
        TextstreamType,
    )

# ***************************************************************************************

_SYSTEM_ENCODING = __.sys.stdin.encoding

# ***************************************************************************************

class TextstreamDisk (__.BaseTextstream, __.ITextstream):
    """Abstract base class of an ITextstream implementation.
    """

    # :: FIELDS :: #

    _encoding : str
    _convert_eol : bool

    _f_is_eof : bool
    _f : __.t.IO[bytes]

    # NOTE: To clarify, _buffer_size is the the amount of bytes, while _string_buffer_size
    # is be the amount of decoded characters, i.e. character codepoints.

    # If _string_buffer is unicode-aware, then a separate byte/char buffer is required so
    # any undecoded characters are preserved
    _byte_buffer : bytes
    _byte_buffer_size  : int
    _n_undecoded_bytes : int

    _string_buffer_split : int


    # :: CONSTRUCTOR & DESTRUCTOR :: #

    def __init__(self,
                 fp: __.t.Union[str, __.pl.Path],
                 buffer_size: int,
                 encoding: str,
                 convert_line_endings: bool,
    ) -> None:
        """TextPosition object instance initializer.

        Parameters
        ----------
        fp : Union[str, Path]
            String or Path object of a textfile to open.
        buffer_size : int
            Size of the buffer used to split a file into segments. Keep in mind that in
            order to completely capture a token, it must be smaller or equal to the size
            allocated to the buffer by this argument. NOTE: this number will be floored
            to the nearest even number.
        encoding : str
            Encoding of text in the file.
        convert_line_endings : bool
            Convert line-endings from Windows style to UNIX style.
        """
        super().__init__(__.TextstreamType.DISK)

        self._encoding   = encoding
        self._convert_eol = convert_line_endings

        # Enforce minimum buffer size
        if (buffer_size<256):
            buffer_size=256
            __.warnings.warn(category=RuntimeWarning, message=
                f"Set the buffer size to {buffer_size} as that is the minimum required size to functionally operate."
            )

        self._byte_buffer_size = buffer_size // 2 * 2 # Ensure even number
        self._byte_buffer = bytes()
        self._n_undecoded_bytes = 0

        self._f_is_eof = False
        self._f = open(fp, "rb") # pylint: disable=consider-using-with

        self._read(self._byte_buffer_size)
        self._refresh_string_buffer_meta()

        return


    def __del__(self):
        self.close()
        return


    # :: INTERFACE METHODS :: #

    def close(self) -> None:
        if (self._f.closed):
            return

        self._f.close()
        self._byte_buffer = bytes()
        self._string_buffer = ""

        return


    def update(self, n: int) -> None:
        if (n < 1):
            if (n < 0):
                raise ValueError("Requested update size is invalid (smaller than 0)!")
            return

        # Can't be possible to read more than the allocated buffer size
        if (n > self._string_buffer_size):
            raise ValueError("Requested update size is invalid (bigger than the allocated buffer string size)!")

        self._update_position(n)

        if (self._f_is_eof):
            if (self._string_buffer_pos >= self._string_buffer_size):
                self._is_eof = True

        elif (self._string_buffer_pos > self._string_buffer_split):

        # IF SYSTEM-ENCODING (UTF-8) OR ASCII-ONLY STRINGS
            # # Amount of chars read by the textstream
            # chars_read = len( self._string_buffer[:self._string_buffer_pos] )

            # self._string_buffer =\
            #     self._string_buffer[self._string_buffer_pos:]\
            #     +\
            #     self._read(chars_read)

            # self._refresh_string_buffer_meta()

        # IF UNICODE-AWARE STRINGS
            # Remainder to fill entire string buffer in bytes (for when multibyte characters are read)
            remainder = self._byte_buffer_size - self._binary_string_length(self._string_buffer)

            # Amount of bytes read by the textstream
            bytes_read = self._binary_string_length(
                self._string_buffer[:self._string_buffer_pos]
            )

            self._string_buffer =\
                self._string_buffer[self._string_buffer_pos:]\
                +\
                self._read(bytes_read + remainder)

            self._refresh_string_buffer_meta()
        # ENDIF

        return


    # :: PRIVATE METHODS :: #

    # @staticmethod
    def _binary_string_length(self, s: str) -> int:
        return len(s.encode(self._encoding))

    # NOTE: In the case that only system decoding is needed (which in most cases is going
    # to be UTF-8), then usage of the static method below is encouraged instead.

    # @staticmethod
    # def _binary_string_length(s: str) -> int:
    #    return len(s.encode(_SYSTEM_ENCODING))


    def _refresh_string_buffer_meta(self) -> None:

        self._string_buffer_pos  = 0
        self._string_buffer_size = len(self._string_buffer)
        self._string_buffer_split = self._string_buffer_size // 2

        # NOTE: For debugging purposes
        # print(self._binary_string_length(self._string_buffer))

        return


    def _read(self, n_bytes: int) -> str:

    # IF SYSTEM-ENCODING (UTF-8) OR ASCII-ONLY STRINGS
        # self._string_buffer = str( self._f.read(n_bytes) )
        # return self._string_buffer

    # IF UNICODE-AWARE STRINGS
        n_bytes -= self._n_undecoded_bytes

        temp = self._f.read(n_bytes)

        # If the amount of bytes read is lower than given as input, then EOF is reached
        bytes_read = len(temp)
        if (bytes_read < n_bytes):
            self._f_is_eof = True
            n_bytes = bytes_read

        # If some multi-byte encoded characters had missing bytes, insert the already
        # read bytes at the beginning of the buffer. That way multi-byte encoded
        # characters can be fully decoded.
        if (self._n_undecoded_bytes):
            self._byte_buffer = self._byte_buffer + temp
        # Else just move the already read bytes to the buffer
        else:
            self._byte_buffer = temp

        # Decode to a string object with given text encoding
        self._string_buffer = self._byte_buffer.decode(encoding=self._encoding, errors="ignore")
        if (self._convert_eol):
            self._string_buffer = self._string_buffer.replace("\r", "")

        # In case multi-byte characters are present, some characters may not have been
        # decoded (at the end). We keep those undecoded bytes and insert them at the
        # beginning of the next buffer when updating.
        n_undecoded_bytes = n_bytes - self._binary_string_length(self._string_buffer) + self._n_undecoded_bytes
        # If converting line endings, then \r bytes that are filtered out don't count
        # towards this number
        if (self._convert_eol):
            n_undecoded_bytes -= self._byte_buffer.count(b"\r\n")

        if (n_undecoded_bytes):
            self._byte_buffer       = self._byte_buffer[-n_undecoded_bytes:]
            self._n_undecoded_bytes = n_undecoded_bytes
        else:
            # No need to re-init if already empty
            if (self._n_undecoded_bytes):
                self._byte_buffer       = bytes()
                self._n_undecoded_bytes = 0

        return self._string_buffer
    # ENDIF
