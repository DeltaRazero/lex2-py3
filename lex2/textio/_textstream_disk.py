"""<internal>"""

'''
zlib License

(C) 2020-2025 DeltaRazero
All rights reserved.
'''

# ******************************************************************************

class __:
  '<imports>'

  import pathlib as pl
  import typing  as t
  import sys
  import warnings

  from ._textstream_core import (
    TextstreamInterface,
    TextstreamBase,
    TextstreamType,
  )

# ******************************************************************************

_SYSTEM_ENCODING = __.sys.stdin.encoding

# ******************************************************************************

class TextstreamDisk (__.TextstreamBase, __.TextstreamInterface):
  """Textstream using disk streaming."""

  __slots__ = (
    '_f', '_f_is_eof'
    '_byte_buffer', '_byte_buffer_size', '_n_undecoded_bytes', '_buffer_split'
    '_encoding', '_convert_eol',
  )

  # :: PRIVATE ATTRIBUTES :: #

  _encoding : str
  _convert_eol : bool

  _f_is_eof : bool
  _f : __.t.IO[bytes]

  # If self._buffer is unicode-aware, then a separate byte/char buffer is required
  # so any undecoded characters are preserved.
  _byte_buffer : bytes
  _byte_buffer_size  : int
  _n_undecoded_bytes : int

  _buffer_split : int

  # :: CONSTRUCTOR :: #

  def __init__(self,
    fp: str | __.pl.Path,
    buffer_size: int,
    encoding: str,
    convert_line_endings: bool,
  ) -> None:
    """
    Parameters
    ----------
    fp : str | Path
      Path to a file. Opens in string mode.
    buffer_size : int, optional
      Size of the buffer in thousand characters. A value of zero (0) allocates
      the whole file into memory.
      In order to capture a token, its length must be smaller or equal to half
      the buffer size.
      Buffer size will be floored to the nearest even number.
    encoding : str, optional
      Text encoding of the file.
    convert_line_endings : bool, optional
      Convert line endings from Windows style to UNIX style.
    """
    super().__init__(__.TextstreamType.DISK)

    self._encoding   = encoding
    self._convert_eol = convert_line_endings

    # Enforce minimum buffer size.
    if (buffer_size < 256):
      buffer_size=256
      __.warnings.warn(category=RuntimeWarning, message=
        f"Enforced buffer size to {buffer_size} as that is the minimum required size to operate functionally."
      )

    # Ensure even number.
    self._byte_buffer_size = buffer_size // 2 * 2
    self._byte_buffer = bytes()
    self._n_undecoded_bytes = 0

    self._f_is_eof = False
    self._f = open(fp, "rb") # pylint: disable=consider-using-with

    self._read(self._byte_buffer_size)
    self._refresh_buffer_meta()

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
    self._buffer = ""

    return

  # @profile
  def update(self, n: int) -> None:
    if (n < 1):
      if (n < 0):
        raise ValueError("Requested update size is invalid: smaller than 0.")
      return

    # Block reading more than the allocated buffer size
    if (n > self._buffer_size):
      raise ValueError("Requested update size is invalid: bigger than the allocated buffer string size.")

    self._update_position(n)

    if (self._f_is_eof):
      if (self._buffer_pos >= self._buffer_size):
        self._is_eof = True

    elif (self._buffer_pos > self._buffer_split):
      # FOR MULTI-BYTE ENCODED OR ASCII-ONLY STRINGS:
      # # Amount of chars read by the textstream.
      # chars_read = len( self._buffer[:self._buffer_pos] )
      # self._buffer = (
      #   self._buffer[self._buffer_pos:] + self._read(chars_read)
      # )
      # self._refresh_buffer_meta()

      # FOR UNICODE-AWARE STRINGS:
      # Remainder to fill entire buffer in bytes.
      remainder = self._byte_buffer_size - self._binary_string_length(self._buffer)
      bytes_read = self._binary_string_length(
        self._buffer[:self._buffer_pos]
      )
      self._buffer = (
         self._buffer[self._buffer_pos:] + self._read(bytes_read + remainder)
      )
      self._refresh_buffer_meta()

    return

  # :: PRIVATE METHODS :: #

  # @staticmethod
  def _binary_string_length(self, s: str) -> int:
    return len(s.encode(self._encoding))

  # NOTE: In case only system-locale decoding is needed (which in most cases is
  # UTF-8), usage of the method below is encourages instead.

  # @staticmethod
  def _binary_string_length_locale(self, s: str) -> int:
    return len(s.encode(_SYSTEM_ENCODING))

  def _refresh_buffer_meta(self) -> None:
    self._buffer_pos   = 0
    self._buffer_size  = len(self._buffer)
    self._buffer_split = self._buffer_size // 2

    return

  def _read(self, n_bytes: int) -> str:
    # FOR MULTI-BYTE ENCODED OR ASCII-ONLY STRINGS:
    # self._buffer = str( self._f.read(n_bytes) )
    # return self._buffer

    # FOR UNICODE-AWARE STRINGS:
    n_bytes -= self._n_undecoded_bytes
    tmp = self._f.read(n_bytes)

    # If the amount of bytes is lower than given, then file EOF is reached.
    bytes_read = len(tmp)
    if (bytes_read < n_bytes):
      self._f_is_eof = True
      n_bytes = bytes_read

    # If a multi-byte encoded character has missing bytes, insert the already
    # read bytes at the beginning of the buffer. This ensures that any incomplete
    # multi-byte encoded characters are loaded fully.
    if (self._n_undecoded_bytes):
      self._byte_buffer = self._byte_buffer + tmp
    # Otherwise just assign the read bytes to the buffer.
    else:
      self._byte_buffer = tmp

    # Decode to a string object with configured text encoding.
    self._buffer = self._byte_buffer.decode(encoding=self._encoding, errors="ignore")

    # Don't count carriage return characters (\r) towards n_undecoded_bytes.
    eol_adjust = 0
    if (self._convert_eol):
      size_before = len(self._buffer)
      self._buffer = self._buffer.replace("\r", "")
      eol_adjust = size_before - len(self._buffer)

    # In case multi-byte characters are present, some may not have been decoded
    # towards the end of the buffer. We keep those undecoded bytes and insert
    # them at the beginning og the next buffer when updating.
    n_undecoded_bytes = (
      n_bytes -
      self._binary_string_length(self._buffer) +
      self._n_undecoded_bytes -
      eol_adjust
    )

    if (n_undecoded_bytes):
      self._byte_buffer       = self._byte_buffer[-n_undecoded_bytes:]
      self._n_undecoded_bytes = n_undecoded_bytes
    else:
      # No need to re-initialize if already empty.
      if (self._n_undecoded_bytes):
        self._byte_buffer       = bytes()
        self._n_undecoded_bytes = 0

      return self._buffer
